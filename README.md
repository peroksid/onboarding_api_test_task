Onboarding API
===

Implemented only the API to upload in chunks:
1) client sends POST to /uploads/ with JSON of upload parameters. Response contains session tioken.
2) client sends POST to /uploads/<upload_id>/chunk for every chunk; sends X-Session-Token header with each response; last one supposed to kick encoding in background. Chunks are store in /tmp/
