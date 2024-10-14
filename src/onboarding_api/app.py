import hashlib
import base64

from typing import Annotated, Union

from fastapi import FastAPI, Header, HTTPException, status
from fastapi.responses import HTMLResponse
from importlib_resources import files

from .crud import create_upload, upload_exists, chunk_exists, create_chunk
from .dependencies import PoolDep, SaveFileDep, UUID4Dep
from .schemas import (
    InitiateUploadInput,
    InitiateUploadOutput,
    UploadChunkInput,
    UploadChunkOutput,
)


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


@app.post("/upload/{upload_id}/chunk", response_model=UploadChunkOutput)
def upload_chunk(
    upload_id: int,
    x_session_token: Annotated[Union[str, None], Header()],
    input: UploadChunkInput,
    save_file: SaveFileDep,
    pool: PoolDep
):
    if x_session_token is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Session token missing"
        )
    if not upload_exists(pool, upload_id, x_session_token):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Upload not found"
        )
    if chunk_exists(pool, upload_id=upload_id, chunk_number=input.number):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Chunk exists already"
        )

    content_bytes = base64.b64decode(input.b64_bytes)

    if input.size != len(content_bytes):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Size does not match",
        )
    if input.hash != hashlib.sha256(content_bytes).hexdigest():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Hash does not match",
        )

    chunk_path = save_file(
        upload_id=upload_id, chunk_number=input.number, content_bytes=content_bytes
    )
    chunk_id = create_chunk(
        pool, upload_id=upload_id, chunk_number=input.number, path=chunk_path
    )
    return UploadChunkOutput(chunk_id=chunk_id)
