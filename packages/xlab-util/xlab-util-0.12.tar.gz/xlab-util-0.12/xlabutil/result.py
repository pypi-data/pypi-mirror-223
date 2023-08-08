import base64

from PIL import Image
from io import BytesIO
from dataclasses import dataclass, field
from typing import Optional, List, Union

import numpy as np

from .util import array_to_base64


@dataclass
class Visual():

    # visualization
    visualization: Optional[str] = field(default_factory=lambda: "")

    def set_visual(self, input: Union[np.ndarray, Image.Image], format: str="jpeg"):
        """设置可视化结果"""
        if isinstance(input, np.ndarray):
            visual = array_to_base64(input, format=format)
        elif isinstance(input, Image.Image):
            img_byte = BytesIO()
            input.save(img_byte, format="jpeg")
            visual = base64.b64encode(img_byte.getvalue()).decode('utf-8')
        else:
            visual = input if isinstance(input, str) else None

        self.visualization = visual


@dataclass
class ClassificationResult:
    """The result of image classification."""
    # The predicted label (category index)
    label: int
    # The confidence score of the prediction
    score: Optional[float]
    # The predicted category name
    category: Optional[str]
    # The scores of all categories
    full_scores: Optional[np.ndarray]



@dataclass
class InstanceMask:
    """The dataclass of the instance segmentation mask."""
    size: List[int]  # The size of the mask
    counts: str  # The RLE-encoded mask


@dataclass
class InstancePose:
    """The dataclass of the pose (keypoint) information of an object."""
    keypoints: List[List[float]] = field(default_factory=lambda: [])  # The coordinates of all keypoints
    keypoint_scores: Optional[List[float]] = field(default_factory=lambda: [])  # The scores of all keypoints


@dataclass
class DetectionResult:
    """The result of object detection."""
    # The bounding boxes of all detected objects
    bboxes: Optional[List[List[int]]]
    # The labels of all detected objects
    labels: Optional[List[int]]
    # The scores of all detected objects
    scores: Optional[List[float]]
    # The segmentation masks of all detected objects
    masks: Optional[List[InstanceMask]]
    # The pose estimation results of all detected objects
    poses: Optional[List[InstancePose]]
    # visualization
    visualization: Optional[str]


@dataclass
class PoseEstimationResult(Visual):
    """The result of object detection."""
    # The bounding boxes of all detected objects
    bboxes: Optional[List[List[int]]] = field(default_factory=lambda: [])
    # The scores of all detected objects
    scores: Optional[List[float]] = field(default_factory=lambda: [])
    # The pose estimation results of all detected objects
    poses: Optional[List[InstancePose]] = field(default_factory=lambda: [])


    def set_pred(self, bbox, score, keypoints, keypoint_scores):
        """设置预测结果"""
        self.bboxes.append(bbox)
        self.scores.append(score)
        self.poses.append(InstancePose(keypoints, keypoint_scores))