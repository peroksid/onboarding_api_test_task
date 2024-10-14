cat dev_env/pgpass_line > ~/.pgpass
chmod go-rwx ~/.pgpass
docker compose up
visit adminer on localhost:8080 to create the db onboarding_api
psql -h localhost -p 5432 -U postgres -d onboarding_api < db_migrations/create_tables.sql