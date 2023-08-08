from readyocr.entities.bbox import BoundingBox
from readyocr.entities.page_entity import PageEntity


class Figure(PageEntity):
    """
    To create a new :class:`Figure` object we need the following

    :param id: Unique identifier of the TextBox entity.
    :type id: str
    :param bbox: Bounding box of the TextBox entity.
    :type bbox: BoundingBox
    """

    def __init__(   
        self,
        id: str,
        bbox: BoundingBox,
        confidence: float=0,
    ):
        super().__init__(id, bbox)
        self.confidence = confidence