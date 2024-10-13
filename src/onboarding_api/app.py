from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from importlib_resources import files


app = FastAPI()


@app.get('/', response_class=HTMLResponse)
def get_example_simple_client():
    return files('onboarding_api.example_simple_client').joinpath('index.html').read_text()


