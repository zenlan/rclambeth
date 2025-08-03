#!/usr/bin/ python3

import json
import math
from PIL import Image, ImageDraw, ImageFont
import funcs


def compile_lines(data):

    lines = []
    lines.append("First Saturday each month 10am-1pm - come early!")
    lines.append("336 Brixton Rd, London SW9 7AA")
    lines.append("One item per person please. No microwaves.")
    lines.append("www.repaircafe-lambeth.org")
    lines.append(
        "{:,} kg of landfill and {:,} kg of CO2 prevented!".format(
            math.ceil(data["stats"]["waste_total"]),
            math.ceil(data["stats"]["co2_total"]),
        )
    )
    return lines


def params_global():

    params = {}
    params["imgqr"] = Image.open("891qr.png")
    params["rgb_background"] = (39, 40, 133)  # 272885
    params["title"] = "Repair Café Lambeth"
    params["font_ttf_title"] = "fonts/OpenSans-Bold.ttf"
    params["font_rgb_title"] = (243, 111, 84)  # f36f54
    params["font_ttf_lines"] = "fonts/OpenSans-Regular.ttf"
    params["font_rgb_lines"] = (255, 255, 255)
    return params


def params_landscape(params):

    params["height"] = round(params["imgqr"].size[1])
    params["width"] = round(params["height"] * 2.0)
    params["margin_left"] = 10
    params["margin_top"] = 0
    params["merge_qr"] = "r"

    # TITLE
    params["font_size_title"] = 48
    params["font_title"] = ImageFont.truetype(
        params["font_ttf_title"],
        params["font_size_title"],
    )

    # LINES
    params["top_lines"] = 62
    params["lines_spacing"] = 16
    params["font_size_lines"] = 20
    params["font_lines"] = ImageFont.truetype(
        params["font_ttf_lines"],
        params["font_size_lines"],
    )
    return params


def params_square(params):

    params["width"] = round(params["imgqr"].size[0] * 2.0)
    params["height"] = params["width"]
    params["margin_left"] = 10
    params["margin_top"] = 0
    params["merge_qr"] = "b"

    # TITLE
    params["font_size_title"] = 48
    params["font_title"] = ImageFont.truetype(
        params["font_ttf_title"],
        params["font_size_title"],
    )

    # LINES
    params["top_lines"] = 62
    params["lines_spacing"] = 16
    params["font_size_lines"] = 20
    params["font_lines"] = ImageFont.truetype(
        params["font_ttf_lines"],
        params["font_size_lines"],
    )
    return params


def generate_image(lines, params, suffix):

    out = Image.new(
        "RGB", (params["width"], params["height"]), params["rgb_background"]
    )
    d = ImageDraw.Draw(out)

    d.text(
        (params["margin_left"], params["margin_top"]),
        params["title"],
        font=params["font_title"],
        fill=params["font_rgb_title"],
    )
    d.multiline_text(
        (params["margin_left"], params["top_lines"]),
        "\n".join(lines),
        font=params["font_lines"],
        fill=params["font_rgb_lines"],
        spacing=params["lines_spacing"],
        align="left",
    )
    if params["merge_qr"] != "x":
        out = merge(out, params["imgqr"], where=params["merge_qr"])
    out.save("891_{}.png".format(suffix))


def merge(im1, im2, where="r"):
    iw = 0
    ih = 1
    if where == "r":
        w = im1.size[iw] + im2.size[iw]
        h = max(im1.size[ih], im2.size[ih])
        x = im1.size[iw]
        y = 0
    elif where == "b":
        w = im1.size[iw]
        h = im1.size[ih]
        x = round((w / 2 / 2))
        y = round((h / 2) - 10)

    im = Image.new("RGB", (w, h))
    im.paste(im1)
    im.paste(im2, (x, y))
    return im


if __name__ == "__main__":

    logger = funcs.init_logger()

    data = json.load(open("891.json", "r"))["data"]
    lines = compile_lines(data)

    params = params_global()
    params = params_landscape(params)
    generate_image(lines, params, "landscape")

    params = params_global()
    params = params_square(params)
    generate_image(lines, params, "square")
