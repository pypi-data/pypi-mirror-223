import os
import pathlib
import io
from uuid import uuid4
from collections.abc import Iterable
from typing import Union

from pypdf import PdfReader, PdfWriter
# from pdf2image import convert_from_bytes
import pdf2image
from pdfminer.high_level import extract_pages
from pdfminer.layout import (
    LTPage,
    LTLine,
    LTRect,
    LTCurve, 
    LTFigure,
    LTImage,
    LTTextLine,
    LTTextBox,
    LTChar,
    LTText
)
from PIL import Image as PILImage

from readyocr.entities import (
    BoundingBox, 
    Character, 
    Line, 
    Block, 
    Image, 
    Figure, 
    Page, 
    Document,
    DrawLine,
    DrawCurve,
    DrawRectangle
)


def _parse_bbox(item, page):
    x=float(item.x0/page.width)
    y=float((page.height - item.y1)/page.height)
    width=float(item.width/page.width)
    height=float(item.height/page.height)

    return BoundingBox(
        x=min(1, max(0, x)),
        y=min(1, max(0, y)),
        width=min(1, max(0, width)),
        height=min(1, max(0, height)),
    )


def _parse_points(points, page):
    xmin = min([point[0] for point in points])
    ymin = min([point[1] for point in points])
    xmax = max([point[0] for point in points])
    ymax = max([point[1] for point in points])

    x=float(xmin/page.width)
    y=float((page.height - ymax)/page.height)
    width=float((xmax - xmin)/page.width)
    height=float((ymax - ymin)/page.height)

    return BoundingBox(
        x=min(1, max(0, x)),
        y=min(1, max(0, y)),
        width=min(1, max(0, width)),
        height=min(1, max(0, height)),
    )


def _parse_page_entity(item, page):
    obj = None
    
    if isinstance(item, LTLine):
        # print(f"Line: {item}")
        obj = DrawLine(
            id=str(uuid4()),
            bbox=_parse_points(item.pts, page),
            confidence=1
        )
    elif isinstance(item, LTRect):
        # print(f"Rect: {item}")
        obj = DrawRectangle(
            id=str(uuid4()),
            bbox=_parse_points(item.pts, page),
            confidence=1
        )
    elif isinstance(item, LTCurve):
        # print(f"Curve: {item}")
        obj = DrawCurve(
            id=str(uuid4()),
            bbox=_parse_points(item.pts, page),
            confidence=1
        )
    elif isinstance(item, LTFigure):
        obj = Figure(
            id=str(uuid4()),
            bbox=_parse_bbox(item, page),
            confidence=1
        )
    elif isinstance(item, LTImage):
        obj = Image(
            id=str(uuid4()),
            bbox=_parse_bbox(item, page),
            confidence=1
        )

    elif isinstance(item, LTTextLine):
        obj = Line(
            id=str(uuid4()),
            bbox=_parse_bbox(item, page),
            text=item.get_text(),
            confidence=1
        )
    elif isinstance(item, LTTextBox):
        obj = Block(
            id=str(uuid4()),
            bbox=_parse_bbox(item, page),
            text=item.get_text(),
            confidence=1
        )
    elif isinstance(item, LTChar):
        obj = Character(
            id=str(uuid4()),
            bbox=_parse_bbox(item, page),
            text=item.get_text(),
            confidence=1,
            metadata={
                # 'line-width': item.graphicstate.linewidth,
                # 'line-cap': item.graphicstate.linecap,
                # 'line-join': item.graphicstate.linejoin,
                # 'miter-limit': item.graphicstate.miterlimit,
                # 'dash': item.graphicstate.dash,
                # 'intent': item.graphicstate.intent,
                # 'flatness': item.graphicstate.flatness,
                'color-space': item.ncs.name,
                'ncomponents': item.ncs.ncomponents,
                'font-family': item.fontname,
                'font-size': item.size,
                'text-stroke-color': item.graphicstate.scolor,
                'text-fill-color': item.graphicstate.ncolor,
            }
        )
    elif isinstance(item, LTText):
        pass
    else:
        assert False, str(("Unhandled", item))

    if isinstance(item, Iterable):
        for child in item:
            child_obj = _parse_page_entity(child, page)
            if child_obj is not None:
                obj.children.add(child_obj)
    
    return obj


def _parse_page(ltpage: LTPage, image: PILImage=None) -> Page:
    page = Page(
        page_number=ltpage.pageid,
        width=ltpage.width,
        height=ltpage.height,
        image=image
    )

    for item in ltpage:
        page_entity = _parse_page_entity(item, page)
        if page_entity is not None:
            page.children.add(page_entity)
    
    if image is not None:
        page.width = image.width
        page.height = image.height

    return page


def load(
        pdf_file: Union[pathlib.PurePath, str, bytes], 
        last_page: int=None, 
        load_image=True, 
        remove_text=False
    ) -> Document:
    """
    Load a PDF file into a Document object.

    :param pdf_file: Either a file path or a bytes object for the PDF file to be worked on.
    :type pdf_file: Union[pathlib.PurePath, str, bytes]
    :param last_page: The last page to be loaded, defaults to None
    :type last_page: int, optional
    :param load_image: if the image is loaded, defaults to False
    :type load_image: bool, optional
    :param remove_text: if the text is removed, defaults to False
    :type remove_text: bool, optional
    :return: A Document object
    :rtype: Document
    """
    if isinstance(pdf_file, pathlib.PurePath):
        pdf_file = str(pdf_file)

    if isinstance(pdf_file, str):
        with open(pdf_file, 'rb') as fp:
            pdf_content = fp.read()
    elif isinstance(pdf_file, bytes):
        pdf_content = pdf_file
    else:
        raise TypeError("pdf_file must be a file path or a file-like object.")

    if remove_text:
        pdf_writer = PdfWriter()
        pdf_reader = PdfReader(io.BytesIO(pdf_content))
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        pdf_writer.remove_text()

        # Save the modified PDF content to a new BytesIO object
        pdf_output = io.BytesIO()
        pdf_writer.write(pdf_output)
        pdf_output.seek(0)   # Reset the stream position to the beginning
        pdf_content = pdf_output.getvalue()

    ltpages = extract_pages(io.BytesIO(pdf_content), maxpages=last_page)
    ltpages = [x for x in ltpages]

    images = []
    if load_image:
        images = pdf2image.convert_from_bytes(pdf_content, last_page=last_page, fmt='jpeg')
        images = [image.convert('RGB') for image in images]

    document = Document()

    if len(ltpages) == len(images):
        for idx, ltpage in enumerate(ltpages):
            if idx < len(images):
                image = images[idx]
            else:
                image = None
            page = _parse_page(ltpage=ltpage, image=image)
            document.add(page)
    elif len(images) > 0:
        for idx, image in enumerate(images):
            page = Page(
                page_number=idx+1,
                width=image.width,
                height=image.height,
                image=image
            )
            document.add(page)
    else:
        for idx, ltpage in enumerate(ltpages):
            page = _parse_page(ltpage=ltpage)
            document.add(page)

    return document