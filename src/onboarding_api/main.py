import os
import uvicorn


os.environ["UVICORN_APP"] = "onboarding_api.app:app"


uvicorn.main()
