from pixels import Pixel

def test_conversiones():

    p: Pixel = Pixel((255,255,255))

    assert p.rgb == (255,255,255)

    print(p.hsl)

    p.setLightness(0.5)

    print(p.rgb)
    print(p.hsl)

    assert None is not None