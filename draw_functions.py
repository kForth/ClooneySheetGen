from reportlab.lib import colors
from reportlab.lib.units import inch


def rectangle(canvas, x_pos, y_pos, width, height, stroke=1, fill=0, fill_color=colors.grey, stroke_color=colors.grey):
    y_pos = (11 * inch) - (y_pos * inch) - (height * inch)
    x_pos = x_pos * inch
    canvas.setFillColor(fill_color)
    canvas.setStrokeColor(stroke_color)
    canvas.rect(x_pos, y_pos, width * inch, height * inch, stroke=stroke, fill=fill)


def box(canvas, x_pos, y_pos, size, stroke=1, fill=0, label="", font_size=0.15, fill_color=colors.grey, stroke_color=colors.grey):
    rectangle(canvas, x_pos, y_pos, size, size, stroke, fill, fill_color, stroke_color)
    centered_string(canvas, x_pos + (size / 2), y_pos + (size / 2.0) - (font_size / 2.0), label, font_size, fill_color)


def centered_string(canvas, x_pos, y_pos, text, font_size, fill_color=colors.grey):
    canvas.setFillColor(fill_color)
    canvas.setFontSize(font_size * inch)
    x_pos = x_pos * inch
    y_pos = (11 * inch) - (y_pos * inch) - (font_size * 0.8 * inch)
    canvas.drawCentredString(x_pos, y_pos, text)


def string(canvas, x_pos, y_pos, text, font_size, fill_color=colors.grey):
    canvas.setFillColor(fill_color)
    canvas.setFontSize(font_size * inch)
    x_pos = x_pos * inch
    y_pos = (11 * inch) - (y_pos * inch) - (font_size * 0.8 * inch)
    canvas.drawString(x_pos, y_pos, text)


def image(canvas, x_pos, y_pos, width, height, filepath, fill_color=colors.grey):
    canvas.setFillColor(fill_color)
    y_pos = (11 * inch) - (y_pos * inch) - (height * inch)
    x_pos = x_pos * inch
    if filepath:
        canvas.drawImage(filepath, x_pos, y_pos, width * inch, height * inch)
