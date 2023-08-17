from sanic import Sanic, Request, HTTPResponse, json

app = Sanic('ingredients_app')


@app.get('/ingredients')
async def get_ingredients(request: Request) -> HTTPResponse:
    return json(
        {
            'meal': 5000
        }
    )
