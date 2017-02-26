from reportlab.lib.units import inch


def draw_rect(canvas, x_pos, y_pos, width, height, outline=1, infill=0):
    y_pos = (11 * inch) - (y_pos * inch) - (height * inch)
    x_pos = x_pos * inch
    canvas.rect(x_pos, y_pos, width * inch, height * inch, stroke=outline, fill=infill)


def draw_square(canvas, x_pos, y_pos, size, outline=1, infill=0, label="", font_size=0.15):
    draw_rect(canvas, x_pos, y_pos, size, size, outline, infill)
    draw_centered_string(canvas, x_pos + (size / 2), y_pos + (size / 2.0) - (font_size / 2.0), label, font_size)


def draw_centered_string(canvas, x_pos, y_pos, text, font_size):
    canvas.setFontSize(font_size * inch)
    x_pos = x_pos * inch
    y_pos = (11 * inch) - (y_pos * inch) - (font_size * 0.8 * inch)
    canvas.drawCentredString(x_pos, y_pos, text)


def draw_string(canvas, x_pos, y_pos, text, font_size):
    canvas.setFontSize(font_size * inch)
    x_pos = x_pos * inch
    y_pos = (11 * inch) - (y_pos * inch) - (font_size * 0.8 * inch)
    canvas.drawString(x_pos, y_pos, text)


def draw_image(canvas, x_pos, y_pos, width, height, filepath):
    y_pos = (11 * inch) - (y_pos * inch) - (height * inch)
    x_pos = x_pos * inch
    canvas.drawImage(filepath, x_pos, y_pos, width * inch, height * inch)
