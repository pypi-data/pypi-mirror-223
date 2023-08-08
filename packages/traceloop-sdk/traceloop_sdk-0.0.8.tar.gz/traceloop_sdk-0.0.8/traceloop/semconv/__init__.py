from enum import Enum


class SpanAttributes:
    TRACELOOP_SPAN_KIND = "traceloop.span.kind"


class TraceloopSpanKindValues(Enum):
    WORKFLOW = "workflow"
    TASK = "task"
    AGENT = "agent"
    TOOL = "tool"
    UNKNOWN = "unknown"
