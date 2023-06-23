# Import pyqrcode
import pyqrcode
from models.models import URL,QR
from sqlalchemy.orm import Session
from security.error import not_found


# Function to create a QR code using original URL
def original_url_qr_code(original_url:str,db:Session):
    # check if the URL exist and active
    url_exist = db.query(URL).filter(URL.original_url == original_url,URL.is_active).first()
    url_id = url_exist.id
    if url_exist:
        # check if qr code already exist
        qr_exist = db.query(QR).filter(QR.url_id==url_id).first()
        if qr_exist:
            return qr_exist
        else:
            # Generate QR code
            qr_code = pyqrcode.create(original_url)
            image = qr_code.png("image.png",scale=8)
            qr_image = QR (
                image = image.read(),
                url_id = url_id
            )
            db.add(qr_image)
            db.commit()
            db.refresh(qr_image)
            return qr_image
    else:
        not_found(message=f"URL:{original_url} doesn't exist")

    
# Function to create a QR code using short URL
def short_url_qr_code(short_url:str,db:Session):
    # check if the URL exist and active
    url_exist = db.query(URL).filter(URL.short_url == short_url,URL.is_active).first()
    url_id = url_exist.id
    if url_exist:
        # check if qr code already exist
        qr_exist = db.query(QR).filter(QR.url_id==url_id).first()
        if qr_exist:
            return qr_exist
        else:
            # Generate QR code
            qr_code = pyqrcode.create(short_url)
            image = qr_code.png("image.png",scale=8)
            qr_image = QR (
                image = image.read(),
                url_id = url_id
            )
            db.add(qr_image)
            db.commit()
            db.refresh(qr_image)
            return qr_image
    else:
        not_found(message=f"URL:{short_url} doesn't exist")
    
# Function to create a QR code using custom URL
def custom_url_qr_code(custom_url:str,db:Session):
    # check if the URL exist and active
    url_exist = db.query(URL).filter(URL.custom_url == custom_url,URL.is_active).first()
    url_id = url_exist.id
    if url_exist:
        # check if qr code already exist
        qr_exist = db.query(QR).filter(QR.url_id==url_id).first()
        if qr_exist:
            return qr_exist
        else:
            # Generate QR code
            qr_code = pyqrcode.create(custom_url)
            image = qr_code.png("image.png",scale=8)
            qr_image = QR (
                image = image.read(),
                url_id = url_id
            )
            db.add(qr_image)
            db.commit()
            db.refresh(qr_image)
            return qr_image
    else:
        not_found(message=f"URL:{custom_url} doesn't exist")