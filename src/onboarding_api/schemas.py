from pydantic import BaseModel, Field


class InitiateUploadOutput(BaseModel):
    upload_id: int = Field(description="ID to use in chunk upload and status check")
    session_token: str = Field(
        description="Session token to send along with chunk upload"
    )


class InitiateUploadInputFileInfo(BaseModel):
    name: str = Field(description="File name")
    size: int = Field(description="File size in bytes")
    mime: str = Field(description="MIME type")
    hash: str = Field(description="SHA-256 digest of the file content")


class InitiateUploadInput(BaseModel):
    file_info: InitiateUploadInputFileInfo = Field(description="File info")
    chunk_count: int = Field(description="Expected chunk count")


class UploadChunkInput(BaseModel):
    number: int = Field(description="Number of chunk")
    size: int = Field(description="Chunk size in bytes")
    hash: str = Field(description="SHA-256 digest of the chunk content")
    b64_bytes: str = Field(description="Chunk content")


class UploadChunkOutput(BaseModel):
    chunk_id: int
