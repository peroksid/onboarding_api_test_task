CREATE TABLE uploads(
    id bigserial PRIMARY KEY,
    session_token uuid,
    name character varying,
    mime character varying,
    hash character (64),
    size int,
    created_at timestamp with time zone
);