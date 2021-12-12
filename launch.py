# Open Pixel Control client: Test crosstalk between LED strips;
# send each strip a different pattern, use a lot of low-brightness
# pixels so that glitches show up clearly.
#
# This also helps identify strips. The first three LEDs are colored
# according to the strip number, in binary: MSB first, bright green
# for 1 and dim red for 0.

from argparse import ArgumentParser
from typing import Dict, List
from yaml import load
from controleds.controleds import LEDSControl
from pixels.pixels import Pixel

from copy import copy

try:
	from yaml import CLoader as Loader
except ImportError:
	from yaml import Loader


import opc, time

import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True,markup=True)]
)

log = logging.getLogger("launch")

parser = ArgumentParser(prog = 'launch.py', description='Controlador de luces de navidad')
parser.add_argument('--config',help = 'Archivo de configuracion, por defecto ./config.yml')


args = parser.parse_args()

cFile = './config.yml'

if args.config is not None:
	cFile = args.config

log.info(f'Cargando configuracion de {cFile}')

configuration: Dict = None
with open(cFile,'r') as cstream:
	configuration = load(cstream,Loader = Loader)
	configuration = configuration.get('controlnavidad',{})

urlClient = f'{configuration.get("host","localhost")}:{configuration.get("port",7890)}'

log.info(f'Conectando con {urlClient}...')

client: opc.Client = None

try:
	client = opc.Client('localhost:7890')
except Exception:
	log.error(f'No se pudo conectar con servidor en {urlClient}')
	exit(-1)

log.info('CONECTADO!')

LEDSControl.loggingLevel(logging.INFO)

panel = LEDSControl(size = 512,initial_tuple=(0,0,0))
bits = ( (80,0,0), (0,255,0) )

panel.strips_order = [0,7,3,2,4,5,6,1]

list_of_pixels: List[Pixel] = [
	Pixel((255,255,255)), #White
	Pixel((255,99,71)), #tomato
	Pixel((0,255,127)), #spring green
	Pixel((135,206,235)), #skyblue
	Pixel((221,160,221)), #plum
	Pixel((255,127,80)), #Coral
	Pixel((102,205,170)), #medium aquamarine
	Pixel((100,149,237)), #corn flower blue
]
list_of_animations: List[List[Pixel]] = list()

pixel_iterator: iter = iter(list_of_pixels)

#Construir las animaciones
for p in list_of_pixels:
	animation: List[Pixel] = list()
	current_pixel: Pixel = copy(p)
	while current_pixel.rgb != (0,0,0):
		animation.append(current_pixel)
		current_pixel.fadeLightness(0.2)
	inverse = copy(animation)
	inverse = inverse[0:round(len(inverse)/2)]
	inverse.reverse()

	sequence = inverse + [p for _ in range(10)] + animation[0:round(len(animation)/2)]
	list_of_animations.append(sequence)

ciclo_animaciones = iter(list_of_animations)

# log.info(f'Ciclo animaciones:  {list_of_animations}')
while True:

	animacion = next(ciclo_animaciones,None)
	log.info(f'Current animacion: {animacion}')

	client.put_pixels(panel.tablero)
	if animacion is None:
		ciclo_animaciones = iter(list_of_animations)
		animacion = next(ciclo_animaciones,None)
	
	for p in animacion:
		for i in range(192):
			panel.setPixel(i,p.rgb)
		client.put_pixels(panel.tablero)
		time.sleep(0.3)

	# nPixel = iter(animation)

	# animacionNotEnded: bool = True
	# while animacionNotEnded:
	# 	current_pixel = next(nPixel,None)
	# 	log.info(f'PIXEL: {current_pixel}')
	# 	if current_pixel is None:
	# 		animacionNotEnded = False
	# 	else:
	# 		for i in range(192):
	# 			panel.setPixel(i,current_pixel.rgb)
	# 		client.put_pixels(panel.tablero)
	# 	time.sleep(0.5)



# salidaReal: bool = True
# while True:
# 	contador: int = 0

# 	current_pixel = next(pixel_iterator,None)
# 	if current_pixel is None:
# 		salidaReal = True
# 		break

# 	for i in range(192):
# 		panel.setPixel(i,current_pixel.rgb)

# 	client.put_pixels(panel.tablero)

# 	current_animation: List[Pixel] = list()
# 	# tira_red: List[Pixel] = list()
# 	# tira_green: List[Pixel] = list()
# 	# tira_blue: List[Pixel] = list()

# 	controlFlag: bool = True
# 	while controlFlag:
# 		if contador > 0:
# 			current_pixel.fadeLightness(0.1)
# 		current_animation.append(copy(current_pixel))
# 		for i in range(192):
# 			panel.setPixel(i,current_pixel.rgb)
# 		client.put_pixels(panel.tablero)
# 		contador += 1
# 		time.sleep(0.5)
# 		if current_pixel.rgb == (0,0,0):
# 			controlFlag = False

# 	second_sequence = copy(current_animation)
# 	current_animation.reverse()
# 	current_animation = current_animation + second_sequence

# 	log.info(f'ANIMATION: {current_animation}')
# 	contador = 0
# 	controlFlag = True

# 	while controlFlag:
# 		for i in range(192):
# 			panel.setPixel(i,current_animation[contador].rgb)
# 		client.put_pixels(panel.tablero)
# 		contador+=1
# 		time.sleep(0.5)
# 		if contador >= len(current_animation):
# 			controlFlag = False




# while True:
# 	# Flash each strip in turn
# 	for strip in range(8):
# 		panel.tablero = [ (90,90,90) ] * 512
# 		for i in range(32):
# 			panel.setPixel(strip * 64 + i * 2,(200,200,200))

# 		# Label all strips always
# 		for s in range(8):
# 			panel.setPixel(s * 64 + 0,bits[(s >> 2) & 1])
# 			panel.setPixel(s * 64 + 1,bits[(s >> 1) & 1])
# 			panel.setPixel(s * 64 + 2,bits[(s >> 0) & 1])

# 		client.put_pixels(panel.copyTablero())
# 		time.sleep(0.5)

# while True:
# 	for i in range(192):
# 		panel.setTableroToPixel((0,0,0))
# 		panel.setPixel(i,(255, 255, 255))
# 		client.put_pixels(panel.tablero)
# 		time.sleep(0.01)
