import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from traceloop.instrumentation.openai import OpenAIInstrumentor

TRACER_NAME = "traceloop.tracer"
TRACELOOP_API_ENDPOINT = "https://api.traceloop.dev/v1/traces"


class Tracer:
    __instance = None

    @staticmethod
    def init():
        api_key = os.getenv("TRACELOOP_API_KEY")
        api_endpoint = os.getenv("TRACELOOP_API_ENDPOINT") or TRACELOOP_API_ENDPOINT
        print(f"Initializing Traceloop Tracer... API endpoint: {api_endpoint}")
        provider = TracerProvider()
        exporter = OTLPSpanExporter(
            endpoint=api_endpoint,
            headers={
                "Authorization": f"Bearer {api_key}",
            }
        )
        processor = BatchSpanProcessor(exporter)
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        Tracer.__instance = trace.get_tracer(TRACER_NAME)

        os.environ["OTEL_PYTHON_REQUESTS_EXCLUDED_URLS"] = "/openai/"

        OpenAIInstrumentor().instrument()
        RequestsInstrumentor().instrument(excluded_urls="^https://api.openai.com")
        # MySQLInstrumentor().instrument()


    @staticmethod
    def instance():
        if Tracer.__instance is None:
            raise Exception("Tracer is not initialized")
        return Tracer.__instance
