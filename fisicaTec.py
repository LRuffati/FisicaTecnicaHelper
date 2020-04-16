from math import log

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


class Transformation:
    def __init__(self, 
                 d_press=None, 
                 d_temp=None,
                 d_vol=None, 
                 work=None, 
                 heat=None,
                 d_s=None,
                 d_h=None):
        self.d_press = d_press
        self.d_temp = d_temp
        self.d_vol = d_vol
        self.work=work
        self.heat=heat
        self.d_s = d_s
        self.d_h = d_h

    def __repr__(self):
        s = []
        s.append(f'pressure change: {self.d_press}')
        s.append(f'temperature change: {self.d_temp}')
        s.append(f'volume change: {self.d_vol}')
        s.append(f'work: {self.work}')
        s.append(f'heat: {self.heat}')
        s.append(f'change entropy: {self.d_s}')
        s.append(f'change hentalpy: {self.d_h}')
        return '\n'.join(s)

def delta_entropy_perfect_gas(cv=None, cp=None, t_pair=None, 
                              v_pair=None, p_pair=None, r_star=None):
    if not any([cp is None, cv is None, v_pair is None, p_pair is None]):
        return (cp*log(v_pair[1]/v_pair[0])) + (cv*log(p_pair[1]/p_pair[0]))
    if not any([cp is None, r_star is None, t_pair is None, p_pair is None]):
        return (cp*log(t_pair[1]/t_pair[0])) - (r_star*log(p_pair[1]/p_pair[0]))
    if not any([r_star is None, cv is None, v_pair is None, t_pair is None]):
        return (cv*log(t_pair[1]/t_pair[0])) + (r_star*log(v_pair[1]/v_pair[0]))

class IdealGasTransforms:
    @staticmethod
    def isotherm():
        """

        """
        pass

    @staticmethod
    def isobare():
        pass

    @staticmethod
    def isocore():
        pass

    @staticmethod
    def adiabatic():
        pass
