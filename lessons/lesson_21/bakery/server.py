import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from logic import calculate_buns_to_bake
from sanic import HTTPResponse, Request, Sanic, json

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

app = Sanic('bakery_app')

ingredients_host = os.environ.get('ingredients_host')
ingredients_api = os.environ.get('ingredients_api')


@app.get('/bakery')
async def calculate_buns(request: Request) -> HTTPResponse:
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{ingredients_host}{ingredients_api}')
        if response.status_code != 200:
            return json({'errors': response.content})

        return json({'buns_to_bake': calculate_buns_to_bake(response.json())})
