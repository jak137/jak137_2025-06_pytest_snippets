from dataclasses import dataclass

from fastapi import FastAPI

from hello_world import cor_1


@dataclass(frozen=True, kw_only=True)
class HelloWorldResponse:
    payload: str


def make_app() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    async def read_root() -> HelloWorldResponse:
        return HelloWorldResponse(payload=await cor_1())

    return app
