import main

list_villa = {
    "HOME": "left",
    "SONA": "forward",
    "YUMMI": "forward",
    "NAMI": "forward",
    "LULU": "right",
    "LUX": "right",
    "TEEMO": "stop",
    "P1": "right"
}
array = {}

for key, value in list_villa.items():
    if not key[1].isdigit():
        array[key.upper()] = value.upper()
main.run(array)