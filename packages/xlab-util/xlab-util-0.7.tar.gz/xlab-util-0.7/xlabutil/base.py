from abc import ABCMeta, abstractmethod
from PIL import Image


ImageType = Image.Image


class CustomInferencer(metaclass=ABCMeta):

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """This method must be implemented in the child class to define the
        inference process."""
        pass


class SemSegInferencer():
    def __call__(self, img: ImageType) -> ImageType:
        pass