from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import subprocess
import os

app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse(url="/streamlit/")

@app.on_event("startup")
async def startup_event():
    subprocess.Popen(["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"])

@app.get("/streamlit/{path_name:path}")
async def proxy(path_name: str):
    from starlette.responses import Response
    import httpx

    url = f"http://localhost:8501/{path_name}"
    async with httpx.AsyncClient() as client:
        proxy = await client.get(url)
    return Response(content=proxy.content, media_type=proxy.headers["Content-Type"])
