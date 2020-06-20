import time
import numpy as np
import sys
import enum
import json
import math

movejson = typesjson = {}

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


# Delay en cada prit
def delay_print(s):
    # Imprimir personaje uno por uno
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)

# Creation Pokemon
class Pokemon:
    def __init__(self, name, types, moves, EVs):
        # Guardar variables como atributos
        self.name = name
        self.types = types
        self.moves = moves
        self.attack = EVs['ATTACK']
        self.spattack = EVs['SPATTACK']
        self.defense = EVs['DEFENSE']
        self.spdefense = EVs['SPDEFENSE']
        self.speed = EVs['SPEED']
        self.health = EVs['HP']
        self.confusion = False
        self.status = Status.none



    def fight(self, Pokemon2):
        # Permiso para que dos Pokémon combatan

        # Texto de la pelea
        print("-----POKEMONE BATTLE-----")
        print("Pokemon 1:", self.name)
        print("TYPE/", (typesjson[self.types[0]]['name']))
        print("ATTACK/", self.attack)
        print("DEFENSE/", self.defense)
        print("LVL/ 50")
        print("\nVS")
        print("Pokemon 2:", Pokemon2.name)
        print("TYPE/", (typesjson[Pokemon2.types[0]]['name']))
        print("ATTACK/", Pokemon2.attack)
        print("DEFENSE/", Pokemon2.defense)
        print("LVL/ 50")

        time.sleep(2)

        # Ventajas de tipo
        version = ['Fire', 'Water', 'Grass']
        string_1_attack = string_2_attack = ''
        for i,k in enumerate(version):
            if self.types == k:
                # Cuando son del mismo tipo
                if Pokemon2.types == k:
                    string_1_attack = '\nIts not very effective...'
                    string_2_attack = '\nIts not very effective...'

                # Cuando el Pokémon2 es superior
                if Pokemon2.types == version[(i+1)%3]:
                    Pokemon2.attack *= 2
                    Pokemon2.defense *= 2
                    self.attack /= 2
                    self.defense /= 2
                    string_1_attack = '\nIts not very effective...'
                    string_2_attack = '\nIts super effective!'

                # Cuando el Pokémon2 es inferior
                if Pokemon2.types == version[(i+2)%3]:
                    self.attack *= 2
                    self.defense *= 2
                    Pokemon2.attack /= 2
                    Pokemon2.defense /= 2
                    string_1_attack = '\nIts super effective!\n'
                    string_2_attack = '\nIts not very effective...\n'


        
        # Bucle while mientras tengan vida cada Pokémon
        while (self.health > 0) and (Pokemon2.health > 0):
            # Imprimir la vida de cada Pokémon
            print(self.name ,"health:", self.health)
            print(Pokemon2.name ,"health:", Pokemon2.health)

            print("Go", self.name, "!")
            for i, x in enumerate(self.moves):
                print(i+1, movejson[x]['name'])
            index = int(input('Pick a move: '))
            print(self.name ,"used", movejson[self.moves[index-1]]['name'])
            time.sleep(1)
            delay_print(string_1_attack)

            # Determinar cuanto daño hacer
            Pokemon2.health = math.floor(Pokemon2.health - self.attack)
            Pokemon2.health = max(Pokemon2.health, 0)

            time.sleep(1)
            print(self.name ,"health:", self.health)
            print(Pokemon2.name ,"health:", Pokemon2.health)
            time.sleep(.5)

            # Verificar si el Pokémon 'fainted'
            if Pokemon2.health <= 0:
                delay_print("\n..." + Pokemon2.name + ' fainted.')
                break

            # Turno del segundo Pokémon
            print("Go",  Pokemon2.name, "!")
            for i, x in enumerate(Pokemon2.moves):
                print(i+1, movejson[x]['name'])
            index = int(input('Pick a move: '))
            print(Pokemon2.name ,"used", movejson[Pokemon2.moves[index-1]]['name'])
            time.sleep(1)
            delay_print(string_2_attack)

            # Determinar daño
            self.health = math.floor(self.health - Pokemon2.attack)
            self.health = max(self.health, 0)


            time.sleep(1)
            print(self.name ,"health: ", self.health)
            print(Pokemon2.name ,"health:", Pokemon2.health)
            time.sleep(.5)

            # Verificar si el Pokémon 'fainted'
            if self.health <= 0:
                delay_print("\n..." + self.name + ' fainted.')
                break






if __name__ == '__main__':
    # Creamos cada Pokémon
    Bulbasaur = Pokemon('Bulbasaur', ['12'], ['22', '75', '33', '73'],{'HP':105, 'ATTACK':54, 'DEFENSE':54, 'SPATTACK':70, 'SPDEFENSE':70, 'SPEED':50})
    Ivysaur = Pokemon('Ivysaur', ['12'], ['22', '75', '331', '73'],{'HP':120, 'ATTACK':67, 'DEFENSE':68, 'SPATTACK':85, 'SPDEFENSE':85, 'SPEED':65})
    Venusaur = Pokemon('Venusaur', ['12', '4'], ['22', '75', '89', '338'],{'HP':140, 'ATTACK':87, 'DEFENSE':88, 'SPATTACK':105, 'SPDEFENSE':105, 'SPEED':85})
    Charmander = Pokemon('Charmander', ['10'], ['52', '10', '33', '7'],{'HP':99, 'ATTACK':57, 'DEFENSE':48, 'SPATTACK':65, 'SPDEFENSE':55, 'SPEED':70})
    Charmeleon = Pokemon('Charmeleon', ['10'], ['52', '10', '53', '7'],{'HP':118, 'ATTACK':69, 'DEFENSE':63, 'SPATTACK':85, 'SPDEFENSE':70, 'SPEED':85})
    Charizard = Pokemon('Charizard', ['10', '3'], ['53', '19', '307', '7'], {'HP':138, 'ATTACK':89, 'DEFENSE':83, 'SPATTACK':114, 'SPDEFENSE':90, 'SPEED':105})
    Squirtle = Pokemon('Squirtle', ['11'], ['61', '33', '29', '57'],{'HP':104, 'ATTACK':53, 'DEFENSE':70, 'SPATTACK':55, 'SPDEFENSE':69, 'SPEED':48})
    Wartortle = Pokemon('Wartortle', ['11'], ['61', '55', '29', '57'],{'HP':119, 'ATTACK':68, 'DEFENSE':85, 'SPATTACK':70, 'SPDEFENSE':85, 'SPEED':63})
    Blastoise = Pokemon('Blastoise', ['11'], ['55', '61', '56', '57'],{'HP':139, 'ATTACK':88, 'DEFENSE':105, 'SPATTACK':90, 'SPDEFENSE':110, 'SPEED':83})


    with open('moves.json') as json_file:
        movejson = json.load(json_file)

    with open('types.json') as json_file:
        typesjson = json.load(json_file)    
    


    Charizard.fight(Blastoise) # Empezar batalla