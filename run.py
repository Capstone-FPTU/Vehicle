# import main
from main import run, go_out_parking
list_villa = {
    "HOME": "left",
    "SONA": "right",
    "YUMMI": "forward",
    "NAMI": "forward",
    "LULU": "right",
    "LUX": "left",
    "TEEMO": "stop",
    "P1": "right",
    "SONA": "parking",
}
array = {}
turn_value = ''
for key, value in list_villa.items():
    if not key[1].isdigit():
        array[key.upper()] = value.upper()
    if key == "HOME":
        turn_value = value
run(array)
# go_out_parking(turn_value)