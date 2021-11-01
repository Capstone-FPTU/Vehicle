# import main
from main import run, go_out_parking
from button_start_vehicle import start_button
list_villa = {
    "HOME": "left",
    "SONA": "right",
    "NAMI": "stop"
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
run(array, turn_value)
# go_out_parking(turn_value)
# start_button()