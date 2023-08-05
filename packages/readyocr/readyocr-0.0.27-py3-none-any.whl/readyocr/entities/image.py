import numpy as np
from PIL import Image

from readyocr.entities.bbox import BoundingBox
from readyocr.entities.page_entity import PageEntity


class Image(PageEntity):
    """
    To create a new :class:`Image` object we need the following

    :param id: Unique identifier of the TextBox entity.
    :type id: str
    :param bbox: Bounding box of the TextBox entity.
    :type bbox: BoundingBox
    :param image: Image of the TextBox entity.
    :type image: Image
    """

    def __init__(   
        self,
        id: str,
        bbox: BoundingBox,
        confidence: float=0,
        image: Image=None,
        metadata: dict=None,
    ):
        super().__init__(id, bbox, metadata)
        self.confidence = confidence
        self.image = image