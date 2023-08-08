import base64
import json
import dataclasses

from PIL import Image
from io import BytesIO
from dataclasses import _is_dataclass_instance

import numpy as np

from .base import NumpyJSONEncoder


def save_image_base64(base64_str: str, img_path: str=None):
    """保存base64为图片"""
    img_bytes = base64.b64decode(base64_str)
    img_bytes = BytesIO(img_bytes)
    img = Image.open(img_bytes)
    if img_path:
        img.save(img_path)

    return img


def img_to_array(img: Image.Image):
    """图片转ndarray"""
    return np.asarray(img)


def array_to_base64(array: np.ndarray, format: str="jpeg"):
    """ndarray转为图片（base64）"""
    img_byte = BytesIO()
    img = Image.fromarray(array)
    img.save(img_byte, format=format)

    return base64.b64encode(img_byte.getvalue()).decode('utf-8')


def array_to_img(img_array) -> Image.Image:
    """ndarray转为图片"""
    return Image.fromarray(img_array.astype(np.uint8))


def to_json(array):
    if _is_dataclass_instance(array):
        array = dataclasses.asdict(array)

    return json.dumps(array, cls=NumpyJSONEncoder)
