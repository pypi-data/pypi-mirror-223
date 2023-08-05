# PyMulti (Fun) - Init

''' This is the __init__.py file. '''

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
import os
import webbrowser

# Function 1 - Game
def game(name):
    # List of Games
    games = ["ant", "bagels", "bounce", "cannon", "connect", "crypto", "fidget", "flappy", "guess", "life", "maze", "memory", "minesweeper", "pacman", "paint", "pong", "simonsays", "snake", "tictactoe", "tiles", "tron", "typing", "illusion", "tennis", "rockpaperscissors"]

    # Checking the Data Type of "name"
    if (isinstance(name, str)):
        # Checking if "name" is Valid
        if (name in games):
            # Playing the Game
            if (name in ["tennis", "rockpaperscissors"]):
                if (name == "tennis"):
                    # Opening the "Tennis" Game
                    webbrowser.open("https://anikethchavare.vercel.app/tennis-game")
                elif (name == "rockpaperscissors"):
                    # Opening the "Rock Paper Scissors" Game
                    webbrowser.open("https://anikethchavare.vercel.app/rock-paper-scissors")
            else:
                # Playing the "freegames" Game
                os.system("python -m freegames." + name)
        else:
            raise Exception("The 'name' argument must be a valid game's name. The available games are:\n\n" + str(games))
    else:
        raise TypeError("The 'name' argument must be a string.")

# Function 2 - Horoscope
'''def horoscope(zodiac_sign="", date=""):
    # Variables
    zodiacSigns = {"Aries":1, "Taurus":2, "Gemini":3, "Cancer":4, "Leo":5, "Virgo":6, "Libra":7, "Scorpio":8, "Sagittarius":9, "Capricorn":10, "Aquarius":11, "Pisces":12}
    url1 = "https://horoscope.com/us/horoscopes/general/horoscope-general-daily-{0}.aspx?sign={1}"

    # Checking the Data Type of "zodiac_sign"
    if (isinstance(zodiac_sign, str)):
        # Checking the Data Type of "date"
        if (isinstance(date, str)):
            # Checking if "zodiac_sign" is Valid
            if (zodiac_sign.lower() in zodiacSigns.keys()):
                return 1
            else:
                raise Exception("The 'zodiac')  
        else:
            raise TypeError("The 'date' argument must be a string.")
    else:
        raise TypeError("The 'zodiac_sign' argument must be a string.")'''