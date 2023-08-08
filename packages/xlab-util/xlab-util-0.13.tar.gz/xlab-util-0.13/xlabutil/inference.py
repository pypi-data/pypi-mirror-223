import json

from io import BytesIO
from PIL import Image
from typing import Union, List, Any

from openxlab.model import Inference
from openxlab.model.clients.modelapi_client import Result 

from .type import ImageType
from .result import PoseEstimationResult, OCRResult
from .util import save_image_base64


class Input():

    @staticmethod
    def input(img_path: str) -> Image.Image:
        return Image.open(img_path).convert("RGB")


class Output():
    
    def __init__(self, content, content_type: str="application/json") -> None:
        self._content_type = content_type
        self._content = content

    
    def result(self, save_path: str=None) -> Union[Image.Image, Any]:
        if self._content_type == "application/json":
            return self._content

        if self._content_type.startswith("image"):
            img = Image.open(BytesIO(self._content))
            if save_path:
                img.save(save_path)

            return img

    def visual(self, img_path: str=None) -> Image.Image:
        visual = self.__getattribute__('visualization')
        if visual:
            return save_image_base64(visual, img_path)


    @property
    def metric(self):
        """返回推理指标"""
        return self._result_attribute

    
    def __getattribute__(self, __name: str) -> Any:
        """支持根据属性名称，查询预测结果"""
        try:
            return object.__getattribute__(self, __name)
        except AttributeError as err:
            if __name in self._result_attribute:
                pred_json = self.result()
                if pred_json and __name in pred_json.keys():
                    return pred_json[__name]
            
            raise err


class PoseEstimationOutput(Output, PoseEstimationResult):

    def __init__(self, raw_result: Result) -> None:
        super().__init__(raw_result)

        self._result_attribute = list(PoseEstimationResult.__dataclass_fields__.keys())


class InstanceSegInference(Inference, Input):

    def __init__(self, model_repo):
        super().__init__(model_repo)


    def __call__(self, img: ImageType, 
                       return_visualization: bool=False, 
                       **kwargs) -> Output:
        if return_visualization:
            kwargs["return_visualization"] = True

        result = super().inference([img], **kwargs)

        return Output(result.original, result.content_type)


class PoseEstimationInference(Inference, Input):

    def __init__(self, model_repo):
        super().__init__(model_repo)


    def __call__(self, img: ImageType, 
                       return_visualization: bool=False, 
                       **kwargs) -> List[PoseEstimationOutput]:
        if return_visualization:
            kwargs["return_visualization"] = True

        result = super().inference([img], **kwargs)

        result = json.loads(result.original)
        if isinstance(result, list):
            return [ PoseEstimationOutput(item) for item in result ]

        return [ PoseEstimationOutput(result) ]


class OCRInference(Inference, Input):

    def __init__(self, model_repo):
        super().__init__(model_repo)


    def __call__(self, img: ImageType, 
                       return_visualization: bool=False, 
                       **kwargs) -> List[OCRResult]:
        if return_visualization:
            kwargs["return_visualization"] = True

        result = super().inference([img], **kwargs)

        result = json.loads(result.original)
        if isinstance(result, list):
            return [ OCRResult(item) for item in result ]

        return [ OCRResult(result) ]


class RemoteInference():

    def from_remote(model_repo: str, 
                    task_type: str="instance-seg"):
        if "instance-seg" == task_type:
            return InstanceSegInference(model_repo)
        elif "pose-estimation" == task_type:
            return PoseEstimationInference(model_repo)
        
        


