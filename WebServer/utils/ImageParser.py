from PIL import Image
import base64
import StringIO
import os

def get_string_for_png(file_path):
    output = StringIO.StringIO()
    im = Image.open(file_path)
    im.save(output, format='PNG')
    output.seek(0)
    output_s = output.read()
    b64 = base64.b64encode(output_s)
    return '{0}'.format(b64)

def get_string_for_svg(file_path):
    img_file = open(file_path, "rb")
    encoded_string = base64.b64encode(img_file.read())
    return encoded_string.decode('utf-8')