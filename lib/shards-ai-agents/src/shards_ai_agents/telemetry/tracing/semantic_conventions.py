"""Typed semantic convention attributes for OpenTelemetry spans.

Each function maps Python keyword arguments to standard or namespaced
OTEL attribute keys, returning a plain dict with None values filtered:

    attrs = {
        **semconv.gen_ai(operation_name="chat", request_model="gpt-4"),
        **semconv.shards_ai_agents_span(event_name="llm_call_started", subject="gpt-4"),
    }

Standard conventions:
    gen_ai()        https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/

Custom conventions (shards_ai_agents.* namespace):
    shards_ai_agents_span()   Common attributes on every Shards-ai-agents span
    shards_ai_agents_crew()   shards_ai_agents.crew.*
    shards_ai_agents_task()   shards_ai_agents.task.*
    shards_ai_agents_agent()  shards_ai_agents.agent.*
    shards_ai_agents_flow()   shards_ai_agents.flow.*
    shards_ai_agents_method()    shards_ai_agents.method.*
    shards_ai_agents_reasoning()  shards_ai_agents.reasoning.*
    shards_ai_agents_guardrail()  shards_ai_agents.guardrail.*
    shards_ai_agents_policy()     shards_ai_agents.policy.*
    shards_ai_agents_memory()     shards_ai_agents.memory.*
    shards_ai_agents_knowledge()  shards_ai_agents.knowledge.*
    shards_ai_agents_tool()       shards_ai_agents.tool.*
    shards_ai_agents_llm()        shards_ai_agents.llm.*
    shards_ai_agents_mcp()        shards_ai_agents.mcp.*
    shards_ai_agents_a2a()        shards_ai_agents.a2a.*
    shards_ai_agents_human_feedback()  shards_ai_agents.human_feedback.*
"""

from __future__ import annotations

from collections.abc import Callable
import json
import logging
from typing import Any

from shards_ai_agents.telemetry.tracing import gen_ai_shapes


logger = logging.getLogger(__name__)


# Attribute keys for duration and count metrics.
# Use these constants instead of hardcoding the strings to keep a single
# source of truth.  The dict-building functions below use the same keys.
CREW_EXECUTION_DURATION_MS = "shards_ai_agents.crew.execution_duration_ms"
AGENT_EXECUTION_DURATION_MS = "shards_ai_agents.agent.execution_duration_ms"
AGENT_LLM_CALLS_COUNT = "shards_ai_agents.agent.llm_calls_count"
FLOW_EXECUTION_DURATION_MS = "shards_ai_agents.flow.execution_duration_ms"
METHOD_DURATION_MS = "shards_ai_agents.method.duration_ms"
MEMORY_QUERY_DURATION_MS = "shards_ai_agents.memory.query_duration_ms"
MEMORY_RETRIEVAL_DURATION_MS = "shards_ai_agents.memory.retrieval_duration_ms"
MEMORY_SAVE_DURATION_MS = "shards_ai_agents.memory.save_duration_ms"
MCP_CONNECTION_DURATION_MS = "shards_ai_agents.mcp.connection_duration_ms"
MCP_TOOL_EXECUTION_DURATION_MS = "shards_ai_agents.mcp.tool_execution_duration_ms"
HUMAN_FEEDBACK_WAIT_DURATION_MS = "shards_ai_agents.human_feedback.wait_duration_ms"
HUMAN_FEEDBACK_REQUEST_ID = "shards_ai_agents.human_feedback.request_id"

# Attribute keys that let a consumer of the spans reason about a run without
# reconstructing it from raw text.
TASK_OUTPUT_FORMAT = "shards_ai_agents.task.output_format"
"""The output format the task declared: ``json``, ``pydantic`` or ``raw``."""
TASK_OUTPUT_PYDANTIC_PRODUCED = "shards_ai_agents.task.output_pydantic_produced"
"""Whether the task's output actually carries a parsed Pydantic object."""
TASK_OUTPUT_JSON_PRODUCED = "shards_ai_agents.task.output_json_produced"
"""Whether the task's output actually carries a parsed JSON dict."""
TOOL_FROM_CACHE = "shards_ai_agents.tool.from_cache"
"""Whether the tool result came from the tool cache rather than a live run."""

