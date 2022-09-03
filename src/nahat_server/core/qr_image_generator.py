from qrcode import QRCode


class QrImageGenerator:
    def __init__(self, logger):
        self.logger = logger
        self.qr_code = QRCode(version=1, box_size=10, border=5)
        self.img = None

    def generate_qr_image(self, code: str, path: str):
        self.qr_code.add_data(code)
        self.qr_code.make(fit=True)
        img = self.qr_code.make_image()
        img.save(path)

