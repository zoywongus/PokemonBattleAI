import time
import numpy as np
import sys
import enum
import json
import math
import random

movejson = typesjson = pokemonjson = {}

# def make_effect_class():


# class Move:

#     def __init__(self, id):
#         if not(id in MOVEJSON):
#             print('move not found')

class Status(enum.Enum):
    none = 0
    sleep = 1
    poison = 2
    paralysis = 3
    burn = 4
    freeze = 5

##TODO ADD ACCURACY STUFF
def calculate_damage(Pokemon1, Pokemon2, move_info, move_effectiveness):
    power = move_info['power']
    attack = Pokemon1.attack
    defense = Pokemon2.defense
    if move_info['damage_class'] == 'special':
        attack = Pokemon1.spattack
        defense = Pokemon2.spdefense

    critical = weather = burnstatus = other = stab = 1
    if move_info['type'] in pokemonjson[Pokemon1.id]['types']:
        stab = 1.5

    modifier = weather * critical * burnstatus * (random.randint(85,100)*0.01) * stab * move_effectiveness * other
    damage = (((22*power*attack/defense) / 50) + 2) * modifier

    return damage

# Delay en cada prit
def delay_print(s):
    # Imprimir personaje uno por uno
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)

# Creation Pokemon
class Pokemon:
    def __init__(self, nameid, types, moves, EVs):
        # Guardar variables como atributos
        self.id = nameid
        self.name = pokemonjson[nameid]['name']
        self.types = pokemonjson[nameid]['types']
        self.moves = moves
        self.attack = EVs['ATTACK']
        self.spattack = EVs['SPATTACK']
        self.defense = EVs['DEFENSE']
        self.spdefense = EVs['SPDEFENSE']
        self.speed = EVs['SPEED']
        self.health = EVs['HP']
        self.confusion = False
        self.status = Status.none

        #might change up something to avoid this
        self.types[0] = str(self.types[0])
        if len(self.types) > 1:
            self.types[1] = str(self.types[1])



    def fight(self, Pokemon2):
        # Permiso para que dos Pokémon combatan

        # Texto de la pelea
        print("-----POKEMONE BATTLE-----")
        print("Pokemon 1:", self.name)
        print("LVL/ 50")
        print("TYPE/", (typesjson[self.types[0]]['name']))
        print("HP/", self.health)
        print("ATTACK/", self.attack)
        print("DEFENSE/", self.defense)
        print("SP ATTACK/", self.spattack)
        print("SP DEFENSE/", self.spdefense)
        print("SPEED/", self.speed)
        print("\nVS")
        print("Pokemon 2:", Pokemon2.name)
        print("LVL/ 50\n")
        print("TYPE/", (typesjson[Pokemon2.types[0]]['name']))
        print("HP/", Pokemon2.health)
        print("ATTACK/", Pokemon2.attack)
        print("DEFENSE/", Pokemon2.defense)
        print("SP ATTACK/", Pokemon2.spattack)
        print("SP DEFENSE/", Pokemon2.spdefense)
        print("SPEED/", Pokemon2.speed, '\n')
        

        time.sleep(1)

        string_1_attack = 'Its super effective!\n'
        string_2_attack = 'Its not very effective...\n'
        
        # Bucle while mientras tengan vida cada Pokémon
        while (self.health > 0) and (Pokemon2.health > 0):
            # Imprimir la vida de cada Pokémon
            print(self.name ,"health:", self.health)
            print(Pokemon2.name ,"health:", Pokemon2.health)

            print("\nGo", self.name, "!")
            for i, x in enumerate(self.moves):
                print(i+1, movejson[x]['name'])
            index = int(input('Pick a move: '))
            print(self.name ,"used", movejson[self.moves[index-1]]['name'])
            time.sleep(1)

            move_effectiveness = typesjson[str(movejson[self.moves[index-1]]['type'])]['offense'][Pokemon2.types[0]]
            if len(Pokemon2.types) > 1:
                move_effectiveness *= typesjson[str(movejson[self.moves[index-1]]['type'])]['offense'][Pokemon2.types[1]]

            # Determine damage taken
            damage = calculate_damage(self, Pokemon2, movejson[self.moves[index-1]], move_effectiveness)
            Pokemon2.health = math.floor(Pokemon2.health - damage)
            Pokemon2.health = max(Pokemon2.health, 0)

            time.sleep(.2)
            print("Did " + str(math.ceil(damage)) + "HP damage!")

            if  move_effectiveness == 0.5:
                delay_print(string_2_attack)
            elif move_effectiveness >= 2:
                delay_print(string_1_attack)

            time.sleep(1)
            print(self.name ,"health:", self.health)
            print(Pokemon2.name ,"health:", Pokemon2.health)
            time.sleep(.5)

            # Verificar si el Pokémon 'fainted'
            if Pokemon2.health <= 0:
                delay_print("\n..." + Pokemon2.name + ' fainted.')
                break

            # Turno del segundo Pokémon
            print("\nGo",  Pokemon2.name, "!")
            for i, x in enumerate(Pokemon2.moves):
                print(i+1, movejson[x]['name'])
            index = int(input('Pick a move: '))
            print(Pokemon2.name ,"used", movejson[Pokemon2.moves[index-1]]['name'])
            time.sleep(1)

            move_effectiveness = typesjson[str(movejson[Pokemon2.moves[index-1]]['type'])]['offense'][self.types[0]]
            if len(Pokemon2.types) > 1:
                move_effectiveness *= typesjson[str(movejson[Pokemon2.moves[index-1]]['type'])]['offense'][self.types[1]]

            # Determinar daño
            damage = calculate_damage(Pokemon2, self, movejson[Pokemon2.moves[index-1]], move_effectiveness)
            self.health = math.floor(self.health - damage)
            self.health = max(self.health, 0)

            time.sleep(.2)
            print("Did " + str(math.ceil(damage)) + "HP damage!")

            if  move_effectiveness == 0.5:
                delay_print(string_2_attack)
            elif move_effectiveness >= 2:
                delay_print(string_1_attack)


            time.sleep(.5)
            print(self.name ,"health: ", self.health)
            print(Pokemon2.name ,"health:", Pokemon2.health)
            time.sleep(.5)

            # Verificar si el Pokémon 'fainted'
            if self.health <= 0:
                delay_print("\n..." + self.name + ' fainted.')
                break






