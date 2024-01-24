import io
import base64
from PIL import Image
import numpy as np
from IPython.display import HTML


def display_html(html):
    display(HTML(f"<body>{html}</body>"))


def html_text(text, align="center"):
    return f"<div style=\"text-align:{align}\">{text}</div>"


def html_image(img, size=256):
    if isinstance(img, str):
        return f"<img src={img} width={size} height={size} />"
    elif isinstance(img, Image.Image):
        img_stream = io.BytesIO()
        img.save(img_stream, format="webp")
        base64_img = base64.b64encode(img_stream.getvalue()).decode("utf-8")
        return f"<img src=\"data:image/webp;base64,{base64_img}\" width={size} height={size} />"
    elif isinstance(img, np.ndarray):
        img_stream = io.BytesIO()
        Image.fromarray(img).save(img_stream, format="webp")
        base64_img = base64.b64encode(img_stream.getvalue()).decode("utf-8")
        return f"<img src=\"data:image/webp;base64,{base64_img}\" width={size} height={size} />"


def html_table(table):
    content = "".join([
            "<tr>" + 
        "".join([
            "".join([f"<td>{item}</td>"])
            for item in row
        ]) +
            "</tr>"
        for row in table
    ])
    return f"<table>{content}</table>"
