from Sheet import *
from Fields import *

config = {  "num_sheets":               60,
            "filename":                 "Stronghold.pdf",
            "encode_scanner":           True,
            "event":                    "Ra Cha Cha Ruckus 2016",
            "spacer_page":              True,
            "x_pos":                    0.25,
            "y_spacing":                3/16.0,
            "box_size":                 0.2,
            "box_spacing":              0.125,
            "bool_x_offset":            1.95,
            "font_size":                0.15,
            "marker_size":              0.5,
            "divider_height":           1.0/64,
            "team_x_offset":            5.6875,
            "seven_segment_width":      0.25,
            "seven_segment_thickness":  0.0625,
            "seven_segment_offset":     0.5,
            "marker_colour":            (255, 0, 0),
            "font_color":               (100, 100, 100)
}

sheet = Sheet(config)

sheet.add_field(Divider("Autonomous"))
sheet.add_field(Numbers("Auton High", ones = 3))
sheet.add_field(Numbers("Auton Low", ones = 3, prev_line=True))
sheet.add_field(Boolean("Reached"))
sheet.add_field(BulkOptions("Auto Crossed", "1 F", ["LB", "P", "CF", "M", "R", "D", "SP", "RW", "RT"]))

sheet.add_field(Divider("Tele-Op"))
sheet.add_field(String("Tally", font_size = 0.125, height = "thin", x_offset = 1.375))
sheet.add_field(Numbers("Scored High", tally = True))
sheet.add_field(Numbers("Scored Low", tally = True))
sheet.add_field(Numbers("Shots Missed", tally = True))
sheet.add_field(Divider())
sheet.add_field(BulkOptions("Crossed", "1 2 F", ["LB", "P", "CF", "M", "R", "D", "SP", "RW", "RT"]))
sheet.add_field(Image("Draw the Robot", 2, 1.5, None, prev_line=True, offset = 3.5, y_offset = 1))
sheet.add_field(Boolean("Challenged"))
sheet.add_field(Boolean("Scale"))
sheet.add_field(Divider("Overall Performance"))
sheet.add_field(Boolean("Disabled"))
sheet.add_field(Boolean("Got Stuck"))
sheet.add_field(Boolean("No Show"))
sheet.add_field(Boolean("Defence"))
# sheet.add_field(Numbers("Defence", ones=3))
sheet.add_field(Image("Notes", 5.625, 0.75, None))#, offset = 3.5, y_offset = 1))

# sheet.add_field(Divider())
# sheet.add_field(String("S = Success    F = Fail"))

sheet.draw_sheets()