GEN_AI_OP_INVOKE_WORKFLOW = "invoke_workflow"
GEN_AI_OP_EXECUTE_METHOD = "execute_method"
GEN_AI_OP_EXECUTE_TASK = "execute_task"


def _filter_none(attrs: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in attrs.items() if v is not None}


def _safe_shape(
    transform: Callable[[Any], Any], value: Any, attr: str
) -> tuple[str | None, dict[str, Any]]:
    try:
        normalized = transform(value)
        if normalized is None:
            return None, {}
        serialized = json.dumps(normalized, default=str)
        return gen_ai_shapes.truncate_attr(serialized, attr=attr)
    except Exception:
        logger.warning(
            "OTel %s serialization failed; dropping attribute", attr, exc_info=True
        )
        return None, {}


def _safe_output(
    response: Any,
    *,
    explicit_finish: str | None = None,
) -> tuple[str | None, list[str] | None, dict[str, Any]]:
    """Shape ``response`` into the OTel ``gen_ai.output.messages`` payload.

    When ``explicit_finish`` is supplied (the OSS event surfaced a real
    provider finish reason) every shaped message's ``finish_reason`` is
    overridden so the per-message field stays in lockstep with the
    span-level ``gen_ai.response.finish_reasons``. Without this the inferred
    default (typically ``"stop"``) would be embedded in the JSON payload
    while the span attribute shows e.g. ``length`` / ``content_filter``.

    The returned tuple also carries ``marker_attrs`` populated when the
    serialized payload exceeded the per-attribute byte cap; see
    :func:`shards_ai_agents.telemetry.tracing.gen_ai_shapes.truncate_attr`. Any failure
    in shaping, serialization, or truncation drops the attribute and logs.
    """
    try:
        shaped = gen_ai_shapes.to_output_messages(response)
        if shaped is None:
            return None, None, {}
        if explicit_finish:
            for msg in shaped:
                if isinstance(msg, dict):
                    msg["finish_reason"] = explicit_finish
        finish_reasons = gen_ai_shapes.finish_reasons_from_messages(shaped)
        serialized = json.dumps(shaped, default=str)
        payload, markers = gen_ai_shapes.truncate_attr(
            serialized, attr="gen_ai.output.messages"
        )
        return payload, finish_reasons, markers
    except Exception:
        logger.warning(
            "OTel gen_ai.output.messages serialization failed; dropping attribute",
            exc_info=True,
        )
        return None, None, {}


def _payload_size(payload: str | None) -> int | None:
    """Return ``len(payload)`` for an already-serialized JSON string.

    Used for ``gen_ai.input.messages.size`` / ``gen_ai.output.messages.size``
    so consumers can budget storage / display without re-shaping the parts
    payload. Reflects the post-truncation size — when truncation fired,
    ``<attr>.original_size_bytes`` carries the pre-truncation byte count
    (see :func:`shards_ai_agents.telemetry.tracing.gen_ai_shapes.truncate_attr`).
    """
    if payload is None:
        return None
    return len(payload)