if __name__ == '__main__':
    with open('moves.json') as json_file:
        movejson = json.load(json_file)

    with open('types.json') as json_file:
        typesjson = json.load(json_file)   

    with open('pokemon.json') as json_file:
        pokemonjson = json.load(json_file) 


    # Creamos cada Pokémon
    Bulbasaur = Pokemon('1', ['12'], ['22', '75', '33', '73'],{'HP':105, 'ATTACK':54, 'DEFENSE':54, 'SPATTACK':70, 'SPDEFENSE':70, 'SPEED':50})
    Ivysaur = Pokemon('2', ['12'], ['22', '75', '331', '73'],{'HP':120, 'ATTACK':67, 'DEFENSE':68, 'SPATTACK':85, 'SPDEFENSE':85, 'SPEED':65})
    Venusaur = Pokemon('3', ['12', '4'], ['22', '75', '89', '338'],{'HP':140, 'ATTACK':87, 'DEFENSE':88, 'SPATTACK':105, 'SPDEFENSE':105, 'SPEED':85})
    Charmander = Pokemon('4', ['10'], ['52', '10', '33', '7'],{'HP':99, 'ATTACK':57, 'DEFENSE':48, 'SPATTACK':65, 'SPDEFENSE':55, 'SPEED':70})
    Charmeleon = Pokemon('5', ['10'], ['52', '10', '53', '7'],{'HP':118, 'ATTACK':69, 'DEFENSE':63, 'SPATTACK':85, 'SPDEFENSE':70, 'SPEED':85})
    Charizard = Pokemon('6', ['10', '3'], ['53', '19', '307', '7'], {'HP':138, 'ATTACK':89, 'DEFENSE':83, 'SPATTACK':114, 'SPDEFENSE':90, 'SPEED':105})
    Squirtle = Pokemon('7', ['11'], ['61', '33', '29', '57'],{'HP':104, 'ATTACK':53, 'DEFENSE':70, 'SPATTACK':55, 'SPDEFENSE':69, 'SPEED':48})
    Wartortle = Pokemon('8', ['11'], ['61', '55', '29', '57'],{'HP':119, 'ATTACK':68, 'DEFENSE':85, 'SPATTACK':70, 'SPDEFENSE':85, 'SPEED':63})
    Blastoise = Pokemon('9', ['11'], ['55', '61', '56', '57'],{'HP':139, 'ATTACK':88, 'DEFENSE':105, 'SPATTACK':90, 'SPDEFENSE':110, 'SPEED':83})


    
        
    


    Charizard.fight(Blastoise) # Empezar batalla