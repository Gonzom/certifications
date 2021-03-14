from datetime import datetime
from pathlib import Path
from typing import Union

from PIL import Image, ImageDraw, ImageFont
import qrcode

from certifications.config import (
    COURSE_AVATAR,
    CERT_FONT,
    CERT_IMAGE,
    CERTS_FOLDER,
    DOMAIN,
    STATIC_PATH,
)


NAME_LINE_WIDTH = 935
NAME_LINE_START = 265
NAME_LINE_HEIGHT = 585
QR_POSITION = (374, 740)
DATE_POSITION = (100, 80)

NAME_FONT_SIZE = 72
DATE_FONT_SIZE = 32


def get_qr_generator():
    return qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=2,
    )


def load_image(image: Union[str, Path], scale: Union[int, float]):
    avatar = Image.open(image)
    width, height = int(avatar.width * scale), int(avatar.height * scale)
    return avatar.resize((width, height))


def get_users_certificate_path(user_url: str) -> Path:
    return (CERTS_FOLDER / user_url).with_suffix(".png")


def get_user_qr(user_url: str) -> str:
    avatar = load_image(COURSE_AVATAR, scale=0.66)

    qr = get_qr_generator()
    qr.add_data(f"https://{DOMAIN}/{user_url}")
    qr.make()
    qr_img = qr.make_image(fill_color="gray").convert("RGB")

    pos = (
        (qr_img.size[0] - avatar.size[0]) // 2,
        (qr_img.size[1] - avatar.size[1]) // 2,
    )
    qr_img.paste(avatar, pos)
    width, height = (qr_img.width // 2, qr_img.height // 2)
    return qr_img.resize((width, height))


def draw_name_on_certificate(painter, name: str) -> None:
    font = ImageFont.truetype(str(CERT_FONT), NAME_FONT_SIZE)
    text_w, _ = painter.textsize(name, font=font)
    name_x_column = (NAME_LINE_WIDTH - text_w) // 2 + NAME_LINE_START
    position_of_name = (name_x_column, NAME_LINE_HEIGHT)
    painter.text(position_of_name, name, (0, 0, 0), font=font)


def draw_date_on_certificate(painter, date: int) -> None:
    font = ImageFont.truetype(str(CERT_FONT), DATE_FONT_SIZE)
    text = datetime.fromtimestamp(date).strftime("%Y/%m/%d")
    painter.text(DATE_POSITION, text, (0, 0, 0), font=font)


def create_certificate(name: str, date: int, user_url: str) -> None:
    img = Image.open(CERT_IMAGE)
    draw = ImageDraw.Draw(img)
    qr = get_user_qr(user_url)
    draw_name_on_certificate(painter=draw, name="ל" + name)
    draw_date_on_certificate(painter=draw, date=date)
    img.paste(qr, QR_POSITION)
    img.save(get_users_certificate_path(user_url))


def get_certification_path(user: "User") -> Path:
    certification_path = get_users_certificate_path(user.url)
    if not certification_path.exists():
        create_certificate(user.fullname, user.issue_date, user.url)
    return certification_path.relative_to(STATIC_PATH)


def get_certification_url(user: "User") -> str:
    return str(get_certification_path(user)).replace("\\", "/")
