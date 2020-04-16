def cal_to_joule(cal):
    return cal*4.1858

def interpolation_linear(pair_low, pair_high, target):
    x_low, y_low = pair_low
    x_hig, y_hig = pair_high
    return y_low + ((y_hig-y_low)/(x_hig-x_low))*(target-x_low)

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


class Pressure:
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
                spec_vol = True
            else:
                spec_vol = False
                JoverKel = r_star * mass

        if temp is None:
            raise KeyError("No temperature to determine volume")

        if press is None:
            raise KeyError("No pressure to determine volume")

        if not spec_vol:
            self._volume = JoverKel * temp.kelvin() / press.pascal()
        else:
            self._spec_vol = r_star * temp.kelvin() / press.pascal()

    def cubic_meters(self):
        return self._volume

    def specific_vol(self):
        return self._spec_vol

    def __repr__(self):

        if hasattr(self, '_volume'):
            return "Volume: "+ str(self._volume)
        else:
            return "Specific volume: " + str(self._spec_vol)

