from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.providers import app_provider, exception_handler, logging_provider, route_provider
from config.config import DevelopmentSettings, ProductionSettings, get_settings
from fastapi.openapi.docs import get_swagger_ui_html
from loguru import logger
import app.http.middleware as middleware


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="/static/fastapi/swagger-ui@5.17.14/swagger-ui-bundle.js",
        swagger_css_url="/static/fastapi/swagger-ui@5.17.14/swagger-ui.css",
        swagger_favicon_url="/static/fastapi/swagger-ui@5.17.14/favicon-32x32.png",
    )


settings = get_settings()


def register(app: FastAPI, provider, settings: DevelopmentSettings | ProductionSettings):
    provider.register(app, settings)


def boot(app: FastAPI, provider):
    provider.boot(app)


def create_app() -> FastAPI:
    """
    Storing object instances in the app context: https://github.com/fastapi/fastapi/issues/81

    Returns:
        FastAPI: _description_
    """

    app = None
    if settings.ENV == 'development':
        logger.info('Starting dev')
        app = FastAPI(lifespan=app_provider.lifespan)
    else:
        logger.info('Starting prod')
        app = FastAPI(lifespan=app_provider.lifespan, docs_url=None, redoc_url=None)

    register(app, app_provider, settings)
    register(app, logging_provider, settings)
    register(app, exception_handler, settings)
    register(app, middleware, settings)

    app.mount(
        "/static",
        StaticFiles(directory="static"),
        name="static",
    )

    boot(app, route_provider)

    return app
