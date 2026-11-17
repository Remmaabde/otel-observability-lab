import time
import random
import logging
import sys
from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# Configure standard logging to output to stdout so Docker/Loki can capture it effortlessly
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("python-otel-app")

# Setup Resource
resource = Resource.create(attributes={"service.name": "python-otel-app"})

# Setup Tracing
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="otel-collector:4317", insecure=True))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = FastAPI()

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["endpoint", "status"])

@app.get("/")
def read_root():
    with tracer.start_as_current_span("root-span"):
        logger.info("Handling request for root endpoint '/' successfully.")
        REQUEST_COUNT.labels(endpoint="/", status="200").inc()
        return {"message": "Hello from OpenTelemetry Lab!"}

@app.get("/slow")
def read_slow():
    with tracer.start_as_current_span("slow-span"):
        delay = random.uniform(0.5, 2.0)
        logger.warning(f"Request is running slowly with a delay of {round(delay, 2)} seconds.")
        time.sleep(delay)
        REQUEST_COUNT.labels(endpoint="/slow", status="200").inc()
        return {"message": "Responded slowly", "delay_seconds": round(delay, 2)}

@app.get("/error")
def read_error():
    with tracer.start_as_current_span("error-span"):
        logger.error("An internal error occurred while processing the /error endpoint!")
        REQUEST_COUNT.labels(endpoint="/error", status="500").inc()
        raise ValueError("Simulated internal server error!")

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)