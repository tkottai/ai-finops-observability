from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource

def setup_otel(app):
    # Resource information
    resource = Resource.create({
        "service.name": "ai-finops-observability"
    })

    # ----- Tracing -----
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    # For now we keep it simple (you can later add OTLP exporter for Tempo/Jaeger)
    # tracer_provider.add_span_processor(BatchSpanProcessor(...))

    # ----- Metrics -----
    reader = PrometheusMetricReader()
    meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meter_provider)

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)
