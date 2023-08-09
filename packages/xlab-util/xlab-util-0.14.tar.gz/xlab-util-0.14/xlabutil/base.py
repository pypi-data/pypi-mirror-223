import json

from abc import ABCMeta, abstractmethod
from PIL import Image

import numpy as np


ImageType = Image.Image


class NumpyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.float32):
            return float(obj)
        return super().default(obj)


class CustomInferencer(metaclass=ABCMeta):

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """This method must be implemented in the child class to define the
        inference process."""
        pass


class SemSegInferencer():
    def __call__(self, img: ImageType) -> ImageType:
        pass