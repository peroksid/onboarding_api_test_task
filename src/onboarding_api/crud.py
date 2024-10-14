def create_upload(pool, session_token, name, mime, size, hash) -> int:
    with pool.connection() as conn, conn.cursor() as cursor:
        cursor.execute(
            """
            insert into uploads 
            (session_token, name, mime, size, hash, created_at)
            values 
            (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            returning id
            """,
            [session_token, name, mime, size, hash],
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
            insert into chunks
            (upload_id, number, path)
            values
            (%s, %s, %s)
            returning id
            """,
            [upload_id, chunk_number, path],
        )
        conn.commit()
        return cursor.fetchone()[0]
