# Degrees converter

Simple library that converts temperature from one unit to another one(e.g. from Celsius to Fahrenheit).

Every method of the class *Converter* returns a float rounded to the second decimal figure.

## Usage

Import the class *Converter* and create an instance of the class *Converter*:

```Python
from degreesConversion.converter import Converter

conv = Converter()
```

and then call the methods of the instance with an int or a float value:

```Python
print(conv.celFah(0))
# output: 32.0
```

The methods can accept a string as argument if it's still a number:

```Python
print(conv.celFah("0"))
# output: 32.0

print(conv.celFah("zero"))
# output: Couldn't convert string to float.
```
