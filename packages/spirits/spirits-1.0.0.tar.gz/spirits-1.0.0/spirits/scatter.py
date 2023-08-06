import os

from .utils import get_image

def division(image_ref: str, row:int, column:int, output_dir:str):
    image = get_image(image_ref)
    ext_name = image_ref.split('.')[-1]
    w, h = image.size
    w_delta, h_delta = w//column, h//row
    if os.path.exists(output_dir):
        if not os.path.isdir(output_dir):
            raise RuntimeError(f"{output_dir} exists and isn't a folder")
    else:
        os.mkdir(output_dir)
    for r in range(row):
        for c in range(column):
            left, upper = c * w_delta, r * h_delta
            image.crop((left, upper, left+w_delta, upper+h_delta)).save(os.path.join(output_dir,f"{r}-{c}.{ext_name}"))

