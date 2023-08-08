from typing import Optional

from traceloop.semconv import TraceloopSpanKindValues
from traceloop.task.decorator import task


def tool(name: Optional[str] = None):
    return task(name=name, tlp_span_kind=TraceloopSpanKindValues.TOOL)
