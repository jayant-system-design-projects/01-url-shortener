from fastapi import FastAPI
from app.middleware.request_middleware import request_middleware
from app.routers.shorten_url_routers import shorten_url_router


def create_app(debug: bool = True) -> FastAPI:
    app = FastAPI(
        title="URL Shortening App",
        description="""
        This is url shortening fast api application.
        This is awesome application which will help you to shorten your long url
        make ease to use it.

        # Shorten URL

        ## Create Shorten URL
        
        You can shorten long url.

        ## Use Shorten URL

        You can use shorten url to redirect to long url.
        """,
        # root_path="myUrlShortener/v1/",
        debug=debug,
    )
    app.middleware("http")(request_middleware)
    app.include_router(shorten_url_router)
    return app


app = create_app()
