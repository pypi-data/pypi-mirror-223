from functools import wraps
from typing import Optional

from traceloop.semconv import TraceloopSpanKindValues, SpanAttributes
from traceloop.tracing.tracer import Tracer


def task(name: Optional[str] = None, tlp_span_kind: Optional[TraceloopSpanKindValues] = TraceloopSpanKindValues.TASK):
    def decorate(fn):
        @wraps(fn)
        def wrap(*args, **kwargs):
            span_name = f"{name}.{tlp_span_kind.value}" if name else f"{fn.__name__}.{tlp_span_kind.value}"
            with Tracer.instance().start_as_current_span(span_name) as span:
                span.set_attribute(SpanAttributes.TRACELOOP_SPAN_KIND, tlp_span_kind.value)
                return fn(*args, **kwargs)
        return wrap
    return decorate

