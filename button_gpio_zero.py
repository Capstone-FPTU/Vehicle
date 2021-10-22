from gpiozero import Button

button = Button(4)
count = 0
while True:
    button.wait_for_press()
    print("The button was pressed!", count)
    count +=1