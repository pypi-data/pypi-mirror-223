#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import wraps
import logging
import time
from typing import Any, Awaitable, Callable, cast, Coroutine, Dict, List, Optional, Tuple

from langchain import PromptTemplate
from langchain.callbacks.manager import AsyncCallbackManagerForChainRun, CallbackManagerForChainRun
from langchain.chains.base import Chain
import pandas as pd
from pydantic import validator

try:
    from datarobot.mlops.connected.client import MLOpsClient
except ImportError:
    # we will raise an error in the public entry point
    pass

import datarobotx.client.deployments as deploy_client
from datarobotx.common.config import context
from datarobotx.common.utils import create_task_new_thread

logger = logging.getLogger("guard")

OutputType = Any

_fire_and_forget_tasks = set()


def validate_mlops_client_version(entry_point: str) -> None:
    try:
        from datarobot.mlops.connected.client import MLOpsClient

        assert hasattr(MLOpsClient, "report_custom_metrics")
    except (ImportError, AssertionError):
        raise RuntimeError(f"{entry_point} requires datarobot-mlops-connected-client>=9.1.1b3")


def fire_and_forget(coro: Coroutine[Any, Any, Any]) -> None:
    """Ensure fire and forget tasks are not garbage collected."""
    task = asyncio.create_task(coro)
    _fire_and_forget_tasks.add(task)
    task.add_done_callback(_fire_and_forget_tasks.discard)


@dataclass
class GuardrailConfig:
    """Guardrail configuration.

    Parameters
    ----------
    deployment_id : str
        DR MLOps deployment id for the guardrail
    datarobot_key : str
        MLOps DR key to be used when making predictions with the guardrail
    prediction_server_endpoint : str
        Prediction server endpoint (including API + version suffix) for
        making predictions with the guardrail
    blocked_msg : str, optional
        Message that should be returned as output if the guardrail flags an input
    guardrail_prompt: PromptTemplate, optional
        Prompt template to be used to control how input(s) are combined and
        formatted as a string before being passed to the guardrail; if omitted
        the inputs will be presented as a newline-separated string of key: value
        pairs
    input_parser: Callable, optional
        Hook to customize how a formatted guardrail prompt string should be passed to the
        guardrail as JSON; callable should accept a string and return a dictionary
        that is serializable to JSON
    output_parser: Callable, optional
        Hook to customize how to determine whether the input was flagged
        by the guardrail model based on the guardrail model's output; callable should
        accept a dictionary (deserialized JSON) and return a bool indicating whether
        the guardrail flagged this input
    timeout_secs: float, optional, default=5.0
        Maximum time to wait in seconds for guardrail to return
    bypass_on_timeout: bool, optional, default=False
        Whether to bypass the guardrail or block content if the guardrail times out
    """

    deployment_id: str
    datarobot_key: str
    prediction_server_endpoint: str
    blocked_msg: str = (
        "This content has been blocked because it did not meet acceptable use guidelines."
    )
    guardrail_prompt: Optional[PromptTemplate] = None
    input_parser: Callable[[str], Dict[str, Any]] = lambda x: {"input": x}
    output_parser: Callable[[Dict[str, Any]], bool] = lambda x: bool(x["flagged"])
    timeout_secs: float = 5.0
    bypass_on_timeout: bool = False


@dataclass
class MonitoringConfig:
    """Monitoring deployment configuration.

    Parameters
    ----------
    deployment_id : str
        DR MLOps deployment id to use when reporting predictions, service health, guardrail interventions
    model_id : str
        DR model id to use when reporting predictions, service health, guardrail interventions
    inputs_parser : Callable, optional
        Function for mapping the positional and keyword arguments passed to the monitored function to a
        dictionary; key-value pairs in this resulting dictionary are used as feature names and feature
        values when reporting prediction data to ML Ops. The values in this dictionary must be of type
        that is reportable to ML Ops. Default is to report the first positional argument as a feature
        named 'prompt'.
    output_parser : Callable, optional
        Function for mapping the value returned from the monitored function to a dictionary; key-value
        pairs in this resulting dictionary are reported as additional feature names and features values
        when reporting prediction data to ML Ops. The values in this dictionary must be of type that is
        reportable to ML Ops. Default is to associate the return value of the function with the feature
        'completion'
    target : str, optional
        The name of the feature that will be reported as the target value to ML Ops. Default is
        'completion'
    intervention_metric_id : str, optional
        DR custom metric id to be optionally used for reporting guardrail interventions

    """

    deployment_id: str
    model_id: str
    inputs_parser: Callable[..., Dict[str, Any]] = lambda *args, **kwargs: {"prompt": args[0]}
    output_parser: Callable[..., Dict[str, Any]] = lambda return_value: {"completion": return_value}
    target: str = "completion"
    intervention_metric_id: Optional[str] = None


