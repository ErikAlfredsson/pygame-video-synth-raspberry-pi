import pygame, sys, os, time
import RPi.GPIO as GPIO

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
PATH = BASE_PATH + "/images/"
images = filter( lambda f: not f.startswith('.') and f.endswith('.jpg'), os.listdir(PATH))
current = 0
num_files = len(images)
loaded_images = []

for i in xrange(0,len(images)):
	name = images[i]
	image = pygame.image.load(PATH + name)
	loaded_images.append(image)	

pygame.init()

info = pygame.display.Info()
print(info)

size = (info.current_w, info.current_h)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.NOFRAME)
white = (255,255,255)
screen.fill(white)

print(screen.get_size())

def nextImage():
	global current, loaded_images, screen

	image = loaded_images[current % len(loaded_images)]	
	image = image.convert()
	image = pygame.transform.scale(image, size)
	screen.blit(image, (0, 0))
	pygame.display.flip()

	# When we get to the end, re-start at the beginning
	current = (current + 1) % num_files	

nextImage()

channel = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

was_low = False

while True:		
	if GPIO.input(channel) and was_low:			
		nextImage()
		was_low = False			
	elif GPIO.input(channel) == 0:
		was_low = True

exit(0)