import pytest

from controleds import LEDSControl

@pytest.fixture(scope = 'module')
def tableroInicial():

    tablero: LEDSControl = LEDSControl(size = 36,strip_size = 12)

    return tablero