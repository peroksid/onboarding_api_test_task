from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from importlib_resources import files

from .crud import create_upload
from .dependencies import PoolDep, UUID4Dep
from .schemas import InitiateUploadInput, InitiateUploadOutput


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def get_example_simple_client():
    return (
        files("onboarding_api.example_simple_client").joinpath("index.html").read_text()
    )


@app.post("/upload", response_model=InitiateUploadOutput)
def initiate_upload(input: InitiateUploadInput, session_token: UUID4Dep, pool: PoolDep):
    upload_id = create_upload(
        pool,
        session_token,
        input.file_info.name,
        input.file_info.mime,
        input.file_info.size,
        input.file_info.hash,
    )
    return InitiateUploadOutput(upload_id=upload_id, session_token=str(session_token))
