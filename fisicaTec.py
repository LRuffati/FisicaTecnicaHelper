class Temperature:
    def __init__(self, **kwargs):
        if 'kelvin' in kwargs:
            self._kelvin = kwargs['kelvin']
            return
        if 'celsius' in kwargs:
            self._kelvin = 273 + kwargs['celsius']
            return

        raise KeyError()

    def kelvin(self):
        return self._kelvin

    def celsius(self):
        return self._kelvin - 273.0

    def __add__(self, other):
        if type(other) is Temperature:
            k = self.kelvin() + other.kelvin()
            return Temperature(kelvin=k)
        raise TypeError()

    def __mul__(self, other):
        return Temperature(kelvin=(other * (self.kelvin())))

    def __rmul__(self, other):
        return self * other

    def __repr__(self):
        return "Temperature: " + str(self.kelvin()) + "K"


class Pressure():
    def __init__(self, **kwargs):
        if 'pascal' in kwargs:
            self._pascal = kwargs['pascal']
            return
        if 'bar' in kwargs:
            self._pascal = 10 ** 5 * kwargs['bar']
            return

        raise KeyError()

    def pascal(self):
        return self._pascal

    def bar(self):
        return self._pascal / (10 ** 5)

    def __add__(self, other):
        if type(other) is Temperature:
            k = self.pascal() + other.pascal()
            return Pressure(pascal=k)
        raise TypeError()

    def __mul__(self, other):
        return Pressure(pascal=(other * (self.pascal())))

    def __rmul__(self, other):
        return self * other

    def __repr__(self):
        return "Pressure: " + str(self.pascal()) + "Pa"


class Volume:
    def __init__(self,
                 volume=None,  # in m^3
                 r_star=None,  # in J / (kg * K)
                 moles=None,  # in kmoles
                 mass=None,  # in kg
                 temp=None,  # Temperature
                 press=None,  # Pressure
                 mol_ma=None):  # in kg/kmol, molar mass
        if volume is not None:
            self._volume = volume
            return

        if r_star is None:
            if moles is not None:
                pass
            elif mol_ma is None:
                raise KeyError("Not enough information, no r* and no molar mass")

            r_star = 8314.0 / mol_ma

        JoverKel = None
        if moles is not None:
            JoverKel = 8314.0 * moles
        else:
            if mass is None:
                raise KeyError("Not enough information, no moles and no mass")
            else:
                JoverKel = r_star * mass

        if temp is None:
            raise KeyError("No temperature to determine volume")

        if press is None:
            raise KeyError("No pressure to determine volume")

        self._volume = JoverKel * temp.kelvin() / press.pascal()

    def cubic_meters(self):
        return self._volume


class Gas:
    def c_p(self):
        pass

    def c_v(self):
        pass


class IdealGas(Gas):
    """
    Contains information on the values
    """

    def __init__(self, c_v=None, c_p=None):
        pass


class State:
    """
    The state of a gas in the thermodynamics plane

    Should at least have:
        + pressure
        + volume
        + temperature
        + internal energy
    """

    def __init__(self,
                 gas,
                 temperature=None,
                 volume=None,
                 pressure=None,
                 entropy=None,
                 enthalpy=None,
                 moles=None,
                 mass=None,
                 internal_energy=None):
        pass

    def isocore(self, target_press=None, target_temp=None):
        pass

    def isobare(self, target_temp=None, target_vol=None):
        pass

    def isotherm(self, target_press=None, target_vol=None):
        pass

    def adiabatic(self, target_press=None, target_vol=None, target_temp=None):
        pass


class Transformation:
    def __init__(self, state_1, state_2, d_s, d_h, work):
        pass
