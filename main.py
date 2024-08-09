import random
import string
import validators
from fastapi import FastAPI, Request, Form, Query, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from file_worker import FileWorker

app = FastAPI()
templates = Jinja2Templates(directory="templates")

FILE_PATH = "url_map.json"
file_worker = FileWorker(FILE_PATH)

def get_short_url():
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))

async def get_original_url_from_db(short_url):
    if short_url is None or len(short_url) == 0:
        return None
    url_map = await file_worker.load()
    return url_map.get(short_url, None)

@app.get("/", response_class=HTMLResponse)
async def get_url(request: Request, error: str = Query(None)):
    return templates.TemplateResponse(request=request, name="index.html", context={"error": error})

@app.post("/", response_class=HTMLResponse)
async def post_url(request: Request, url: str = Form(...)):
    if not validators.url(url):
        return RedirectResponse(url="/?error=Invalid URL", status_code=302)
    short_url = get_short_url()
    if not short_url:
        raise HTTPException(status_code=500, detail=f"Cannot get Short url for {url}")
    url_map = await file_worker.load()
    url_map[short_url] = url
    await file_worker.save(url_map)
    url_dict = {"url": url, "short_url": short_url}
    return templates.TemplateResponse(request=request, name="result.html", context={"url_dict": url_dict})

@app.get("/{url:path}")
async def get_original_url(url: str):
    original_url = await get_original_url_from_db(url)
    print(original_url)
    if not original_url or not validators.url(original_url):
        raise HTTPException(status_code=404, detail=f"URL {original_url} not found")
    return RedirectResponse(url=original_url)

