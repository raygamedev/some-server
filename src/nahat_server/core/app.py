from logging import Logger
from typing import Optional
from fastapi import FastAPI
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from nahat_std.schemas.schema import QrCodeModel
from nahat_server.core.lib.qr_generator import QrGenerator
from nahat_server.core.lib.logger import logger
router = InferringRouter()


@cbv(router)
class Server:
    def __init__(self):
        self.logger = logger
        self.__current_qr_code: Optional[str] = None
        self.qr_generator = QrGenerator(logger=self.logger)

    @property
    def current_qr_code(self):
        return self.__current_qr_code

    @current_qr_code.setter
    def current_qr_code(self, qr_code):
        self.__current_qr_code = qr_code

    def handle_update_qr_code_req(self, qr_code: str):
        self.current_qr_code = qr_code
        self.qr_generator.generate_qr_image(self.current_qr_code, path='/tmp/lol.png')

    """ Endpoints """
    @router.post("/qr_code")
    def update_qr_code(self, qr_code: QrCodeModel):
        self.handle_update_qr_code_req(qr_code.code)
        return {"updated_qr_code", self.current_qr_code}


Server()
app = FastAPI()
app.include_router(router)
