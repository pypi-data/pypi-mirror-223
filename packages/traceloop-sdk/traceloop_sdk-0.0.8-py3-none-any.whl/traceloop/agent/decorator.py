from typing import Optional

from traceloop.semconv import TraceloopSpanKindValues
from traceloop.task.decorator import task


def agent(name: Optional[str] = None):
    return task(name=name, tlp_span_kind=TraceloopSpanKindValues.AGENT)
