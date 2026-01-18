from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from starlette.templating import Jinja2Templates
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

REQUEST_COUNT= Counter(
"http_requests_total",
"Total number of requests",
["method", "path","status"]
)
REQUEST_LATENCY=Histogram(
    "http_request_duration_seconds",
    "Http request latency in seconds",
    ["path"]
)

templates = Jinja2Templates(directory="templates")

async def homepage(request):
    start_time=time.time()
    #return templates.TemplateResponse("index.html", {"request": request})
    Response = JSONResponse({"message": "Testing PRometheus"})
    # ends after response
    duration=time.time()-start_time
    REQUEST_COUNT.labels(request.method,"/", Response.status_code).inc()
    REQUEST_LATENCY.labels("/").observe(duration)
    return Response
async def metrics(request):
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)



routes = [
    Route("/", homepage, name="homepage"),
    Route("/metrics", metrics, name="metrics"),
]

app = Starlette(debug=True, routes=routes)  