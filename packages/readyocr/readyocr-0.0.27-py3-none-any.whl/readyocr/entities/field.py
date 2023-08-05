import os
from typing import List
from readyocr.entities.bbox import BoundingBox
from readyocr.entities.page_entity import PageEntity


class Field(PageEntity):
    
    def __init__(
            self,
            id,
            bbox: BoundingBox,
            type: str,
            text: str,
            confidence: float,
            page_number: int,
            metadata: dict=None
        ):
        """
        Invoice Field

        :param bbox: Bounding box of the field
        :type bbox: BoundingBox
        :param type: Type of the field
        :type type: str
        :param text: Normalized text text of the field
        :type text: str
        :param confidence: Confidence of the field
        :type confidence: float
        :param page_number: Page number of the field
        :type page_number: int
        :param metadata: Metadata of the field, defaults to None
        :type metadata: dict, optional
        """
        super().__init__(id, bbox, metadata)
        self.type = type
        self.text = text
        self.confidence = confidence
        self.page_number = page_number

    def __repr__(self):
        return os.linesep.join([
            f"Field(id: {self.id}, bbox: {self.bbox}, type: {self.type}, text: {self.text}, confidence: {self.confidence}, page_number: {self.page_number})",
            f"Field Children: {len(self.children)}"
        ])
    
    def export_json(self):
        """
        :return: Returns the json representation of the textbox
        :rtype: dict
        """
        response = super().export_json()
        response["type"] = self.type
        response["text"] = self.text
        response["confidence"] = self.confidence
        response["pageNumber"] = self.page_number

        return response


class LineItem():

    def __init__(
        self,
        fields: List[Field] = None
    ):
        """
        LineItem belong to LineItemGroup, and contains Field

        :param fields: Fields in the line item row, defaults to None
        :type fields: List[Field], optional
        """
        if fields is None:
            fields = []
        self.__set__(fields)

    def _check_duplicate(self, fields: List[Field]):
        field_types = set()
        for field in fields:
            if field.type in field_types:
                raise ValueError(f"duplicate field type {field.type} in line item row")
            field_types.add(field.type)

    def __set__(self, fields: List[Field]):
        self._check_duplicate(fields)
        self._fields = fields

    def __getitem__(self, index):
        if isinstance(index, int):
            return self._fields[index]
        else:
            for field in self._fields:
                if field.type == index:
                    return field
            raise IndexError(f"{index} is not present in this line item row")
        
    def __len__(self):
        return len(self._fields)
    
    def __iter__(self):
        return iter(self._fields)

    def __repr__(self):
        return f"LineItem(fields: {self._fields})"
    
    def get(self, index):
        try:
            return self.__getitem__(index)
        except IndexError:
            return None

    def export_json(self):
        return [x.export_json() for x in self._fields]


class LineItemGroup():

    def __init__(
            self,
            line_item_rows: List[LineItem]
        ):
        """
        LineItemGroup contains LineItem

        :param line_item_rows: line item rows in the line item group
        :type line_item_rows: List[LineItem]
        """
        self._line_item_rows = line_item_rows

    def __getitem__(self, index):
        return self._line_item_rows[index]

    def __len__(self):
        return len(self._line_item_rows)

    def __iter__(self):
        return iter(self._line_item_rows)

    def __repr__(self):
        return os.linesep.join([str(x) for x in self._line_item_rows])

    def export_json(self):
        return {
            "LineItems": [x.export_json() for x in self._line_item_rows]
        }
