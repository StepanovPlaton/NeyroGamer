import pygame

_PNG_IMAGE = '1.jpg'

pygame.display.init()
img = pygame.image.load(_PNG_IMAGE)
screen = pygame.display.set_mode(img.get_size(), pygame.FULLSCREEN)
screen.blit(img, (0, 0))
pygame.display.flip()
input()
pygame.quit()