# Version 5 of Algo
# Updated from v4

# Note: this file is modified from the README.md file provided by organizer of tournament.
 
## File Overview

```
v5
 │
 ├──gamelib*
 │   ├──__init__.py*
 │   ├──algocore.py*
 │   ├──game_map.py*
 │   ├──game_state.py*
 │   ├──navigation.py*
 │   ├──tests.py*
 │   ├──unit.py*
 │   └──util.py*
 │
 ├──algo_strategy.py
 ├──documentation*
 ├──README.md*
 ├──run.ps1*
 ├──unit_locations.py
 └──run.sh*
```

### Creating an Algo

The `algo_strategy.py` file is the file holding the main algorithm.
The 'unit_location.py' file is the file holding all location coordinates and the building and  ordering information used in 'algo_strategy.py'.  
Upload entire v5 folder to terminal for algo upload. 

### `algo_strategy.py`

This file contains the `AlgoStrategy` class modified to implement our strategy.

The `on_game_start` method is modified for inital setup.

### `documentation`

A directory containing the sphinx generated programming documentation, as well as the files required
to build it. You can view the docs by opening index.html in documents/_build.
You can remake the documentation by running 'make html' in the documentation folder.
You will need to install sphinx for this command to work.

### `run.sh`

A script that contains logic to invoke your code. You do not need to run this directly.
See the 'scripts' folder in the Starterkit for information about testing locally.

### `run.ps1`

A script that contains logic to invoke your code. You shouldn't need to change
this unless you change file structure or require a more customized process
startup.

### `gamelib/__init__.py`

This file tells python to treat `gamelib` as a bundled python module. This
library of functions and classes is intended to simplify development by
handling tedious tasks such as communication with the game engine, summarizing
the latest turn, and estimating paths based on the latest board state.

### `gamelib/algocore.py`

This file contains code that handles the communication between your algo and the
core game logic module. You shouldn't need to change this directly. Feel free to 
just overwrite the core methods that you would like to behave differently. 

### `gamelib/game_map.py`

This module contains the `GameMap` class which is used to parse the game state
and provide functions for querying it. 

### `gamelib/navigation.py`

Functions and classes used to implement pathfinding.

### `gamelib/tests.py`

Unit tests. You can write your own if you would like, and can run them using
the following command:

    python3 -m unittest discover

### `gamelib/unit.py`

This module contains the `GameUnit` class which holds information about a Unit.

### `gamelib/util.py`

Helper functions and values that do not yet have a better place to live.

## Strategy Overview

Start with a 'basic-v2' defensive configuration with mild scout attacks. Once accumulated enough SP (threshold 90), swich to an advanced configuration. 
Advanced configuration creates two "self-destruct" sinks to attract enemy attacks and a corridor-like-path to trengthen our attack while defending opponent attacks(corridor only appears when it is our turn to attack, full defense configuration when not attacking). If SP drops below 70, switch back to basic configuration. 


Difference from the v4 algos:
- Defined new defense v2: sending two waves of scouts if there are enough scouts, otherwise just send one big wave of scouts for attack. 
- Uses 'Basic_v2' starting configuration. Blocking walls on one side, allowing attacks and maximize defnese on the other side.  
-Different offense mp threshold and variable offence_sp_counter delcared for tracking to allow an attack when mp is enough but sp is not. 
