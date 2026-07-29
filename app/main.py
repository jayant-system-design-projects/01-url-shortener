from typing import AsyncContextManager
from fastapi import FastAPI
from app.config import Config
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.schedulers.redis_prune_schedule import _redis_prune_schedule_task
from app.middleware.request_middleware import request_middleware
from app.routers.shorten_url_routers import shorten_url_router
from app.global_exception_handler import setup_global_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Run FastAPI lifespan tasks.

    Parameters
    ----------
    app : FastAPI
        The FastAPI application instance.

    Yields
    ------
    None
        Control back to FastAPI while the app is running.
    """
    try:
        scheduler = AsyncIOScheduler()

        scheduler.add_job(
            _redis_prune_schedule_task,
            "interval",
            seconds=Config.REDIS_UNPOPULAR_URL_PRUNE_TASK_TIME_IN_SECONDS,
        )

        scheduler.start()

        print("Scheduler started.")
        yield
    except Exception as e:
        print(f"An error occurred during app lifecycle: {e}")
        raise
    finally:
        scheduler.shutdown()
        print("Scheduler ")


def create_app(
    lifespan: AsyncContextManager,
    debug: bool = True,
) -> FastAPI:
    """
    Create the FastAPI application.

    Parameters
    ----------
    lifespan : AsyncContextManager
        The FastAPI lifespan context manager.
    debug : bool, optional
        Whether the app should run in debug mode.

    Returns
    -------
    FastAPI
        The configured FastAPI application.
    """
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
        lifespan=lifespan,
        # root_path="myUrlShortener/v1/",
        debug=debug,
    )
    app.middleware("http")(request_middleware)
    setup_global_exception_handlers(app)
    app.include_router(shorten_url_router)
    return app


app = create_app(lifespan=lifespan)
