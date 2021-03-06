# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Any, ClassVar, List, Tuple

import copy

import logging


@dataclass
class LEDSControl:

    size: int
    strip_size: int = 64
    initial_tuple: Tuple[int,int,int] = (0,0,0)
    __tablero: List[Tuple[int,int,int]] = field(default_factory = list,init=False,repr=False)
    strips_order: List[int] = field(default_factory=list,init=False)
    log: ClassVar[logging.log] = field(init=False,default = None)
    log_level: ClassVar[Any] = logging.DEBUG

    def __post_init__(self):
        self.__tablero = [self.initial_tuple for _ in range(0,self.size)]
        self.strips_order = [0,1,2,3,4,5,6,7]

        if LEDSControl.log is None:
            LEDSControl.log = logging.getLogger('LEDSControl')
            LEDSControl.log.setLevel(LEDSControl.log_level)
    
    @classmethod
    def loggingLevel(self,value: Any) -> None:
        """Establece el nivel de logging de la clase"""

        if LEDSControl.log is not None:
            LEDSControl.log.setLevel(value)
        LEDSControl.log_level = value

    @property
    def tablero(self) -> List[Tuple[int,int,int]]:
        """Devuelve el tablero de pixels del panel"""
        return self.__tablero
    
    @tablero.setter
    def tablero(self,value: List[Tuple[int,int,int]]) -> None:
        """Cambia el tablero de pixels del panel"""
        self.__tablero = value
        self.size = len(self.__tablero)
    
    def copyTablero(self) -> List[Tuple[int,int,int]]:
        """Devuelve una copia del tablero actual"""

        return copy.copy(self.__tablero)
    
    def setPixel(self,pos: int, value: Tuple[int,int,int]) -> Tuple[int,int,int]:
        """Cambia el valor del pixel y devuelve el nuevo valor"""

        # LEDSControl.log.debug(f'Pixel {pos} a valor {value}')
        
        nPos = self.__conversor_posicion(pos)
        self.__tablero[nPos] = value
        return self.__tablero[nPos]
    
    def setTableroToPixel(self,pixel: Tuple[int,int,int]) -> None:
        """Limpia el tablero completo a un color determinado"""
        self.__tablero = [pixel for _ in range(0,self.size)]
    
    def __conversor_posicion(self,position: int) -> int:
        """Devuelve la posicion reconvertida seg??n las tiras en los canales"""
        strip_correspondiente: int  = position // self.strip_size 

        channel_strip: int = self.strips_order[strip_correspondiente]

        newPosition: int = (position - (strip_correspondiente * self.strip_size)) + (channel_strip * self.strip_size)

        LEDSControl.log.debug(f'Pos: {position}, tira: {strip_correspondiente}, reasignado a {channel_strip}, posicion devuelta: {newPosition}')

        # ## ELIMINAR CUANDO SE TERMINE LA DEPURACION
        # newPosition = position

        return newPosition

    def getPixel(self,pos: int) -> Tuple[int,int,int]:
        """Devuelve el valor del pixel en la posici??n indicada"""

        nPos = self.__conversor_posicion(pos)
        return self.__tablero[nPos]
