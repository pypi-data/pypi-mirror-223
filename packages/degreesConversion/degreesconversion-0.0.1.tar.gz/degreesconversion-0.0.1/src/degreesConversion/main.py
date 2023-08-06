class Converter:
    error = "Couldn't convert string to float."

    def celFah(self, celsius: int | float) -> float | str:
        try:
            celsius = float(celsius)
            fahrenheit = round((celsius * (9 / 5)) + 32, 2)
            return fahrenheit
        except ValueError:
            return self.error

    def fahCel(self, fahrenheit: int | float) -> float | str:
        try:
            fahrenheit = float(fahrenheit)
            celsius = round((fahrenheit - 32) * (5 / 9), 2)
            return celsius
        except ValueError:
            return self.error

    def celKel(self, celsius: int | float) -> float | str:
        try:
            celsius = float(celsius)
            kelvin = round(celsius + 273.15, 2)
            return kelvin
        except ValueError:
            return self.error

    def kelCel(self, kelvin: int | float) -> float | str:
        try:
            kelvin = float(kelvin)
            celsius = round(kelvin - 273.15, 2)
            return celsius
        except ValueError:
            return self.error

    def fahKel(self, fahrenheit: int | float) -> float | str:
        try:
            fahrenheit = float(fahrenheit)
            kelvin = round((fahrenheit - 32) * (5 / 9) + 273.15, 2)
            return kelvin
        except ValueError:
            return self.error

    def kelFah(self, kelvin: int | float) -> float | str:
        try:
            kelvin = float(kelvin)
            fahrenheit = round((kelvin * 9 / 5) - 459.67, 2)
            return fahrenheit
        except ValueError:
            return self.error
