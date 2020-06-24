# PokemonBattleAI
CS486 AI Project Pokemon Battle Tree Search Algorithms 

Pokemon Specs

## How to run simulator
Do `python3 pokemonsim.py`. Also at the bottom of script, you can add your own or use the pre-made Pokemons (change `[POKEMON1OBJECT].fight([POKEMON2OBJECT])`).
Move numbers found in `moves.json`, Pokemon numbers found `pokemon.json`. Venusaur.fight(Mewtwo).


## Running AI stuff
(todo in the future)

# Status updates of project
```
June 24: 1v1 battling works (some move effects not implemented yet - still need more tests). Added some Pokemon to test around. Level 50 stats now automatically calculated for each Pokemon. 

June 23 (II): Status moves should be fully implemented now. Stat boosting moves should be fully implemented. Basic 1v1 mechanics should be complete. Basic non-damaging moves not in effect yet. Maybe test a bit more

June 23: Added confusion effects to moves. Mechanics for acrobatics/struggle implemented. Implemented recoil-on-miss mechanics. Confusion moves and mechanics seem to be working.

June 22: Added critical hit chances. Added mechanics for status conditions, and updated turn structuring. Did not fully test status moves yet (still have to update move effects)

June 19: Updated some special/physical distinguishment. Updated attack damage calculations a bit
```

Data files based from https://github.com/fonse/pokemon-battle

Backbone skeleton turn based battling and classes from https://github.com/cesaralvrz/Pokemon-Battle-Simulator

## Todo
Add some basic non-damaging move mechanics!
Then add trainer class for 3v3 - 6v6
Not too complex (no dig/fly mechanics and maybe no weather?)


### Translations to Keep Track?
Note: all will use level 50 defaults 0EV/0IV so just round down each calculation

normal 1
fighting 2
flying 3
poison 4
ground 5
rock 6
bug 7
ghost 8
steel 9
fire 10
water 11
grass 12
electric 13
psychic 14
ice 15
dragon 16
dark 17
fairy 18