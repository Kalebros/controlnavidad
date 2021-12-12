# -*- coding: utf-8 -*-

from dataclasses import dataclass,field
from typing import Any, Tuple

import math

@dataclass
class Pixel:

    rgb: Tuple[int,int,int] = (0,0,0)

    @property
    def hsl(self) -> Tuple[float,float,float]:
        """Devuelve el valor RGB en el espacio HSL
        
        El espacio HSL (Hue, Saturation, Lightness) permite
        ajustar mejor el brillo y el fading entre colores,
        ya que solo es necesario ajustar el canal de lightness hacia arria o hacia abajo
        """

        r = float(self.rgb[0] / 255.0)
        g = float(self.rgb[1] / 255.0)
        b = float(self.rgb[2] / 255.0)

        high = max(r, g, b)
        low = min(r, g, b)
        h, s, l = ((high + low) / 2,)*3

        if high == low:
            h = 0.0
            s = 0.0
        else:
            d = high - low
            s = d / (2 - high - low) if l > 0.5 else d / (high + low)
            h = {
                r: (g - b) / d + (6 if g < b else 0),
                g: (b - r) / d + 2,
                b: (r - g) / d + 4,
            }[high]
            h /= 6

        return (h, s, l)
    
    def setLightness(self, l: float) -> None:
        """Cambia la luminosidad"""

        hsl_mode: Tuple[float, float, float] = self.hsl

        hsl_corregido: Tuple[float,float,float] = [hsl_mode[0],hsl_mode[1],l]

        self.rgb = self.__hsl_to_rgb(hsl_corregido)
    
    def fadeLightness(self,value: float) -> float:
        """Reduce la luminosidad un valor concreto
        
        El valor concreto debe de estar entre 0.0 y 1.0
        """

        hsl_mode: Tuple[float, float, float] = self.hsl

        nValue: float = hsl_mode[2] - value
        if nValue < 0.0:
            nValue = 0.0

        hsl_corregido: Tuple[float,float,float] = [hsl_mode[0],hsl_mode[1],nValue]

        self.rgb = self.__hsl_to_rgb(hsl_corregido)

        return nValue
    
    def incrementLightness(self,value: float) -> float:
        """Aumenta la luminosidad un valor concreto
        
        El valor concreto debe de estar entre 0.0 y 1.0
        """
        hsl_mode: Tuple[float, float, float] = self.hsl

        nValue: float = hsl_mode[2] + value
        if nValue > 1.0:
            nValue = 1.0

        hsl_corregido: Tuple[float,float,float] = [hsl_mode[0],hsl_mode[1],nValue]

        self.rgb = self.__hsl_to_rgb(hsl_corregido)

        return nValue


    def __hsl_to_rgb(self, hsl: Tuple[float,float,float]) -> Tuple[int,int,int]:
        """Convierte de HSL a RGB"""

        h =hsl[0]
        s = hsl[1]
        l = hsl[2]

        if s == 0:
            r, g, b = l, l, l
        else:
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r = self.__hue_to_rgb(p, q, h + 1/3)
            g = self.__hue_to_rgb(p, q, h)
            b = self.__hue_to_rgb(p, q, h - 1/3)

        return (round(r * 255.0), round(g*255.0), round(b*255.0))
    
    def __hue_to_rgb(self, p: Any, q: Any, t: Any) -> Any:
        """Convierte el tono a RGB"""

        t += 1 if t < 0 else 0
        t -= 1 if t > 1 else 0
        if t < 1/6: return p + (q - p) * 6 * t
        if t < 1/2: return q
        if t < 2/3: p + (q - p) * (2/3 - t) * 6
        return p