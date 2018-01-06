from abc import abstractmethod


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
