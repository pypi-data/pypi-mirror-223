from readyocr.entities.bbox import BoundingBox
from readyocr.entities.page_entity import PageEntity


class DrawCurve(PageEntity):
    """
    To create a new :class:`DrawCurve` object we need the following

    :param id: Unique identifier of the DrawCurve entity.
    :type id: str
    :param bbox: Bounding box of the DrawCurve entity.
    :type bbox: BoundingBox
    :param confidence: Confidence of the DrawCurve entity.
    :type confidence: float
    :param metadata: Metadata of the DrawCurve entity.
    :type metadata: dict
    """

    def __init__(
        self,
        id: str,
        bbox: BoundingBox,
        confidence: float=0,
        metadata: dict=None
    ):
        super().__init__(id, bbox, metadata)
        self.confidence = confidence