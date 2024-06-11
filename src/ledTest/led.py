# Bibliotheken laden
from gpiozero import LED
from time import sleep

# Initialisierung von GPIO17 als LED (Ausgang)
#led = LED(17)

while(True):
	val = input('enter input:')
	if val == 's':
		# 5 Sekunden warten
		#led.on()
		sleep(1)
		#led.off()
		print("s")
	if val == 'q':
		break
print('feddich')
