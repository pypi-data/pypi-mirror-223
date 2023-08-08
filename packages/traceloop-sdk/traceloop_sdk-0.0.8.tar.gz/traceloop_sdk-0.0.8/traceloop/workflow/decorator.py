from functools import wraps
from typing import Optional

from traceloop.semconv import SpanAttributes, TraceloopSpanKindValues
from traceloop.tracing.tracer import Tracer


def workflow(name: Optional[str] = None):
    def decorate(fn):
        @wraps(fn)
        def wrap(*args, **kwargs):
            span_name = f"{name}.workflow" if name else f"{fn.__name__}.workflow"
            with Tracer.instance().start_as_current_span(span_name) as span:
                span.set_attribute(SpanAttributes.TRACELOOP_SPAN_KIND, TraceloopSpanKindValues.WORKFLOW.value)
                return fn(*args, **kwargs)
        return wrap
    return decorate
