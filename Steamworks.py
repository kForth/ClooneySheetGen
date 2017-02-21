from Sheet import *
from Fields import *

config = {  "num_sheets":               1,
            "filename":                 "Steamworks",
            "encode_scanner":           True,
            "event":                    "Test 2017",
            "spacer_page":              True,
            "x_pos":                    0.25,
            "y_spacing":                0.18,
            "box_size":                 0.18, #0.2
            "box_spacing":              0.1,
            "bool_x_offset":            1.95,
            "font_size":                0.12, #0.15
            "box_font_size":            0.1,
            "marker_size":              0.5,
            "divider_height":           1.0/64,
            "team_x_offset":            5.6875,
            "seven_segment_width":      0.25,
            "seven_segment_thickness":  0.0625,
            "seven_segment_offset":     0.5,
            "marker_colour":            (255, 0, 0),
            "font_color":               (100, 100, 100),
            "label_offset":             1.25
}
config["bool_x_offset"] = (config["box_size"] + config["box_spacing"]) * 6

sheet = Sheet(config)

sheet.add_field(Image("Draw the Robot", 2, 1.5, None, prev_line=True, offset = 3.5, y_offset = 1.25))
sheet.add_field(Divider("Autonomous"))
sheet.add_field(Boolean("Reach Baseline"))
sheet.add_field(Boolean("Trigger Hopper"))
sheet.add_field(Boolean("Scored Low Boiler"))
sheet.add_field(Numbers("High Boiler", tens=5))
sheet.add_field(Numbers("Gears", ones = 3))

sheet.add_field(Divider("Tele-Op"))
sheet.add_field(String("Tally", font_size = 0.125, height = "thin", x_offset = 1.625))
sheet.add_field(Numbers("Placed Gears", tally = True, tens=1))
sheet.add_field(Numbers("Dropped Gears", tally = True, tens=1))
sheet.add_field(Numbers("Gears from Floor", tally = True, tens=1))

sheet.add_field(Numbers("Scored High", ones=0, tens=10, tally = True))
sheet.add_field(Numbers("High Boiler Attempts", tally = True))
sheet.add_field(Numbers("Low Boiler Attempts", tally = True))
sheet.add_field(HorizontalOptions("Climbed", options="S F NA"))

sheet.add_field(Divider("Actions"))
sheet.add_field(Boolean("Scored Low"))
sheet.add_field(Boolean("Balls from Hopper"))
sheet.add_field(Boolean("Balls from Chute"))
sheet.add_field(Boolean("Balls from Floor"))
sheet.add_field(HorizontalOptions("Defense", options=str("M Md H 🔥")))


sheet.add_field(Divider("Overall Performance"))
sheet.add_field(Boolean("Disabled"))
sheet.add_field(Boolean("Didn't Move"))
sheet.add_field(Boolean("No Show"))
sheet.add_field(Numbers("Confidence", ones=5))
# sheet.add_field(Numbers("Defence", ones=3))
sheet.add_field(Image("Notes", 5.625, 0.75, None))#, offset = 3.5, y_offset = 1))

# sheet.add_field(Divider())
# sheet.add_field(String("S = Success    F = Fail"))

sheet.draw_sheets()
