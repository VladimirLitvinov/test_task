from fastapi import FastAPI
from api_v1 import router
from api_v1.exceptions import custom_api_exception_handler, CustomApiException

app = FastAPI()

app.include_router(router)
app.add_exception_handler(CustomApiException, custom_api_exception_handler)