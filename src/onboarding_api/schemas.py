from pydantic import BaseModel, Field


class InitiateUploadOutput(BaseModel):
    upload_id: int = Field(description="ID to use in chunk upload and status check")
    session_token: str = Field(
        description="Session token to send along with chunk upload"
    )


class InitiateUploadInputFileInfo(BaseModel):
    name: str = Field(description="File name")
    size: int = Field(description="File size, byte count")
    mime: str = Field(description="MIME type")
    hash: str = Field(description="SHA-256 digest of the file content")


class InitiateUploadInput(BaseModel):
    file_info: InitiateUploadInputFileInfo = Field(description="File info")