def gen_ai(
    *,
    operation_name: str | None = None,
    agent_name: str | None = None,
    agent_id: str | None = None,
    agent_description: str | None = None,
    workflow_name: str | None = None,
    request_model: str | None = None,
    response_model: str | None = None,
    provider_name: str | None = None,
    system_instructions: str | None = None,
    tool_definitions: list[Any] | None = None,
    tool_name: str | None = None,
    tool_type: str | None = None,
    tool_call_arguments: dict[str, Any] | str | None = None,
    tool_call_result: Any = None,
    input_messages: Any = None,
    output_messages: Any = None,
    output_type: str | None = None,
    temperature: float | None = None,
    top_p: float | None = None,
    max_tokens: int | None = None,
    stream: bool | None = None,
    seed: int | None = None,
    stop_sequences: list[str] | None = None,
    frequency_penalty: float | None = None,
    presence_penalty: float | None = None,
    choice_count: int | None = None,
    response_id: str | None = None,
    finish_reason: str | None = None,
    conversation_id: str | None = None,
) -> dict[str, Any]:
    """Build OTel GenAI span attributes from raw event values.

    Owns both the attribute keys (`gen_ai.input.messages`, `gen_ai.tool.*`, …)
    and the value shapes (parts arrays, finish_reason enums, …) defined in the
    OTel GenAI semantic convention. Spec-shape transforms live in
    `gen_ai_shapes` and are invoked through `_safe_shape` /  `_safe_output`,
    which swallow failures so instrumentation never raises into user code.

    Sampling params (``temperature``/``top_p``/…) and response identifiers
    (``finish_reason``/``response_id``) are optional so older OSS ``shards_ai_agents``
    callers that don't surface those fields keep producing valid spans. When
    ``finish_reason`` is supplied it overrides the value inferred from the
    output payload shape.

    Spec: https://opentelemetry.io/docs/specs/semconv/gen-ai/
    """
    explicit_finish = gen_ai_shapes.coerce_finish_reason(finish_reason)
    output_payload, inferred_finish_reasons, output_markers = _safe_output(
        output_messages, explicit_finish=explicit_finish
    )
    response_finish_reasons = (
        [explicit_finish] if explicit_finish else inferred_finish_reasons
    )
    input_payload, input_markers = _safe_shape(
        gen_ai_shapes.to_input_messages,
        input_messages,
        "gen_ai.input.messages",
    )
    system_payload, system_markers = _safe_shape(
        gen_ai_shapes.to_system_instructions,
        system_instructions,
        "gen_ai.system_instructions",
    )
    tool_definitions_payload, tool_definitions_markers = _safe_shape(
        gen_ai_shapes.to_tool_definitions,
        tool_definitions,
        "gen_ai.tool.definitions",
    )
    tool_args_payload, tool_args_markers = _safe_shape(
        gen_ai_shapes.to_tool_call_arguments,
        tool_call_arguments,
        "gen_ai.tool.call.arguments",
    )
    tool_result_payload, tool_result_markers = _safe_shape(
        gen_ai_shapes.to_tool_call_result,
        tool_call_result,
        "gen_ai.tool.call.result",
    )

    return _filter_none(
        {
            "gen_ai.operation.name": operation_name,
            "gen_ai.agent.name": agent_name,
            "gen_ai.agent.id": agent_id,
            "gen_ai.agent.description": agent_description,
            "gen_ai.workflow.name": workflow_name,
            "gen_ai.request.model": request_model,
            "gen_ai.response.model": response_model,
            "gen_ai.provider.name": provider_name,
            "gen_ai.output.type": output_type,
            "gen_ai.request.temperature": temperature,
            "gen_ai.request.top_p": top_p,
            "gen_ai.request.max_tokens": max_tokens,
            "gen_ai.request.stream": stream,
            "gen_ai.request.seed": seed,
            "gen_ai.request.stop_sequences": stop_sequences,
            "gen_ai.request.frequency_penalty": frequency_penalty,
            "gen_ai.request.presence_penalty": presence_penalty,
            "gen_ai.request.choice.count": choice_count,
            "gen_ai.response.id": response_id,
            "gen_ai.system_instructions": system_payload,
            "gen_ai.tool.definitions": tool_definitions_payload,
            "gen_ai.tool.name": tool_name,
            "gen_ai.tool.type": tool_type,
            "gen_ai.tool.call.arguments": tool_args_payload,
            "gen_ai.tool.call.result": tool_result_payload,
            "gen_ai.input.messages": input_payload,
            "gen_ai.input.messages.size": _payload_size(input_payload),
            "gen_ai.output.messages": output_payload,
            "gen_ai.output.messages.size": _payload_size(output_payload),
            "gen_ai.response.finish_reasons": response_finish_reasons,
            "gen_ai.conversation.id": conversation_id,
            **input_markers,
            **output_markers,
            **system_markers,
            **tool_definitions_markers,
            **tool_args_markers,
            **tool_result_markers,
        }
    )


