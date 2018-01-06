from fields.horizontal_options import HorizontalOptions


class Numbers(HorizontalOptions):
    def __init__(self, label, ones=9, tens=0, show_zero=False, **kwargs):
        options = []
        for i in range(0 if show_zero else 1, ones + 1):
            options.append(str(i))
        if tens > 0:
            for j in range(1, tens + 1):
                options.append("+10")

        HorizontalOptions.__init__(self, label, options, **kwargs)
