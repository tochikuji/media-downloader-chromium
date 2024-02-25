import fastapi
from os import system
from starlette.middleware.cors import CORSMiddleware
from fastapi import Request
import uvicorn

from pydantic import BaseModel
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import os


dstroot = os.environ.get("DATAROOT", "/data")
print(f"dstroot: {dstroot}")


app = fastapi.FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)


class Item(BaseModel):
    url: str


@app.exception_handler(RequestValidationError)
async def handler(request: Request, exc: RequestValidationError):
    print(exc)
    print(request)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.post("/")
def index(item: Item):
    print(item.url)
    system(
        f'yt-dlp -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best -o "{dstroot}/%(title)s.%(ext)s" {item.url}'
    )


@app.options("/")
def options():
    return fastapi.responses.JSONResponse(content={"status": "ok"}, headers={"Access-Control-Allow-Origin": "*"})


uvicorn.run(app, host="127.0.0.1", port=19988, log_level="info")
