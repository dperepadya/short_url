import os
import random
import string
import validators
from fastapi import FastAPI, Request, Form, Query, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from repository_worker import FileWorker, MongoWorker

app = FastAPI()
templates = Jinja2Templates(directory="templates")

STORAGE_TYPE = 2
if STORAGE_TYPE == 1:
    FILE_PATH = "url_map.json"
    storage_worker = FileWorker(path=FILE_PATH)
elif STORAGE_TYPE == 2:
    storage_worker = MongoWorker(host=os.getenv("MONGO_HOST", "localhost"),
                                 port=os.getenv("MONGO_PORT", 27017))

def get_short_url():
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))

async def get_original_url_from_db(short_url):
    if short_url is None or len(short_url) == 0:
        return None
    url = await storage_worker.load(short_url)
    return url

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
    # url_map = await storage_worker.load()
    # url_map[short_url] = url
    url_dict = {"short_url": short_url, "url": url}
    await storage_worker.save(url_dict)
    return templates.TemplateResponse(request=request, name="result.html", context={"url_dict": url_dict})

@app.get("/{url:path}")
async def get_original_url(url: str):
    original_url = await get_original_url_from_db(url)
    if not original_url or not validators.url(original_url):
        raise HTTPException(status_code=404, detail=f"URL {original_url} not found")
    return RedirectResponse(url=original_url)

