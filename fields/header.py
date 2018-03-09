from fields._base import FieldBase
from fields.string import String
from fields.barcode  import Barcode
from fields.box_number import BoxNumber


class Header(FieldBase):
    POSITIONS = [
        "Red 1",
        "Red 2",
        "Red 3",
        "Blue 1",
        "Blue 2",
        "Blue 3"
    ]

    def __init__(self, match, pos):
        super().__init__()
        self.match = match
        self.pos = pos

    def draw(self, canvas, x_pos, y_pos, config):
        String("Celt-X Team 5406", font_size=0.25).draw(canvas, 0.05 + config["marker_size"],
                                                       0.05 + config["marker_size"], config)
        String(config["event"], font_size=3.0 / 32).draw(canvas, 0.125 + config["marker_size"],
                                                         0.3 + config["marker_size"], config)
        String("Match " + str(self.match) + "    " + self.POSITIONS[self.pos] + "    Scout: _______", font_size=0.25) \
            .draw(canvas, 0.125 + config["marker_size"], 7.0/16 + config["marker_size"], config)

        match_pos_string = str(self.match)
        while len(match_pos_string) < 3:
            match_pos_string = "0" + match_pos_string
        match_pos_string += str(self.pos)

        barcode = Barcode("-EncodedMatchData", int(match_pos_string))
        barcode.set_id("encoded_match_data")
        barcode_x = 8.5 - config["marker_size"]
        barcode_y = config["marker_size"]
        barcode.draw(canvas, barcode_x, barcode_y, config)

        team_num = BoxNumber("Team Number")
        team_num.set_id("team_number")
        team_num_x = config["x_pos"] + config["marker_size"]
        team_num_y = 1
        team_num.draw(canvas, team_num_x, team_num_y, config)

        box_bardcode_info = [
            {
                "type":    barcode.get_type(),
                "id":      barcode.get_id(),
                "options": barcode.get_info(),
                "x_pos":   barcode_x,
                "y_pos":   barcode_y,
                "height":  barcode.get_height(config)
            },
            {
                "type":    team_num.get_type(),
                "id":      team_num.get_id(),
                "options": team_num.get_info(),
                "x_pos":   team_num_x,
                "y_pos":   team_num_y,
                "height":  team_num.get_height(config)

            }
        ]

        return self.get_height(config), box_bardcode_info

    def get_height(self, config):
        return BoxNumber("Team Number").get_height(config)
