import unittest

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


def pelmenator(i):
    return i ** 2

class TestPelm(unittest.TestCase):
    def test_pelmenator(self):
        self.assertEqual(pelmenator(-2),4)



class TestZopa(unittest.TestCase):
    def test_zopa_zero(self):
        self.assertEqual(len(zopa(1,2,1)), 1)

    def test_zopa_negative(self):
        self.assertEqual(len(zopa(1,2,3)), 0)
    

    def test_zopa_positivo(self):
        self.assertEqual(len(zopa(2,5,1)), 2)
    
    def test_zopa_proverka(self):
        self.assertEqual(zopa(3,9,6), [-2,-1])
    
    def test_zopa_exeption(self):
        with self.assertRaises(ValueError):
            zopa(0, 1,1)

unittest.main() 
