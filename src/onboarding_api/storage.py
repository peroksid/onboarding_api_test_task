import pathlib
from .config import get_settings


def save_file(upload_id, chunk_number, content_bytes) -> str:
    chunks_storage = pathlib.Path(get_settings().storage_path)
    upload_root = chunks_storage / str(upload_id)

    if not upload_root.exists():
        upload_root.mkdir()

    chunk_path = upload_root / str(chunk_number)
    with open(chunk_path, "wb") as fp:
        fp.write(content_bytes)
    return str(chunk_path)
