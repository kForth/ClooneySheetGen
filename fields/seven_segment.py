import draw_functions as draw
from fields._base import FieldBase


class SevenSegment(FieldBase):
    NUMBERS = [[True, True, True, False, True, True, True],  # 0
               [False, False, True, False, False, True, False],  # 1
               [True, False, True, True, True, False, True],  # 2
               [True, False, True, True, False, True, True],  # 3
               [False, True, True, True, False, True, False],  # 4
               [True, True, False, True, False, True, True],  # 5
               [True, True, False, True, True, True, True],  # 6
               [True, False, True, False, False, True, False],  # 7
               [True, True, True, True, True, True, True],  # 8
               [True, True, True, True, False, True, True],  # 9
               [False, True, False, False, True, False, False],  # Alternate 1
               [False, False, False, False, False, False, False]]  # Blank / Alternate Zero

    def __init__(self, value=11):
        super().__init__()
        if value == " ":
            value = 11
        self.value = value

    def _iter(self, img, x_pos, y_pos, config, func, *args, **kwargs):
        width = config["seven_segment_width"]
        thickness = config["seven_segment_thickness"]
        values = []
        values.append(func(img, x_pos + thickness, y_pos, width, thickness,
                   *[e(0) if callable(e) else e for e in args],
                   **dict([(k, v(0) if callable(v) else v) for k, v in kwargs.items()])))
        values.append(func(img, x_pos, y_pos + thickness, thickness, width,
                   *[e(1) if callable(e) else e for e in args],
                   **dict([(k, v(1) if callable(v) else v) for k, v in kwargs.items()])))
        values.append(func(img, x_pos + thickness + width, y_pos + thickness, thickness, width,
                   *[e(2) if callable(e) else e for e in args],
                   **dict([(k, v(2) if callable(v) else v) for k, v in kwargs.items()])))
        values.append(func(img, x_pos + thickness, y_pos + thickness + width, width, thickness,
                   *[e(3) if callable(e) else e for e in args],
                   **dict([(k, v(3) if callable(v) else v) for k, v in kwargs.items()])))
        values.append(func(img, x_pos, y_pos + thickness * 2 + width, thickness, width,
                   *[e(4) if callable(e) else e for e in args],
                   **dict([(k, v(4) if callable(v) else v) for k, v in kwargs.items()])))
        values.append(func(img, x_pos + thickness + width, y_pos + thickness * 2 + width, thickness, width,
                   *[e(5) if callable(e) else e for e in args],
                   **dict([(k, v(5) if callable(v) else v) for k, v in kwargs.items()])))
        values.append(func(img, x_pos + thickness, y_pos + width * 2 + thickness * 2, width, thickness,
                   *[e(6) if callable(e) else e for e in args],
                   **dict([(k, v(6) if callable(v) else v) for k, v in kwargs.items()])))

    def draw(self, canvas, x_pos, y_pos, config):
        self._iter(canvas, x_pos, y_pos, config, draw.rectangle, fill=lambda i: self.NUMBERS[self.value][i])
        # width = config["seven_segment_width"]
        # thickness = config["seven_segment_thickness"]
        # draw.rectangle(canvas, x_pos + thickness, y_pos, width, thickness, fill=numbers[self.value][0])
        # draw.rectangle(canvas, x_pos, y_pos + thickness, thickness, width, fill=numbers[self.value][1])
        # draw.rectangle(canvas, x_pos + thickness + width, y_pos + thickness, thickness, width,
        #                fill=numbers[self.value][2])
        # draw.rectangle(canvas, x_pos + thickness, y_pos + thickness + width, width, thickness,
        #                fill=numbers[self.value][3])
        # draw.rectangle(canvas, x_pos, y_pos + thickness * 2 + width, thickness, width, fill=numbers[self.value][4])
        # draw.rectangle(canvas, x_pos + thickness + width, y_pos + thickness * 2 + width, thickness, width,
        #                fill=numbers[self.value][5])
        # draw.rectangle(canvas, x_pos + thickness, y_pos + width * 2 + thickness * 2, width, thickness,
        #                fill=numbers[self.value][6])
        return self.get_height(config)

    def get_height(self, config):
        return config["seven_segment_width"] * 2 + config["seven_segment_thickness"] * 3 + config["y_spacing"]
