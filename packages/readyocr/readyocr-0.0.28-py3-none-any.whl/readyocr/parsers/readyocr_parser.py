from typing import Dict
from readyocr.entities import (
    BoundingBox, 
    Word, 
    Line, 
    Paragraph, 
    Block, 
    Table, 
    Cell, 
    MergedCell, 
    Key, 
    Value, 
    Page, 
    Document, 
    Character,
    Image,
    Figure,
    Field,
    LineItem,
    LineItemGroup,
    Invoice
)
from readyocr.entities.entity_list import EntityList


def _create_object(entity_json):
    """_summary_

    :param entity_json: entity information json format
    :type entity_json: json
    """
    bbox = BoundingBox(entity_json['boundingBox']['x'], entity_json['boundingBox']['y'],
                       entity_json['boundingBox']['width'], entity_json['boundingBox']['height'])
    if entity_json['class'] == 'Table':
        entity = Table(id=entity_json['id'],
                       bbox=bbox,
                       confidence=1.0)
    elif entity_json['class'] == 'Cell':
        entity = Cell(id=entity_json['id'],
                      bbox=bbox,
                      row_index=entity_json['rowIndex'],
                      col_index=entity_json['columnIndex'],
                      text=entity_json['text'],
                      confidence=entity_json['confidence'])
    elif entity_json['class'] == 'MergedCell':
        entity = MergedCell(id=entity_json['id'],
                            bbox=bbox,
                            row_index=entity_json['rowIndex'],
                            col_index=entity_json['columnIndex'],
                            row_span=entity_json['rowSpan'],
                            col_span=entity_json['columnSpan'],
                            text=entity_json['text'],
                            confidence=entity_json['confidence'])
    elif entity_json['class'] in ('Word', 'Line', 'Key', 'Value', 'Character', 'Paragraph', 'Block'):
        entity = eval(entity_json['class'])(id=entity_json['id'],
                                            bbox=bbox,
                                            text=entity_json['text'],
                                            confidence=entity_json['confidence'])
    elif entity_json['class'] in ('Image', 'Figure'):
        entity = eval(entity_json['class'])(id=entity_json['id'],
                                            bbox=bbox,
                                            confidence=entity_json['confidence'])
    elif entity_json['class'] == 'Field':
        entity = Field(
            id=entity_json['id'],
            bbox=bbox,
            text=entity_json['text'],
            confidence=entity_json['confidence'],
            type=entity_json['type'],
            page_number=entity_json['pageNumber']
        )
    else:
        entity = None
    return entity


def _parse_invoice(invoice_json):
    page_numbers = invoice_json.get('pageNumbers')
    fields_json = invoice_json.get('fields')
    line_item_groups_json = invoice_json.get('lineItemGroups')

    fields = []
    for field_json in fields_json:
        field = _create_object(field_json)
        fields.append(field)

    line_item_groups = []
    for line_item_group_json in line_item_groups_json:
        line_item_group = []
        for line_item_json in line_item_group_json.get('LineItems'):
            for item_json in line_item_json:
                item = _create_object(item_json)
                line_item_group.append(item)
        line_item_groups.append(line_item_group)

    return Invoice(
        fields=fields,
        line_item_groups=line_item_groups,
        page_numbers=page_numbers,
    )
        

def load(response: Dict) -> Document:
    """
    Convert ReadyOCR json to ReadyOCR document

    :param response: json response from readyocr
    :type response: Dict
    :return: ReadyOCR document
    :rtype: Document
    """
    document = Document()
    for page_json in response['document']['pages']:
        # initialize page object
        page = Page(page_number=page_json['pageNumber'],
                    width=page_json['dimension']['width'],
                    height=page_json['dimension']['height'])
        # add entity into page
        for entity_json in page_json['entities']:
            entity = _create_object(entity_json=entity_json)
            if entity is not None:
                page.children.add(entity)
        # linking entities
        for entity_json in page_json['entities']:
            parent_entity = page.children.get_by_id(entity_json['id'])
            for child_id in entity_json['childrenIds']:
                child_entity = page.children.get_by_id(child_id)
                parent_entity.add(child_entity)
        # add more things into page
        document.add(page)

    invoices_json = response.get('document').get('invoices')
    if invoices_json is not None:
        for invoice_json in invoices_json:
            invoice = _parse_invoice(invoice_json)

            document.invoices.append(invoice)
    
    return document