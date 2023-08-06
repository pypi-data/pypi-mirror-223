from typing import List, Tuple, Optional

import requests as reqs
from PIL import Image


# region get image object
def get_image_from_url(url:str) -> Image.Image:
    image_content = reqs.get(url).content
    return Image.open(image_content)

def get_image_from_file(file:str) -> Image.Image:
    return Image.open(file)

def get_image(image_ref:str) -> Image.Image:
    if image_ref.startswith("http") and "://" in image_ref: # http[s]://
        return get_image_from_url(image_ref)
    else:
        return get_image_from_file(image_ref)

# endregion get image object

def block_check(images: List[List[Image.Image]], if_raise:bool = True) -> Tuple[int, int]:
    """
    make sure images in the same row have the same height
    make sure images in the same column have the same width
    :return: the (width, height) of desired image
    """
    iWidth, iHeight = 0, 0
    for i, line in enumerate(images): # check height each line
        width, height = line[0].size
        iWidth += width
        for idx, val in enumerate(line):
            if val.size[1] != height and if_raise:
                raise RuntimeError(f"row {i} col {idx}'s height is {val.size[1]} diffing {height}")
    
    columns = len(images[0])
    for idx in range(columns): # check width each column
        width, height = images[0][idx].size
        iHeight += height
        for row in range(len(images)):
            if images[row][idx].size[0] != width and if_raise:
                raise RuntimeError(f"row {row} col {idx}'s width is {images[row][idx].size[0]} diffing {width}")
    return iWidth, iHeight

def make_none_zero(value: Optional[int]) -> int:
    return 0 if value is None else value


def partition_check(count:int, row:int, column:int) -> Tuple[int, int]:
    if count ==0 or (row == 0 and column == 0):
        raise RuntimeError("no image is specified or row and column can both are 0")
    if row == 0:
        row = count // column
    elif column == 0:
        column = count // row
    if row * column != count:
        raise RuntimeError("row * column doesn't match the count of files")
    return row, column

def partition(image_ref:List[str], row:int=0, column:int=0) -> List[List[Image.Image]]:
    count = len(image_ref)
    row, column = partition_check(count, row, column)
    desired, idx = [], 0
    while idx+1 < count:
        desired.append([
            get_image(img)
            for img in image_ref[idx:idx+column]
        ])
        idx += column
    return desired