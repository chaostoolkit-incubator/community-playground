import datetime
import sys

from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import JSONResponse
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
import uvicorn

version = f"{sys.version_info.major}.{sys.version_info.minor}"
templates = Jinja2Templates(directory='templates')

app = Starlette()
app.mount('/static', StaticFiles(directory='statics'), name='static')

@app.route('/')
async def homepage(request):
    template = "index.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)

@app.route("/msg")
async def message(request):
    message = f"Hello world! From Starlette running on Uvicorn with Gunicorn in Alpine."
    return JSONResponse({"message": message, "version": version})

@app.route('/dt')
async def mydatetime(request):
    print(datetime.datetime.now())
    return JSONResponse({'hello': 'world', 'now': str(datetime.datetime.now())})

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
