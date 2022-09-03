from typing import Optional
from fastapi import FastAPI, APIRouter
from nahat_std.schemas.schema import QrCodeModel
from nahat_server.core.qr_image_generator import QrImageGenerator
from nahat_std.logger import logger


class NahatServer:
    def __init__(self):
        self.logger = logger
        self.__current_qr_code: Optional[str] = None
        self.qr_generator = QrImageGenerator(logger=self.logger)
        self.router = APIRouter()
        self.router.add_api_route("/qr_code", self.update_qr_code, methods=["POST"])
        self.router.add_api_route("/qr_validated", self.validated_qr_code, methods=["GET"])

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
    def validated_qr_code(self):
        self.logger.info("Notifying frontend")
        return {"Qr Code Validated": "should present UI approve button"}

    def update_qr_code(self, qr_code: QrCodeModel):
        self.handle_update_qr_code_req(qr_code.code)
        return {"updated_qr_code", self.current_qr_code}


server = NahatServer()
app = FastAPI()
app.include_router(server.router)
