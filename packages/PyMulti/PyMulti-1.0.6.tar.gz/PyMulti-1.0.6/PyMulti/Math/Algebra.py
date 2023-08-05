# PyMulti (Math) - Algebra

''' This is the "Algebra" module. '''

'''
Copyright 2023 Aniketh Chavare

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# Imports
import math

# Function 1 - Find Discriminant (Quadratic Equations)
def find_discriminant(a, b, c):
    # Checking the Data Type of "a"
    if (isinstance(a, (int, float))):
        # Checking the Data Type of "b"
        if (isinstance(b, (int, float))):
            # Checking the Data Type of "c"
            if (isinstance(c, (int, float))):
                # Returning the Discriminant
                return (b**2) - (4 * a * c)
            else:
                raise TypeError("The 'c' argument must be an integer or a float.")
        else:
            raise TypeError("The 'b' argument must be an integer or a float.")
    else:
        raise TypeError("The 'a' argument must be an integer or a float.")

# Function 2 - Find Roots (Quadratic Equations)
def find_roots(a, b, c):
    # Checking the Data Type of "a"
    if (isinstance(a, (int, float))):
        # Checking the Data Type of "b"
        if (isinstance(b, (int, float))):
            # Checking the Data Type of "c"
            if (isinstance(c, (int, float))):
                # Discriminant
                discriminant = find_discriminant(a, b, c)

                # Alpha & Beta
                alpha = (-b + math.sqrt(discriminant)) / (2 * a)
                beta = (-b - math.sqrt(discriminant)) / (2 * a)

                # Returning the Roots
                return (alpha, beta)
            else:
                raise TypeError("The 'c' argument must be an integer or a float.")
        else:
            raise TypeError("The 'b' argument must be an integer or a float.")
    else:
        raise TypeError("The 'a' argument must be an integer or a float.")