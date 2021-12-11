# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Any, ClassVar, List, Tuple

import copy

import logging


@dataclass
class LEDSControl:

    size: int
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

        LEDSControl.log.debug(f'Pixel {pos} a valor {value}')
        self.__tablero[pos] = value
        return self.__tablero[pos]

    def getPixel(self,pos: int) -> Tuple[int,int,int]:
        """Devuelve el valor del pixel en la posición indicada"""

        return self.__tablero[pos]
