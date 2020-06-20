# PokemonBattleAI
CS486 AI Project Pokemon Battle Tree Search Algorithms 

Pokemon Specs

##How to run simulator
python3 pokemonsim.py
Will reorganize things and update CLI interface in the future

##Running AI stuff
(todo in the future)

# Status
Starting to integrate json files to grab types and moves data. Just a simple skeleton so far. No moves distinguishment/statuses/effects/teams.

Data files based from https://github.com/fonse/pokemon-battle

Backbone skeleton turn based battling and classes from https://github.com/cesaralvrz/Pokemon-Battle-Simulator


### Translations to Keep Track?
Note: all will use level 50 defaults 0EV/0IV so just round down each calculation
HP: [(2*Base+IV+EV/4+100)*Level/100+10]*Nature
Everything else: [(2*Base+IV+EV/4)*Level/100+5]*Nature


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



- use damage calculator algorithm
- Will have secondary effects (burn/paralysis/poison/freeze/sleep/confusion)
