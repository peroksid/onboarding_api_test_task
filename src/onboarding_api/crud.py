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
