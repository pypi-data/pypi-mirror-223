import json

from io import BytesIO
from PIL import Image
from typing import Union, Any

from openxlab.model import Inference
from openxlab.model.clients.modelapi_client import Result 
from .type import ImageType


class InferenceResult():
    
    def __init__(self, raw_result: Result) -> None:
        self._raw_result = raw_result
        self._content_type = self._raw_result.content_type
        self._content = self._raw_result.original


    def save(self, save_path: str) -> Union[Image.Image, Any]:
        with open(save_path, 'wb') as file:
            file.write(self._content)

    
    def image(self) -> Image.Image:
        if self._content_type.startswith("image"):
            return Image.open(BytesIO(self._content))

    
    def pred(self) -> Any:
        if self._content_type == "application/json":
            return json.loads(self._content)


class InstanceSegInference(Inference, InferenceResult):

    def __init__(self, model_repo):
        super().__init__(model_repo)


    def __call__(self, img: ImageType, 
                       return_visualization: bool=False, 
                       **kwargs) -> InferenceResult:
        if return_visualization:
            kwargs["return_visualization"] = True

        result = super().inference([img], **kwargs)

        return InferenceResult(result)


class RemoteInference():

    def from_remote(model_repo: str, 
                    task_type: str="instance-seg"):
        if "instance-seg" == task_type:
            return InstanceSegInference(model_repo)
        
        


