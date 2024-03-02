import pytest

def zopa(a,b,c):
    if a==0:
        raise ValueError

    D=b**2-4*(a*c)
    if D<0:
        return []
    elif D==0:
        return [-b/(2*a)]
    else:
        x1 = (-b - D**0.5)/(2*a)
        x2 = (-b + D**0.5)/(2*a)
        return sorted([x1, x2])


def test_zopa_zero():
    assert len(zopa(1,2,1)) == 1, 'У дискриминанта другое количество решений'


def test_zopa_negative():
    assert len(zopa(1,2,3)) == 0, 'У дискриминанта другое количество решений'  


def test_zopa_positivo():
    assert len(zopa(2,5,1)) == 2, 'У дискриминанта другое количество решений'

def test_zopa_proverka():
    assert zopa(3,9,6) == [-2, -1], 'Не вышло'

def test_zopa_exeption():
    for b in range(100):
        for c in range(100):
            with pytest.raises(ValueError):
                zopa(0, b, c)
