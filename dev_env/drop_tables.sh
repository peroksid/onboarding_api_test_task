#!/bin/bash
psql -h localhost -p 5432 -U postgres -d onboarding_api < db_migrations/drop_tables.sql