def gen_ai_usage(
    *,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
    cached_input_tokens: int | None = None,
    reasoning_tokens: int | None = None,
    cache_creation_tokens: int | None = None,
) -> dict[str, Any]:
    return _filter_none(
        {
            "gen_ai.usage.input_tokens": input_tokens,
            "gen_ai.usage.output_tokens": output_tokens,
            "gen_ai.usage.cache_read.input_tokens": cached_input_tokens,
            "gen_ai.usage.cache_creation.input_tokens": cache_creation_tokens,
            "gen_ai.usage.reasoning_tokens": reasoning_tokens,
        }
    )


def gen_ai_io(
    *, input_value: str | None = None, output_value: str | None = None
) -> dict[str, Any]:
    """Input/output for non-LLM (workflow/orchestration) spans.

    The OTel GenAI spec requires ``gen_ai.input.messages`` /
    ``gen_ai.output.messages`` to follow the input-messages JSON schema (an
    array of ``{role, parts:[{type, content}]}``). Orchestration spans carry
    arbitrary already-serialized payloads (handlers call ``_serialize``), so they
    are shaped through the same ``gen_ai_shapes`` transforms ``gen_ai()`` uses —
    each value becomes a single text message that stays schema-conformant and
    renders across GenAI backends.
    """
    input_payload, input_markers = _safe_shape(
        gen_ai_shapes.to_input_messages, input_value, "gen_ai.input.messages"
    )
    output_payload, output_markers = _safe_shape(
        gen_ai_shapes.to_output_messages, output_value, "gen_ai.output.messages"
    )
    return _filter_none(
        {
            "gen_ai.input.messages": input_payload,
            "gen_ai.output.messages": output_payload,
            **input_markers,
            **output_markers,
        }
    )


def shards_ai_agents_span(
    *,
    event_name: str | None = None,
    subject: str | None = None,
) -> dict[str, Any]:
    return _filter_none(
        {
            "shards_ai_agents.event_name": event_name,
            "shards_ai_agents.subject": subject,
        }
    )


def shards_ai_agents_crew(
    *,
    key: str | None = None,
    name: str | None = None,
    id: str | None = None,
    inputs: str | None = None,
    process: str | None = None,
    num_tasks: int | None = None,
    num_agents: int | None = None,
    output: str | None = None,
    usage_metrics: str | None = None,
    execution_duration_ms: float | None = None,
) -> dict[str, Any]:
    return _filter_none(
        {
            "shards_ai_agents.crew.key": key,
            "shards_ai_agents.crew.name": name,
            "shards_ai_agents.crew.id": id,
            "shards_ai_agents.crew.inputs": inputs,
            "shards_ai_agents.crew.process": process,
            "shards_ai_agents.crew.num_tasks": num_tasks,
            "shards_ai_agents.crew.num_agents": num_agents,
            "shards_ai_agents.crew.output": output,
            "shards_ai_agents.crew.usage_metrics": usage_metrics,
            CREW_EXECUTION_DURATION_MS: execution_duration_ms,
        }
    )