def format_guardrail_prompt(
    inputs: Dict[str, str], guardrail_prompt: Optional[PromptTemplate] = None
) -> str:
    """Format prompt for the guardrail model to evaluate if output should be blocked based on input(s)."""
    try:
        if guardrail_prompt is not None:
            return guardrail_prompt.format(**inputs)
    except (TypeError, KeyError):
        pass

    return "\n".join([f"{str(key)}: {str(value)}" for key, value in inputs.items()])


async def arecord_intervention(
    deployment_id: str, model_id: str, intervention_metric_id: str
) -> None:
    """Report guardrail intervention to DR MLOps."""
    try:
        mclient = MLOpsClient(
            service_url=context._webui_base_url, api_key=context.token
        )  # type: ignore[no-untyped-call]
        ts = datetime.now(timezone.utc).isoformat()
        buckets = [
            {
                "timestamp": ts,
                "value": 1,
            },
        ]
        await mclient.report_custom_metrics(  # type: ignore[no-untyped-call]
            deployment_id, model_id, buckets, intervention_metric_id
        )
        logger.info(
            "Reported a guardrail intervention to DataRobot MLOps deployment %s", deployment_id
        )
        await mclient.shutdown()  # type: ignore[no-untyped-call]
    except Exception as e:
        logger.warning(
            "%s exception raised while reporting intervention data to DataRobot MLOps deployment %s",
            e.__class__.__name__,
            deployment_id,
        )
        if str(e):
            logger.warning("%s: %s", e.__class__.__name__, str(e))


async def arecord_llm_prediction(
    deployment_id: str,
    model_id: str,
    inputs_parser: Callable[..., Dict[str, Any]],
    output_parser: Callable[..., Dict[str, Any]],
    target: str,
    args: Tuple[Any, ...],
    kwargs: Dict[str, str],
    output: OutputType,
    elapsed_ms: int,
) -> None:
    """Report LLM input(s) and output to DR MLOps."""
    try:
        mclient = MLOpsClient(
            service_url=context._webui_base_url, api_key=context.token
        )  # type: ignore[no-untyped-call]
        logger.debug("Parsing inputs for reporting to ML Ops")
        input_features = inputs_parser(*args, **kwargs)

        logger.debug("Parsing output for reporting to ML Ops")
        output_features = output_parser(output)

        features = {**input_features, **output_features}
        msg = f"Inputs and outputs parsed to dictionary: {features}"
        logger.debug(msg)

        await asyncio.gather(
            mclient.report_deployment_stats(  # type: ignore[no-untyped-call]
                deployment_id, model_id, 1, execution_time_ms=elapsed_ms
            ),
            mclient.report_prediction_data(  # type: ignore[no-untyped-call]
                deployment_id, model_id, pd.DataFrame([features]), target_col=target
            ),
        )
        logger.info(
            "Reported LLM input and output data to DataRobot MLOps deployment %s", deployment_id
        )
        await mclient.shutdown()  # type: ignore[no-untyped-call]
    except Exception as e:
        logger.warning(
            "%s exception raised while reporting prediction data to DataRobot MLOps deployment %s",
            e.__class__.__name__,
            deployment_id,
        )
        if str(e):
            logger.warning("%s:%s", e.__class__.__name__, str(e))


