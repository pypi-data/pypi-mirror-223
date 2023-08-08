import base64

from PIL import Image
from io import BytesIO

import numpy as np


def save_base64(base64_str: str, img_path: str):
    """保存base64为图片"""
    img_bytes = base64.b64decode(base64_str)
    img_bytes = BytesIO(img_bytes)
    Image.open(img_bytes).save(img_path)


def img_to_array(img: Image.Image):
    """图片转ndarray"""
    return np.asarray(img)


def array_to_base64(img_array):
    """ndarray转为图片（base64）"""
    img_byte = BytesIO()
    img = Image.fromarray(img_array)
    img.save(img_byte, format="jpeg")

    return base64.b64encode(img_byte.getvalue()).decode('utf-8')


def array_to_img(img_array) -> Image.Image:
    """ndarray转为图片"""
    return Image.fromarray(img_array.astype(np.uint8))