def shards_ai_agents_task(
    *,
    key: str | None = None,
    id: str | None = None,
    name: str | None = None,
    description: str | None = None,
    expected_output: str | None = None,
    output: str | None = None,
    output_format: str | None = None,
    output_pydantic_produced: bool | None = None,
    output_json_produced: bool | None = None,
) -> dict[str, Any]:
    return _filter_none(
        {
            "shards_ai_agents.task.key": key,
            "shards_ai_agents.task.id": id,
            "shards_ai_agents.task.name": name,
            "shards_ai_agents.task.description": description,
            "shards_ai_agents.task.expected_output": expected_output,
            "shards_ai_agents.task.output": output,
            TASK_OUTPUT_FORMAT: output_format,
            TASK_OUTPUT_PYDANTIC_PRODUCED: output_pydantic_produced,
            TASK_OUTPUT_JSON_PRODUCED: output_json_produced,
        }
    )


def shards_ai_agents_agent(
    *,
    role: str | None = None,
    key: str | None = None,
    llm_calls_count: int | None = None,
    execution_duration_ms: float | None = None,
) -> dict[str, Any]:
    return _filter_none(
        {
            "shards_ai_agents.agent.role": role,
            "shards_ai_agents.agent.key": key,
            AGENT_LLM_CALLS_COUNT: llm_calls_count,
            AGENT_EXECUTION_DURATION_MS: execution_duration_ms,
        }
    )


def shards_ai_agents_flow(
    *,
    name: str | None = None,
    id: str | None = None,
    method_names: str | None = None,
    inputs: str | None = None,
    result: str | None = None,
    execution_duration_ms: float | None = None,
    aggregated_crew_usage_metrics: str | None = None,
) -> dict[str, Any]:
    return _filter_none(
        {
            "shards_ai_agents.flow.name": name,
            "shards_ai_agents.flow.id": id,
            "shards_ai_agents.flow.method_names": method_names,
            "shards_ai_agents.flow.inputs": inputs,
            "shards_ai_agents.flow.result": result,
            FLOW_EXECUTION_DURATION_MS: execution_duration_ms,
            "shards_ai_agents.flow.aggregated_crew_usage_metrics": aggregated_crew_usage_metrics,
        }
    )


def shards_ai_agents_method(
    *,
    name: str | None = None,
    state: str | None = None,
    params: str | None = None,
    result: str | None = None,
    duration_ms: float | None = None,
) -> dict[str, Any]:
    return _filter_none(
        {
            "shards_ai_agents.method.name": name,
            "shards_ai_agents.method.state": state,
            "shards_ai_agents.method.params": params,
            "shards_ai_agents.method.result": result,
            METHOD_DURATION_MS: duration_ms,
        }
    )


def shards_ai_agents_reasoning(
    *,
    attempt: int | None = None,
    plan: str | None = None,
    ready: bool | None = None,
) -> dict[str, Any]:
    return _filter_none(
        {
            "shards_ai_agents.reasoning.attempt": attempt,
            "shards_ai_agents.reasoning.plan": plan,
            "shards_ai_agents.reasoning.ready": ready,
        }
    )


