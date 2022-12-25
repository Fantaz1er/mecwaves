import os
import matplotlib.pyplot as plt

from numpy import cos, pi, arange
from matplotlib import rcParams

const = int | float
value = int | float
plot = int | float | str
# SI System
meters = int | float
kilograms = int | float
seconds = int | float


class MechanicWave:
    """
    Waves - the process of oscillation, propagation in space over time.
     The main property of a wave: propagation without the transfer of matter.
      There are two types of perturbation orientations: longitudinal and transverse waves.
       The module provides for the use of only longitudinal waves and for determining the values of the plane (elastic) wave equation.
        ONLY FOR ELASTIC MEDIA.

    P.S.:
    for other types of waves the program is under development
    """

    def __init__(self):
        self.two_pi: float = 2 * pi

    @staticmethod
    def wavelength(velocity: value, period: value = None, periodicity: value = None) -> value:
        """Determination of the wavelength [m]"""
        return velocity * period if period else velocity / periodicity

    @staticmethod
    def velocity(wavelength: value, period: value = None, periodicity: value = None) -> value:
        """To determine the speed of wave propagation [m/s]"""
        return wavelength * periodicity if periodicity else wavelength / period

    @staticmethod
    def period(wavelength: value, velocity: value) -> value:
        """To determine the wave period [s]"""
        return wavelength / velocity

    @staticmethod
    def periodicity(wavelength: value, velocity: value) -> value:
        """To determine the wave periodicity [Hz or 1/s]"""
        return velocity / wavelength

    def omega(self, periodicity: value) -> value:
        """To determine the wave omega [Hz or 1/s]"""
        return self.two_pi * periodicity

    def phase(self, wavelength, x2: meters, x1: meters = 0) -> value:
        """To determine the wave phase"""
        return (self.two_pi / wavelength) * (x2 - x1)


class SpreadElasticMedia(MechanicWave):
    def __init__(self, **kwargs):
        super(SpreadElasticMedia, self).__init__()
        try:
            self.w: value = kwargs['omega']
        except KeyError:
            self.w: value = self.omega(kwargs['periodicity'])
        self.A: const = kwargs['AMPLITUDE']
        self.wavelength = kwargs['wavelength']


class PlaneWave(SpreadElasticMedia):
    """Plane wave equation.
        Determination of displacement of a plane wave.
            The propagation of a wave is not accompanied by the transfer of matter.
                "Displacement (S)" - the displacement of the particle of the medium from the equilibrium position,
                at which "x" is the equilibrium position of the particle
    """
    def __init__(self, x: meters, t: seconds, **kwargs):
        try:
            super(PlaneWave, self).__init__(AMPLITUDE=kwargs['AMPLITUDE'],
                                            wavelength=kwargs['wavelength'],
                                            omega=kwargs['omega'])
        except KeyError:
            super(PlaneWave, self).__init__(AMPLITUDE=kwargs['AMPLITUDE'],
                                            wavelength=kwargs['wavelength'],
                                            periodicity=kwargs['periodicity'])
        self.x = x
        self.t = t

    def __str__(self):
        return str(round(self.A * cos(self.w * self.t - self.phase(self.wavelength, self.x)), 5))


class DrawPlaneWavePlot(SpreadElasticMedia):
    @staticmethod
    def save_plot(name_file:  str = '', fmt: str = 'png'):
        path_plots = f'./plots/{fmt}'
        if not os.path.exists(path_plots):
            os.mkdir(path_plots)
        os.chdir(path_plots)
        plt.savefig(f'{name_file}.{fmt}')
        print('[+] Elastic wave plot is created')

    def __init__(self, x: meters, t: seconds, **kwargs):
        try:
            super(DrawPlaneWavePlot, self).__init__(AMPLITUDE=kwargs['AMPLITUDE'],
                                                    wavelength=kwargs['wavelength'],
                                                    omega=kwargs['omega'])
        except KeyError:
            super(DrawPlaneWavePlot, self).__init__(AMPLITUDE=kwargs['AMPLITUDE'],
                                                    wavelength=kwargs['wavelength'],
                                                    periodicity=kwargs['periodicity'])

        rcParams['font.family'] = 'Arial', 'Arial', 'Tahoma'
        rcParams['font.fantasy'] = 'Arial'

        plt.figure(figsize=(5, 2.7))

        fig, ax = plt.subplots()

        ox = arange(0.0, t, 0.01)
        oy = self.A * cos(self.w * ox - self.phase(self.wavelength, x))

        ax.plot(ox, oy, lw=2)
        ax.grid()

        plt.title(f'Elastic Wave Plot\nS(x,t)={self.A}×cos({self.w / pi}π×{t} - 2π/{self.wavelength}×{x})')
        ax.set_xlabel('Time [s]', fontweight='bold')
        ax.set_ylabel('Amplitude', fontweight='bold')

        self.save_plot('elastic_wave_plot')


if __name__ == "__main__":
    # waves = MechanicWave()
    # print(waves.wavelength(12.2, periodicity=2))
    # print(waves.periodicity(6.1, 12.2))
    # print(PlaneWave(x=9, t=2, wavelength=10, AMPLITUDE=2, periodicity=3))
    DrawPlaneWavePlot(x=9, t=2, wavelength=10, AMPLITUDE=2, omega=6*pi)
