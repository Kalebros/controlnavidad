# Open Pixel Control client: Test crosstalk between LED strips;
# send each strip a different pattern, use a lot of low-brightness
# pixels so that glitches show up clearly.
#
# This also helps identify strips. The first three LEDs are colored
# according to the strip number, in binary: MSB first, bright green
# for 1 and dim red for 0.

from argparse import ArgumentParser
from typing import Dict
from yaml import load
from controleds.controleds import LEDSControl

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

while True:
	for i in range(192):
		panel.setTableroToPixel((0,0,0))
		panel.setPixel(i,(255, 255, 255))
		client.put_pixels(panel.tablero)
		time.sleep(0.01)


# bits = ( (80,0,0), (0,255,0) )

# while True:
# 	# Flash each strip in turn
# 	for strip in range(8):
# 		pixels = [ (90,90,90) ] * 512
# 		for i in range(32):
# 			pixels[strip * 64 + i * 2] = (200,200,200)

# 		# Label all strips always
# 		for s in range(8):
# 			pixels[s * 64 + 0] = bits[(s >> 2) & 1]
# 			pixels[s * 64 + 1] = bits[(s >> 1) & 1]
# 			pixels[s * 64 + 2] = bits[(s >> 0) & 1]

# 		client.put_pixels(pixels)
# 		time.sleep(0.5)
