from pathlib import Path
from typing import Union

from PIL import Image, ImageDraw, ImageFont
import qrcode

from certifications.config import (
    COURSE_AVATAR, CERT_FONT, CERT_IMAGE, CERTS_FOLDER, DOMAIN,
    STATIC_PATH,
)

def get_qr_generator():
    return qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=2
    )


def load_image(image: Union[str, Path], scale: Union[int, float]):
    avatar = Image.open(image)
    width, height = int(avatar.width * scale), int(avatar.height * scale)
    return avatar.resize((width, height))


def get_certificate_path(user_url):
    return (CERTS_FOLDER / user_url).with_suffix('.png')


def get_user_qr(user_url: str) -> str:
    avatar = load_image(COURSE_AVATAR, scale=0.66)

    qr = get_qr_generator()
    qr.add_data(f"https://{DOMAIN}/{user_url}")
    qr.make()
    qr_img = qr.make_image(fill_color='gray').convert('RGB')

    pos = (
        (qr_img.size[0] - avatar.size[0]) // 2,
        (qr_img.size[1] - avatar.size[1]) // 2,
    )
    qr_img.paste(avatar, pos)
    width, height = (qr_img.width // 2, qr_img.height // 2)
    return qr_img.resize((width, height))


def create_certificate(name: str, user_url: str) -> None:
    img = Image.open(CERT_IMAGE)
    draw = ImageDraw.Draw(img)
    font_size = 72
    font = ImageFont.truetype(str(CERT_FONT), font_size)
    draw.text(((1200 - 250) // 2, 585), name, (0, 0, 0), font=font)
    qr = get_user_qr(user_url)
    img.paste(qr, (374, 740))
    img.save(get_certificate_path(user_url))


def get_certification_url(user: 'User') -> str:
    certification_path = get_certificate_path(user.url)
    if not certification_path.exists():
        create_certificate(user.fullname, user.url)
    return certification_path.relative_to(STATIC_PATH)
