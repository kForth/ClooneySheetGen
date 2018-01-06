from abc import abstractmethod

import numpy as np


class FieldBase(object):
    SHEET_WIDTH = 8.5
    SHEET_HEIGHT = 11

    def __init__(self):
        self.prev_line = False
        self.id = None
        self.label = None

    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def _iter(self, img, x_pos, y_pos, config, func, *args, **kwargs):
        pass

    @abstractmethod
    def draw(self, canvas, x_pos, y_pos, config):
        pass

    def _read_box(self, img, x_pos, y_pos, width, height, min_val=50):
        crop = img[y_pos:y_pos + height, x_pos:x_pos + width]
        avg = crop.sum() / (3 * crop.size)
        return avg < min_val

    # @abstractmethod
    # def read(self, img, x_pos, y_pos, config):
    #     pass

    def set_id(self, data_id):
        self.id = data_id

    def get_id(self):
        return self.id

    def get_label(self):
        return self.label

    def get_type(self):
        return self.__class__.__name__

    def get_height(self, config):
        return 0

    def get_width(self, config):
        return 0