async def is_flagged(
    monitor: MonitoringConfig,
    guardrail: Optional[GuardrailConfig],
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> bool:
    """Determine if a guardrail deployment flags user inputs."""
    if guardrail is None:
        return False

    try:
        prompt = format_guardrail_prompt(
            monitor.inputs_parser(*args, **kwargs), guardrail_prompt=guardrail.guardrail_prompt
        )

        guardrail_output = await asyncio.wait_for(
            deploy_client.post_predictions_unstructured(
                did=guardrail.deployment_id,
                dr_key=guardrail.datarobot_key,
                pred_server_endpoint=guardrail.prediction_server_endpoint,
                data=guardrail.input_parser(prompt),
            ),
            guardrail.timeout_secs,
        )
        flagged = guardrail.output_parser(guardrail_output)
        msg = (
            f"Guardrail corresponding to DataRobot MLOps deployment '{guardrail.deployment_id}' evaluated input(s)"
            " and "
        )
        if flagged:
            msg += "flagged output to be blocked"
        else:
            msg += "did not flag output for blocking"
        logger.info(msg)
        return flagged

    except asyncio.TimeoutError:
        msg = (
            f"Guardrail execution corresponding to DataRobot MLOps deployment '{guardrail.deployment_id}' "
            + f"timed out after {guardrail.timeout_secs} seconds; "
        )
        if guardrail.bypass_on_timeout:
            msg += " guardrail bypassed"
        else:
            msg += " flagged output to be blocked"
        logger.warning(msg)
        return not guardrail.bypass_on_timeout

    except BaseException as e:
        logger.warning(
            "%s exception raised while executing guardrail associated with DataRobot MLOps deployment %s",
            e.__class__.__name__,
            guardrail.deployment_id,
        )
        if str(e):
            logger.warning("%s: %s", e.__class__.__name__, str(e))
        return True


def aguard(
    monitor: MonitoringConfig, *guardrails: GuardrailConfig
) -> Callable[[Callable[..., Awaitable[OutputType]]], Callable[..., Awaitable[OutputType]]]:
    """Decorator for monitoring and optionally guardrailing an async entrypoint with DR MLOps.

    Parameters
    ----------
    monitor: MonitoringConfig
        Monitoring configuration
    guardrails: GuardrailConfig, optional
        Guardrail configuration(s)
    """
    validate_mlops_client_version("aguard")

    def wrapper_factory(
        f: Callable[..., Awaitable[OutputType]]
    ) -> Callable[..., Awaitable[OutputType]]:
        @wraps(f)
        async def monitored_entrypoint(*args: Any, **kwargs: Any) -> OutputType:
            start_time = time.time_ns() // 1_000_000
            results = await asyncio.gather(
                f(*args, **kwargs),
                *[is_flagged(monitor, guardrail, args, kwargs) for guardrail in guardrails],
                return_exceptions=True,
            )
            output = cast(OutputType, results.pop(0))
            for idx, guardrail in enumerate(guardrails):
                if results[idx]:  # guardrail flagged?
                    output = guardrail.blocked_msg
                    if monitor.intervention_metric_id is not None:
                        fire_and_forget(
                            arecord_intervention(
                                monitor.deployment_id,
                                monitor.model_id,
                                monitor.intervention_metric_id,
                            )
                        )
                    break
            if isinstance(output, BaseException):
                raise output
            else:
                fire_and_forget(
                    arecord_llm_prediction(
                        monitor.deployment_id,
                        monitor.model_id,
                        monitor.inputs_parser,
                        monitor.output_parser,
                        monitor.target,
                        args,
                        kwargs,
                        output,
                        time.time_ns() // 1_000_000 - start_time,
                    )
                )
                return output

        return monitored_entrypoint

    return wrapper_factory


def guard(
    monitor: MonitoringConfig, *guardrails: GuardrailConfig
) -> Callable[[Callable[..., OutputType]], Callable[..., OutputType]]:
    """Decorator for monitoring and optionally guardrailing a synchronous entrypoint with DR MLOps.

    Notes
    -----
    Useful if application code entry point is not an async function and/or doesn't have a managed event loop
    already running. Will create a new thread for executing the wrapped function and orchestrating
    async logic for reporting status to ML Ops
    """
    validate_mlops_client_version("guard")

    def wrapper_factory(f: Callable[..., OutputType]) -> Callable[..., OutputType]:
        @wraps(f)
        def monitored_entrypoint(*args: Any, **kwargs: Any) -> OutputType:
            start_time = time.time_ns() // 1_000_000

            async def async_wrapper(*args: Any, **kwargs: Any) -> List[Any]:
                """Execute original synchronous function and guardrail logic in new thread

                (with our own managed event loop)
                """

                async def async_f() -> OutputType:
                    return f(*args, **kwargs)

                return await asyncio.gather(
                    async_f(),
                    *[is_flagged(monitor, guardrail, args, kwargs) for guardrail in guardrails],
                    return_exceptions=True,
                )

            results = create_task_new_thread(
                async_wrapper(*args, **kwargs),
                wait=True,
            ).result()
            output = cast(OutputType, results.pop(0))
            for idx, guardrail in enumerate(guardrails):
                if results[idx]:  # guardrail flagged?
                    output = guardrail.blocked_msg
                    if monitor.intervention_metric_id is not None:
                        create_task_new_thread(
                            arecord_intervention(
                                monitor.deployment_id,
                                monitor.model_id,
                                monitor.intervention_metric_id,
                            ),
                            wait=False,
                        )
                    break
            if isinstance(output, BaseException):
                raise output
            else:
                create_task_new_thread(
                    arecord_llm_prediction(
                        monitor.deployment_id,
                        monitor.model_id,
                        monitor.inputs_parser,
                        monitor.output_parser,
                        monitor.target,
                        args,
                        kwargs,
                        output,
                        time.time_ns() // 1_000_000 - start_time,
                    ),
                    wait=False,
                )
                return output

        return monitored_entrypoint

    return wrapper_factory


class GuardChain(Chain):
    """Apply monitoring and guardrails to a chain with DataRobot MLOps.

    Parameters
    ----------
    inner_chain : chain
        The chain being wrapped with monitoring and optional guardrails
    monitor : MonitoringConfig
        Configuration for how to monitor the inner chain
    guardrails : list of GuardrailConfig, optional
        Configuration for how to use guardrails with the inner chain
    """

    inner_chain: Chain
    monitor: MonitoringConfig
    guardrails: List[GuardrailConfig] = []

    @property
    def input_keys(self) -> List[str]:
        """Chain inputs.

        Inherits inputs from inner_chain
        """
        return self.inner_chain.input_keys

    @property
    def output_keys(self) -> List[str]:
        """Chain outputs.

        Inherits outputs from inner_chain
        """
        return self.inner_chain.output_keys

    @validator("inner_chain")
    def wrapped_must_be_single_output(cls, v: Any) -> Any:  # pylint: disable=no-self-argument
        if len(v.output_keys) != 1:
            raise ValueError("Guard chain can only be used with chains that return a single output")
        return v

    @validator("monitor")
    def use_langchain_inputs_parser(cls, v: Any) -> Any:  # pylint: disable=no-self-argument
        v.inputs_parser = lambda *args, **kwargs: args[0]
        return v

    def _call(
        self, inputs: Dict[str, Any], run_manager: Optional[CallbackManagerForChainRun] = None
    ) -> Dict[str, Any]:
        async def chain_output_getter(*args: Any, **kwargs: Any) -> str:
            return cast(str, self.inner_chain(*args, **kwargs)[self.output_keys[0]])

        guarded_call = guard(self.monitor, *self.guardrails)(chain_output_getter)
        return {self.output_keys[0]: guarded_call(inputs, run_manager)}

    async def _acall(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[AsyncCallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        async def chain_output_getter(*args: Any, **kwargs: Any) -> str:
            outputs = await self.inner_chain.acall(*args, **kwargs)
            return cast(str, outputs[self.output_keys[0]])

        guarded_call = aguard(self.monitor, *self.guardrails)(chain_output_getter)
        return {self.output_keys[0]: await guarded_call(inputs, run_manager)}
