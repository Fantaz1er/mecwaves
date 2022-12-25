from mecwaves import PlaneWave
from timeit import timeit
from numpy import pi

if __name__ == '__main__':
    number = 120
    print(timeit(lambda: PlaneWave(x=9, t=2, wavelength=10, AMPLITUDE=0.1, omega=2*pi), number=number))  # best
    print(timeit(lambda: PlaneWave(x=9, t=2, wavelength=10, AMPLITUDE=0.1, periodicity=1), number=number))
