# import main
from main import run, go_out_parking
list_villa = {
    "HOME": "left",
    "SONA": "right",
    "YUMMI": "forward",
    "NAMI": "parking",
    "LULU": "right",
    "LUX": "right",
    "TEEMO": "stop",
    "P1": "right",
    "SONA": "right",
}
values_view = list_villa.values()
value_iterator = iter(values_view)
first_value = next(value_iterator)
nguhoc = next(iter(list_villa.items())).count
print(first_value)
array = {}
turn_value = ''
for key, value in list_villa.items():
    if not key[1].isdigit():
        array[key.upper()] = value.upper()
    if key == "HOME":
        turn_value = value.upper()
# run(array, turn_value)
# go_out_parking(turn_value)