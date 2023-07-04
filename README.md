# Autoclicker

This is a simple Python program to automate mouse clicks, with some extra features for click randomisation.

## Features
* Set the time duration between clicks (this will default to as fast as possible if left blank or if the input is invalid)
* Choose a hotkey to start and stop the autoclicker
* Easily the position of the click anywhere on screen (this will default to (0,0), ie the top left corner) using the "set position" button
* Toggle a random time offset, which will randomly add or subtract up to 1 second of extra delay between clicks
* Toggle a random positional offset, which will randomly move the click position by up to 5 units in any direction 

## Issues
* The click position coordinates are currently unchecked - entering non-numerical values will cause a crash!
