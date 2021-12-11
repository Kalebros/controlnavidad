
def test_conversionNumeros(tableroInicial):
    """Testea la conversion de posiciones del tablero.

    Cada una de las tiras es de 12 leds, lo cual nos da un total de 36 leds.
    La idea es que, si el orden de los canales es [0,1,2,3,4,5,6,7],
    el cambiar los colores de los leds en orden nos dara una secuencia continua,
    en este caso si ponemos el valor de la tira como valor (0,0,1) para la primera,
    (0,0,2) para la segunda y (0,0,3) para la tercera, las posiciones deben de coincidir
    
    """

    #Comprobar que el tablero esta apagado

    for i in range(0,36):
        assert tableroInicial.getPixel(i) == (0,0,0)
    
    #Cambiar los valores en orden

    for i in range(0,3):
        for j in range(0,12):
            tableroInicial.setPixel(
                pos=(i*12) + j,
                value = (0,0,i+1)
            )
    
    for i in range(0,36):
        pixel = tableroInicial.getPixel(i)
        print(i,pixel)
        if i<12:
            assert pixel[2] == 1
        elif (i >= 12) and (i < 24):
            assert pixel[2] == 2
        else:
            assert pixel[2] == 3

    # GUARDAR EL ESTADO DEL TABLERO
    tablero_normal = tableroInicial.copyTablero()
    
    #Limpiar el tablero

    tableroInicial.tablero = [(0,0,0) for _ in range(0,36)]

    for i in range(0,36):
        assert tableroInicial.getPixel(i) == (0,0,0)
    
    tableroInicial.strips_order=[0,2,1,3,4,5,6,7]

    for i in range(0,3):
        for j in range(0,12):
            tableroInicial.setPixel(
                pos=(i*12) + j,
                value = (0,0,i+1)
            )
    
    for i in range(0,36):
        pixel = tableroInicial.getPixel(i)
        print(i,pixel)
        if i<12:
            assert pixel[2] == 1
        elif (i >= 12) and (i < 24):
            assert pixel[2] == 2
        else:
            assert pixel[2] == 3
    
    shifted_tablero = tableroInicial.copyTablero()

    print(f'PRIMERA: {tablero_normal}')
    print(f'SEGUNDA: {shifted_tablero}')

    assert len(shifted_tablero) == len(tablero_normal)

    for i in range(0,12):
        assert shifted_tablero[i] == tablero_normal[i]
    
    for i in range(12,36):
        assert shifted_tablero[i] != tablero_normal[i]
    
    for i in range(0,12):
        assert shifted_tablero[i] == (0,0,1)
    
    for i in range(12,24):
        assert shifted_tablero[i] == (0,0,3)
    for i in range(24,36):
        assert shifted_tablero[i] == (0,0,2)