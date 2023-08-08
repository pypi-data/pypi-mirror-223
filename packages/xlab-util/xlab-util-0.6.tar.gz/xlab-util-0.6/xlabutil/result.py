import numpy as np

from dataclasses import dataclass
from typing import Optional, List


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
    # visualization
    visualization: Optional[str]


@dataclass
class InstanceMask:
    """The dataclass of the instance segmentation mask."""
    size: List[int]  # The size of the mask
    counts: str  # The RLE-encoded mask


@dataclass
class InstancePose:
    """The dataclass of the pose (keypoint) information of an object."""
    keypoints: List[List[float]]  # The coordinates of all keypoints
    keypoint_scores: Optional[List[float]]  # The scores of all keypoints


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
class PoseEstimationResult:
    """The result of object detection."""
    # The bounding boxes of all detected objects
    bboxes: Optional[List[List[int]]]
    # The scores of all detected objects
    scores: Optional[List[float]]
    # The pose estimation results of all detected objects
    poses: Optional[List[InstancePose]]
    # visualization
    visualization: Optional[str]