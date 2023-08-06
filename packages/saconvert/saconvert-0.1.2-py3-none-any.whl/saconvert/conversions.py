# conversions/convert.py

class LengthConverter:
    def __init__(self, value, unit):
        """
        Initialize the LengthConverter object.

        Parameters:
            value (float): The length value to be converted.
            unit (str): The initial unit of the length (e.g., "Meter", "Light Year").
        """
        self.value = value
        self.unit = unit

    def to_meter(self):
        """
        Convert the length to meters.

        Returns:
            float: The length value in meters.
        """
        if self.unit == "Meter":
            return self.value
        elif self.unit == "Kilometer":
            return self.value * 1000
        elif self.unit == "Centimeter":
            return self.value / 100
        elif self.unit == "Millimeter":
            return self.value / 1000
        elif self.unit == "Micrometer":
            return self.value / 1e6
        elif self.unit == "Nanometer":
            return self.value / 1e9
        elif self.unit == "Mile":
            return self.value * 1609.34
        elif self.unit == "Yard":
            return self.value * 0.9144
        elif self.unit == "Foot":
            return self.value * 0.3048
        elif self.unit == "Inch":
            return self.value * 0.0254
        elif self.unit == "Light Year":
            return self.value * 9.461e15
        else:
            raise ValueError("Invalid unit")

    def to_kilometer(self):
        """
        Convert the length to kilometers.

        Returns:
            float: The length value in kilometers.
        """
        return self.to_meter() / 1000

    def to_centimeter(self):
        """
        Convert the length to centimeters.

        Returns:
            float: The length value in centimeters.
        """
        return self.to_meter() * 100

    def to_millimeter(self):
        """
        Convert the length to millimeters.

        Returns:
            float: The length value in millimeters.
        """
        return self.to_meter() * 1000

    def to_micrometer(self):
        """
        Convert the length to micrometers.

        Returns:
            float: The length value in micrometers.
        """
        return self.to_meter() * 1e6

    def to_nanometer(self):
        """
        Convert the length to nanometers.

        Returns:
            float: The length value in nanometers.
        """
        return self.to_meter() * 1e9

    def to_mile(self):
        """
        Convert the length to miles.

        Returns:
            float: The length value in miles.
        """
        return self.to_meter() / 1609.34

    def to_yard(self):
        """
        Convert the length to yards.

        Returns:
            float: The length value in yards.
        """
        return self.to_meter() / 0.9144

    def to_foot(self):
        """
        Convert the length to feet.

        Returns:
            float: The length value in feet.
        """
        return self.to_meter() / 0.3048

    def to_inch(self):
        """
        Convert the length to inches.

        Returns:
            float: The length value in inches.
        """
        return self.to_meter() / 0.0254

    def to_light_year(self):
        """
        Convert the length to light years.

        Returns:
            float: The length value in light years.
        """
        return self.to_meter() / 9.461e15


# Weight

class WeightConverter:
    def __init__(self, value, unit):
        """
        Initialize the WeightConverter object.

        Parameters:
            value (float): The weight value to be converted.
            unit (str): The initial unit of the weight (e.g., "Kilogram", "Pound").
        """
        self.value = value
        self.unit = unit

    def to_kilogram(self):
        """
        Convert the weight to kilograms.

        Returns:
            float: The weight value in kilograms.
        """
        if self.unit == "Kilogram":
            return self.value
        elif self.unit == "Gram":
            return self.value / 1000
        elif self.unit == "Milligram":
            return self.value / 1e6
        elif self.unit == "Pound":
            return self.value * 0.453592
        elif self.unit == "Ounce":
            return self.value * 0.0283495
        elif self.unit == "Carat":
            return self.value * 0.0002
        elif self.unit == "Atomic Mass Unit":
            return self.value * 1.66054e-27
        else:
            raise ValueError("Invalid unit")

    def to_gram(self):
        """
        Convert the weight to grams.

        Returns:
            float: The weight value in grams.
        """
        return self.to_kilogram() * 1000

    def to_milligram(self):
        """
        Convert the weight to milligrams.

        Returns:
            float: The weight value in milligrams.
        """
        return self.to_kilogram() * 1e6

    def to_pound(self):
        """
        Convert the weight to pounds.

        Returns:
            float: The weight value in pounds.
        """
        return self.to_kilogram() / 0.453592

    def to_ounce(self):
        """
        Convert the weight to ounces.

        Returns:
            float: The weight value in ounces.
        """
        return self.to_kilogram() / 0.0283495

    def to_carat(self):
        """
        Convert the weight to carats.

        Returns:
            float: The weight value in carats.
        """
        return self.to_kilogram() / 0.0002

    def to_atomic_mass_unit(self):
        """
        Convert the weight to atomic mass units.

        Returns:
            float: The weight value in atomic mass units.
        """
        return self.to_kilogram() / 1.66054e-27

    def to_ton(self):
        """
        Convert the weight to U.S. tons (short tons).

        Returns:
            float: The weight value in U.S. tons (short tons).
        """
        return self.to_kilogram() / 907.185
