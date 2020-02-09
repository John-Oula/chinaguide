import os
import secrets

from PIL.Image import Image


def save_pic(form_pic):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_pic.filename)
    pic_fn = random_hex + f_ext
    pic_path = os.path.join(app.root_path,'static/profile_pics',pic_fn)
    output_size = (500,500)
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    i.save(pic_path)
    return pic_fn
