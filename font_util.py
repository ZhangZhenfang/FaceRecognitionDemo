from PIL import Image, ImageDraw, ImageFont
import numpy as np


class FontUtil:
    @staticmethod
    def text2Mat(text, height, width, font_size):
        ones = np.ones((height, width)) * 255
        canvas = Image.fromarray(ones)
        canvas = canvas.convert("RGB")
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.truetype("simhei.ttf", font_size, encoding="utf-8")
        draw.text((0, 0), text, (255, 0, 255), font=font)
        return canvas
