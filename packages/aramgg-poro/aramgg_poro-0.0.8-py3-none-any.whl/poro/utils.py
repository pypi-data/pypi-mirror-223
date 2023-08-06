import re

from io import BytesIO
from PIL import Image
import base64

def dict_to_str(d, tab=0):
    s = ["{\n"]
    for k, v in d.items():
        if isinstance(v, dict):
            v = dict_to_str(v, tab+1)
        else:
            v = repr(v)
        
        s.append("%s%r: %s,\n" % ("  "*tab, k, v))
    s.append("%s}" %("  "*tab))
    return ''.join(s)

def get_int_from_str(str):
    return int(re.sub(r"[^0-9]", "", str))

def img_to_str(img):
    buffer = BytesIO()
    with BytesIO(img) as f:
        with Image.open(f) as _img:
            if _img.mode!="RGB":
                _img = _img.convert("RGB")
            _img.save(buffer, format="jpeg")
            str = base64.b64encode(buffer.getvalue())
            buffer.close()
    
    return str

def version_to_id(version):
    return "".join([version.split(".")[0], version.split(".")[1], "01"])

def match_version_to_version(match_version):
    return "".join([match_version.split(".")[0], ".", match_version.split(".")[1], ".1"])