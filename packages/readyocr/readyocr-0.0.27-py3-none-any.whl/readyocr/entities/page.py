import os
from PIL import Image

from readyocr.entities.bbox import SpatialObject
from readyocr.entities.entity_list import EntityList


class Page(SpatialObject):
    """ 
    Creates a new document, ideally representing a single item in the dataset.
    
    :param page_number: Page number in the document linked to this Page object
    :type page_number: int
    :param width: Width of page, in pixels
    :type width: float
    :param height: Height of page, in pixels
    :type height: float
    :param children: Child entities in the Page
    :type children: List
    """

    def __init__(
        self,
        page_number: int,
        width: int,
        height: int,
        image: Image=None,
    ):
        self.page_number = page_number
        super().__init__(width=width, height=height)
        self.metadata = {}
        self.image = image
        self._children = EntityList()

    @property
    def children(self) -> EntityList:
        """
        :return: Returns all the objects present in the Page.
        :rtype: EntityList
        """
        assert self not in self._children, "Recursive children is not allow"
        return self._children
    
    @children.setter
    def children(self, children: EntityList):
        """
        :param children: List of child entities in the Page.
        :type children: EntityList
        """
        self._children = children

    @property
    def descendants(self):
        """
        :return: Returns all the children of the entity.
        :rtype: list
        """
        descendants = []
        for x in self.children:
            if len(x.descendants) > 0:
                descendants.extend(x.descendants)
        descendants.extend(self.children)
        # remove mutual descendants
        descendants = list(set(descendants))
        assert self not in descendants, "Recursive descendants is not allow"

        return EntityList(descendants)
    
    def find_parent_by_child_id(self, child_id: str) -> EntityList:
        """
        Find the parent of a child entity by its ID.

        :param child_id: ID of the child entity.
        :type child_id: str
        :return: Returns the parent entity of the child entity.
        :rtype: EntityList
        """
        parents = []
        for desc in self.descendants:
            child_ids = [x.id for x in desc.children]
            if child_id in child_ids:
                parents.append(desc)
        # remove mutual parents
        parents = list(set(parents))
        return EntityList(parents)
    
    def __repr__(self):
        return os.linesep.join([
            f"Page(page_number: {self.page_number}, width: {self.width}, height: {self.height})",
            f"Children - {len(self.children)}"
        ])
    
    def export_json(self):
        return {
            "pageNumber": self.page_number,
            "dimension": {
                "width": self.width,
                "height": self.height
            },
            "entities": [x.export_json() for x in self.descendants]
        }