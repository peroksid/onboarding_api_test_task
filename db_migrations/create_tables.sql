CREATE TABLE uploads(
    id bigserial PRIMARY KEY,
    session_token uuid,
    name character varying,
    mime character varying,
    hash character (64),
    size int,
    expected_chunk_count integer,
    complete_chunk_count integer default 0,
    created_at timestamp with time zone
);

CREATE TABLE chunks(
    id bigserial PRIMARY KEY,
    upload_id bigint,
    number bigint,
    path character varying
);