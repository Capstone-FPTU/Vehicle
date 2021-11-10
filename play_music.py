import pygame
def music(data):
    pygame.mixer.init()
    pygame.mixer.music.load(data)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
