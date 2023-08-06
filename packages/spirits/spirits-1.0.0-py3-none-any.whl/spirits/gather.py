from typing import List

from PIL import Image

from .utils import block_check

def compose(images: List[List[Image.Image]], output_image: str, size_check:bool = True):
    width, height = block_check(images, size_check)
    output = Image.new("RGBA", (width, height))
    acc_w, acc_h = 0, 0
    # TODO: Don't care about waterfall style
    for idx, row in enumerate(images):
        for i, image in enumerate(row):
            w, h = image.size
            output.paste(image, (acc_w, acc_h))
            acc_w += w
        acc_h += h
        acc_w = 0
    output.save(output_image)