import qrcode
from io import BytesIO

def get_qr(content:str)->bytes:
    try:
        qr=qrcode.make(data=content,version=1)
        with BytesIO() as bio:
            qr.save(bio)
            qr_bytes = bio.getvalue()
        return qr_bytes
    except Exception as e:
        raise Exception(str(e))