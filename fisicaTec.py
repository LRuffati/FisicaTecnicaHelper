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
        + a method to generate PV and TS graphs
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
        self.gas = gas
        if temperature is not None:
            self.temperature = temperature

        if volume is not None:
            self.volume = volume

        if pressure is not None:
            self.pressure = pressure

        if entropy is not None:
            self.entropy = entropy

        if enthalpy is not None:
            self.enthalpy = enthalpy

        if moles is not None:
            self.moles = moles

        if mass is not None:
            self.mass = mass

        if internal_energy is not None:
            self.internal_energy = internal_energy

    def get_enthalpy(self):
        if self.enthalpy is None:
            self.enthalpy = self.internal_energy + (self.volume + self.pressure)
        return self.enthalpy

    def get_pv(self):
        pass

    def get_ts(self):
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
    def __init__(self, state_1, state_2, d_sq, d_sirr, d_h, work):
        self.d_sirr = d_sirr
        self.d_sq = d_sq
        self.state_1 = state_1
        self.state_2 = state_2

    def is_rev(self):
        if self.d_sirr == 0:
            return True

    def is_adiab(self):
        if self.d_sq == 0:
            return True

    def get_entrop(self):
        if self.state_1.entropy is None or self.state_2.entropy is None:
            return self.d_sirr + self.d_sq # se non avessimo uno dei due valori dovremmo considerare la legge coi logaritmi, che casino scegliere le variabili
        else:
            return self.state_2.entropy - self.state_1.entropy
