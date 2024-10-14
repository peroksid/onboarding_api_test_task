from pydantic import BaseModel

from .schemas import InitiateUploadInput


def create_upload(pool, session_token, inp: InitiateUploadInput) -> int:
    with pool.connection() as conn, conn.cursor() as cursor:
        cursor.execute(
            """
            insert into uploads 
            (session_token, name, mime, size, hash, expected_chunk_count, created_at)
            values 
            (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            returning id
            """,
            [
                session_token,
                inp.file_info.name,
                inp.file_info.mime,
                inp.file_info.size,
                inp.file_info.hash,
                inp.chunk_count,
            ],
        )
        conn.commit()
        return cursor.fetchone()[0]


def upload_exists(pool, upload_id: int, session_token: str) -> bool:
    with pool.connection() as conn, conn.cursor() as cursor:
        cursor.execute(
            """
            select count(*)
            from uploads where id = %s and session_token = %s
            """,
            [upload_id, session_token],
        )
        return cursor.fetchone()[0] == 1


class ChunkRow(BaseModel):
    id: int
    upload_id: int
    number: int
    path: str


def list_chunks(pool, upload_id: int):
    with pool.connection() as conn, conn.cursor(row_factory=ChunkRow) as cursor:
        cursor.execute(
            """
            select * from chunks where upload_id = %s order by chunk_number asc
            """,
            [upload_id]
        )
        return cursor.fetchall()


def chunk_exists(pool, upload_id: int, chunk_number: int) -> bool:
    with pool.connection() as conn, conn.cursor() as cursor:
        cursor.execute(
            """
            select count(*)
            from chunks where upload_id = %s and number = %s
            """,
            [upload_id, chunk_number],
        )
        return cursor.fetchone()[0] == 1


def create_chunk(pool, upload_id: int, chunk_number: int, path: str):
    with pool.connection() as conn, conn.cursor() as cursor:
        cursor.execute(
            """
            update uploads set complete_chunk_count = complete_chunk_count + 1 where id = %s returning complete_chunk_count, expected_chunk_count
            """,
            [upload_id],
        )
        complete_chunk_count, expected_chunk_count = cursor.fetchone()[0:2]
        cursor.execute(
            """
            insert into chunks (upload_id, number, path) values (%s, %s, %s) returning id
            """,
            [upload_id, chunk_number, path],
        )
        conn.commit()
        chunk_id = cursor.fetchone()[0]
    return complete_chunk_count, expected_chunk_count, chunk_id