def shards_ai_agents_guardrail(
    *,
    guardrail: str | None = None,
    guardrail_type: str | None = None,
    retry_count: int | None = None,
    success: bool | None = None,
    result: str | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    return _filter_none(
        {
            "shards_ai_agents.guardrail.description": guardrail,
            "shards_ai_agents.guardrail.type": guardrail_type,
            "shards_ai_agents.guardrail.retry_count": retry_count,
            "shards_ai_agents.guardrail.success": success,
            "shards_ai_agents.guardrail.result": result,
            "shards_ai_agents.guardrail.error": error,
        }
    )


def shards_ai_agents_policy(
    *,
    id: str | None = None,
    name: str | None = None,
    decision: str | None = None,
    mode: str | None = None,
    point: str | None = None,
    reason: str | None = None,
    blocking: bool | None = None,
    degradation_stage: str | None = None,
    degradation_error: str | None = None,
    absent_fields: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    return _filter_none(
        {
            "shards_ai_agents.policy.id": id,
            "shards_ai_agents.policy.name": name,
            "shards_ai_agents.policy.decision": decision,
            "shards_ai_agents.policy.mode": mode,
            "shards_ai_agents.policy.point": point,
            "shards_ai_agents.policy.reason": reason,
            "shards_ai_agents.policy.blocking": blocking,
            "shards_ai_agents.policy.degradation.stage": degradation_stage,
            "shards_ai_agents.policy.degradation.error": degradation_error,
            "shards_ai_agents.policy.absent_fields": (
                ",".join(absent_fields) if absent_fields else None
            ),
        }
    )


def shards_ai_agents_memory(
    *,
    query: str | None = None,
    value: str | None = None,
    limit: int | None = None,
    score_threshold: float | None = None,
    results: str | None = None,
    memory_content: str | None = None,
    metadata: str | None = None,
) -> dict[str, Any]:
    return _filter_none(
        {
            "shards_ai_agents.memory.query": query,
            "shards_ai_agents.memory.value": value,
            "shards_ai_agents.memory.limit": limit,
            "shards_ai_agents.memory.score_threshold": score_threshold,
            "shards_ai_agents.memory.results": results,
            "shards_ai_agents.memory.content": memory_content,
            "shards_ai_agents.memory.metadata": metadata,
        }
    )


def shards_ai_agents_knowledge(
    *,
    task_prompt: str | None = None,
    query: str | None = None,
    retrieved_knowledge: str | None = None,
) -> dict[str, Any]:
    return _filter_none(
        {
            "shards_ai_agents.knowledge.task_prompt": task_prompt,
            "shards_ai_agents.knowledge.query": query,
            "shards_ai_agents.knowledge.retrieved_knowledge": retrieved_knowledge,
        }
    )


def shards_ai_agents_tool(
    *,
    from_cache: bool | None = None,
) -> dict[str, Any]:
    """Attributes of a tool call that completed, whatever it returned.

    ``from_cache`` says whether the result was served from the tool cache; a
    cached call never ran the tool, so its duration and result mean something
    different to a consumer than a live call's.
    """
    return _filter_none(
        {
            TOOL_FROM_CACHE: from_cache,
        }
    )


def shards_ai_agents_tool_failure(
    *,
    message: str | None = None,
    reason: str | None = None,
    code: str | None = None,
    retryable: bool | None = None,
    policy: str | None = None,
) -> dict[str, Any]:
    """Attributes for a tool that ran to completion but reported it failed.

    Distinct from a tool that *raised*: the call returned normally, so without
    these the span looks identical to a successful one.
    """
    return _filter_none(
        {
            "shards_ai_agents.tool.failure.message": message,
            "shards_ai_agents.tool.failure.reason": reason,
            "shards_ai_agents.tool.failure.code": code,
            "shards_ai_agents.tool.failure.retryable": retryable,
            "shards_ai_agents.tool.failure.policy": policy,
        }
    )


def shards_ai_agents_skill(
    *,
    name: str | None = None,
    path: str | None = None,
    disclosure_level: int | None = None,
    search_path: str | None = None,
    skills_found: int | None = None,
    skill_names: str | None = None,
) -> dict[str, Any]:
    return _filter_none(
        {
            "shards_ai_agents.skill.name": name,
            "shards_ai_agents.skill.path": path,
            "shards_ai_agents.skill.disclosure_level": disclosure_level,
            "shards_ai_agents.skill.search_path": search_path,
            "shards_ai_agents.skill.skills_found": skills_found,
            "shards_ai_agents.skill.skill_names": skill_names,
        }
    )


def shards_ai_agents_llm(
    *,
    call_id: str | None = None,
    callbacks: str | None = None,
    available_functions: str | None = None,
    call_type: str | None = None,
) -> dict[str, Any]:
    return _filter_none(
        {
            "shards_ai_agents.llm.call_id": call_id,
            "shards_ai_agents.llm.callbacks": callbacks,
            "shards_ai_agents.llm.available_functions": available_functions,
            "shards_ai_agents.llm.call_type": call_type,
        }
    )


def shards_ai_agents_mcp(
    *,
    server_name: str | None = None,
    server_url: str | None = None,
    transport_type: str | None = None,
    tool_name: str | None = None,
    tool_args: str | None = None,
    tool_result: str | None = None,
    connect_timeout: int | None = None,
    is_reconnect: bool | None = None,
    error_type: str | None = None,
) -> dict[str, Any]:
    return _filter_none(
        {
            "shards_ai_agents.mcp.server_name": server_name,
            "shards_ai_agents.mcp.server_url": server_url,
            "shards_ai_agents.mcp.transport_type": transport_type,
            "shards_ai_agents.mcp.tool_name": tool_name,
            "shards_ai_agents.mcp.tool_args": tool_args,
            "shards_ai_agents.mcp.tool_result": tool_result,
            "shards_ai_agents.mcp.connect_timeout": connect_timeout,
            "shards_ai_agents.mcp.is_reconnect": is_reconnect,
            "shards_ai_agents.mcp.error_type": error_type,
        }
    )


def shards_ai_agents_human_feedback(
    *,
    method_name: str | None = None,
    message: str | None = None,
    feedback: str | None = None,
    outcome: str | None = None,
    emit: str | None = None,
    wait_duration_ms: float | None = None,
    request_id: str | None = None,
) -> dict[str, Any]:
    return _filter_none(
        {
            "shards_ai_agents.human_feedback.method_name": method_name,
            "shards_ai_agents.human_feedback.message": message,
            "shards_ai_agents.human_feedback.feedback": feedback,
            "shards_ai_agents.human_feedback.outcome": outcome,
            "shards_ai_agents.human_feedback.emit": emit,
            HUMAN_FEEDBACK_WAIT_DURATION_MS: wait_duration_ms,
            HUMAN_FEEDBACK_REQUEST_ID: request_id,
        }
    )


def shards_ai_agents_a2a(
    *,
    endpoint: str | None = None,
    endpoints: str | None = None,
    task_description: str | None = None,
    agent_id: str | None = None,
    context_id: str | None = None,
    is_multiturn: bool | None = None,
    turn_number: int | None = None,
    a2a_agent_name: str | None = None,
    agent_card: str | None = None,
    protocol_version: str | None = None,
    skill_id: str | None = None,
    metadata: str | None = None,
    status: str | None = None,
    result: str | None = None,
    final_result: str | None = None,
    total_turns: int | None = None,
    task_id: str | None = None,
    success_count: int | None = None,
    failure_count: int | None = None,
    results: str | None = None,
) -> dict[str, Any]:
    return _filter_none(
        {
            "shards_ai_agents.a2a.endpoint": endpoint,
            "shards_ai_agents.a2a.endpoints": endpoints,
            "shards_ai_agents.a2a.task_description": task_description,
            "shards_ai_agents.a2a.agent_id": agent_id,
            "shards_ai_agents.a2a.context_id": context_id,
            "shards_ai_agents.a2a.is_multiturn": is_multiturn,
            "shards_ai_agents.a2a.turn_number": turn_number,
            "shards_ai_agents.a2a.agent_name": a2a_agent_name,
            "shards_ai_agents.a2a.agent_card": agent_card,
            "shards_ai_agents.a2a.protocol_version": protocol_version,
            "shards_ai_agents.a2a.skill_id": skill_id,
            "shards_ai_agents.a2a.metadata": metadata,
            "shards_ai_agents.a2a.status": status,
            "shards_ai_agents.a2a.result": result,
            "shards_ai_agents.a2a.final_result": final_result,
            "shards_ai_agents.a2a.total_turns": total_turns,
            "shards_ai_agents.a2a.task_id": task_id,
            "shards_ai_agents.a2a.success_count": success_count,
            "shards_ai_agents.a2a.failure_count": failure_count,
            "shards_ai_agents.a2a.results": results,
        }
    )
