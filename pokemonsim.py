import time
import numpy as np
import sys
import enum
import json
import math
import random

movejson = typesjson = pokemonjson = {}
string_1_attack = 'Its super effective!\n'
string_2_attack = 'Its not very effective...\n'

#Stat modification multiplier
stat_stage_multiplier = {-6: 0.25, -5: 0.285, -4: 0.33, -3: 0.4, -2: 0.5, -1: 0.66, 0: 1, 1: 1.5, 2: 2, 3: 2.5, 4: 3, 5: 3.5, 6: 4}
accuracy_stage_multiplier = {-6: 0.33, -5: 0.375, -4: 0.428, -3: 0.5, -2: 0.6, -1: 0.75, 0: 1, 1: 1.33, 2: 1.66, 3: 2, 4: 2.33, 5: 2.66, 6: 3}

#effects number of moves
recoil_moves_list = [49, 199, 254, 255, 263, 270]
weight_moves_list = [197,292]
heal_moves_list = [4, 348, 353]
confusion_moves_list = [77, 268, 338]
flinch_moves_list = [32, 147, 151]
poison_moves_list = [3, 78, 203, 210]
burn_moves_list = [5, 126, 201, 254, 274]
freeze_moves_list = [6, 261, 275]
paralysis_moves_list = [7, 153, 263, 276]
stat_moves_attacker_list = [139, 140, 141, 183, 205, 219, 230, 277, 296, 335]
stat_moves_defender_list = [21, 69, 70, 71, 72, 73, 272, 297, 331]
#sleep list too


class Status(enum.Enum):
    none = 0
    sleep = 1
    poison = 2
    paralysis = 3
    burn = 4
    freeze = 5


def calculate_damage(Pokemon1, Pokemon2, move_info, move_effectiveness):
    critical = weather = burnstatus = other = stab = 1
    crit_chance = 0.0625
    power = move_info['power']
    attack = Pokemon1.attack * stat_stage_multiplier[Pokemon1.attackstage]
    defense = Pokemon2.defense * stat_stage_multiplier[Pokemon2.defensestage]
    if move_info['damage_class'] == 'special':
        attack = Pokemon1.spattack * stat_stage_multiplier[Pokemon1.spattackstage]
        defense = Pokemon2.spdefense * stat_stage_multiplier[Pokemon2.spdefensestage]

    if Pokemon1.status == Status.burn and move_info['damage_class'] == 'physical':
        burnstatus = 0.5

    if move_info['effect'] == 289: #100% critical hit moves
        crit_chance = 1
    elif move_info['effect'] == 44 or move_info['effect'] == 201 or move_info['effect'] == 210: #increased crit rate
        crit_chance = 0.125
    
    if random.random() <= crit_chance:
        print("A critical hit!")
        critical = 2
   
    if move_info['type'] in pokemonjson[Pokemon1.id]['types']:
        stab = 1.5

    if move_info['effect'] in weight_moves_list:
        power = Pokemon1.calculate_weight_power(Pokemon2, move_info['effect'])
    elif move_info['effect'] == 255: #struggle
        move_effectiveness = 1
    elif move_info['effect'] == 318: #acrobatics
        power *= 2

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
    def __init__(self, nameid, types, moves, EVs): #EVs is placeholder for lvl50 stats for now
        # Guardar variables como atributos
        self.id = nameid
        self.name = pokemonjson[nameid]['name']
        self.types = pokemonjson[nameid]['types']
        self.moves = moves
        #set base stats
        self.attack = self.curattack = EVs['ATTACK']
        self.spattack = self.curspattack = EVs['SPATTACK']
        self.defense = self.curdefense = EVs['DEFENSE']
        self.spdefense = self.curspdefense = EVs['SPDEFENSE']
        self.speed = self.curspeed = EVs['SPEED']
        self.health = self.curhealth = EVs['HP']
        self.confusion = self.flinch = False
        self.status = Status.none
        self.sleep_counter = self.confusion_counter = 0
        self.attackstage = self.defensestage = self.spattackstage = self.spdefensestage = self.speedstage = self.accuracystage = 0

        #might change up something to avoid this
        self.types[0] = str(self.types[0])
        if len(self.types) > 1:
            self.types[1] = str(self.types[1])

    def check_faint(self): #checks if fainted and prints out faint statement if true
        if self.curhealth <= 0:
            delay_print("\n..." + self.name + ' fainted.')
            return True

        return False

    #Applies stat changes depending on effect id on Pokemon
    def change_stat_stage(self, move_effect):
        stat_string = ""
        if move_effect in [69, 183]:
            self.attackstage = max(-6, self.attackstage - 1)
            stat_string += self.name + "'s attack fell!\n"
        if move_effect in [70, 183, 230, 335]:
            self.defensestage = max(-6, self.defensestage - 1)
            stat_string += self.name + "'s defense fell!\n"
        if move_effect in [72]:
            self.spattackstage = max(-6, self.spattackstage - 1)
            stat_string += self.name + "'s special attack fell!\n"
        if move_effect in [73, 230, 335]:
            self.spdefensestage = max(-6, self.spdefensestage - 1)
            stat_string += self.name + "'s special defense fell!\n"
        if move_effect in [21, 71, 331, 335]:
            self.speedstage = max(-6, self.speedstage - 1)
            stat_string += self.name + "'s speed fell!\n"
        if move_effect in [140, 141]:
            self.attackstage = min(6, self.attackstage + 1)
            stat_string += self.name + "'s attack rose!\n"
        if move_effect in [139, 141]:
            self.defensestage = min(6, self.defensestage + 1)
            stat_string += self.name + "'s defense rose!\n"
        if move_effect in [277, 141]:
            self.spattackstage = min(6, self.spattackstage + 1)
            stat_string += self.name + "'s special attack rose!\n"
        if move_effect in [141]:
            self.spdefensestage = min(6, self.spdefensestage + 1)
            stat_string += self.name + "'s special defense rose!\n"
        if move_effect in [219, 296, 141]:
            self.speedstage = min(6, self.speedstage + 1)
            stat_string += self.name + "'s speed rose!\n"
        if move_effect in [205]:
            self.spattackstage = max(-6, self.spattackstage - 2)
            stat_string += self.name + "'s special attack harshly fell!\n"
        if move_effect in [272, 297]:
            self.spdefensestage = max(-6, self.spdefensestage - 2)
            stat_string += self.name + "'s special attack defense fell!\n"

        print(stat_string)

    #Checks if specific status condition affects Pokemon. Returns True if status can be applied
    def check_status_affect(self, status_condition):
        if not(self.status == Status.none):
            return False
        if status_condition == Status.burn and '11' in self.types:
            return False
        if status_condition == Status.freeze and '15' in self.types:
            return False
        if status_condition == Status.paralysis and '5' in self.types:
            return False
        if status_condition == Status.poison and (('4' in self.types) or ('9' in self.types)):
            return False
        return True

    def get_status_string(self):
        if self.status == Status.paralysis:
            return "[PAR]"
        elif self.status == Status.freeze:
            return "[FRZ]"
        elif self.status == Status.burn:
            return "[BRN]"
        elif self.status == Status.poison:
            return "[PSN]"
        elif self.status == Status.sleep:
            return "[SLP]"
        return ""

    def calculate_recoil_damage(self, damage, move_effect):
        hurt = 0
        if move_effect == 49 or move_effect == 255:
            hurt = math.floor(damage / 4)
        elif move_effect == 199 or move_effect == 254 or move_effect == 263:
            hurt = math.floor(damage / 3)
        elif move_effect == 270:
            hurt = math.floor(damage / 2)

        self.health -= hurt
        print(self.name + " was hurt " + str(hurt) + "HP (" + str(100*hurt/self.health) + "%)by recoil!")

    def calculate_weight_power(self, Pokemon2, move_effect):
        pokemon1_weight = pokemonjson[self.id]['weight']
        pokemon2_weight = pokemonjson[Pokemon2.id]['weight']
        if move_effect == 197: #only depends defender weight
            if pokemon2_weight < 10:
                return 20
            elif pokemon2_weight < 25:
                return 40
            elif pokemon2_weight < 50:
                return 60
            elif pokemon2_weight < 100:
                return 80
            elif pokemon2_weight < 200:
                return 100
            else:
                return 200
        else:
            relative = pokemon2_weight / pokemon1_weight #move_effect == 292 relative weight
            if relative <= 0.20:
                return 120
            elif relative <= 0.25:
                return 100
            elif relative <= 33.34:
                return 80
            elif relative <= 0.5:
                return 60
            else:
                return 40

    def calculate_heal(self, damage, move_effect):
        healhp = math.floor(damage * 0.5)
        if move_effect == 353:
            healhp = math.floor(damage * 0.75)
        
        healhp = min(self.health - self.curhealth, healhp) #can't go above max health
        if healhp == 0:
            return
        else:
            self.curhealth += healhp
            print(self.name + " healed " + str(healhp) + "HP (" + str(math.floor(100*healhp/self.health)) + "%)")

    def calculate_recoil_on_miss(self):
        recoil = min(math.floor(self.health/2), self.curhealth)
        self.health -= recoil
        print(self.name + " kept on going and crashed for " + str(recoil) + " HP (" + str(100*recoil/self.health) + ") recoil damage!")

    def apply_status_damage(self):
        if self.status == Status.poison:
            print(self.name + " took damage from poison.")
            self.curhealth -= math.floor(self.health / 8)
        elif self.status == Status.burn:
            print(self.name + " took damage from burn.")
            self.curhealth -= math.floor(self.health / 16)

    def apply_status_ailment(self, move_effect):
        if move_effect in burn_moves_list:
            self.apply_burn()
        elif move_effect in poison_moves_list:
            self.apply_poison()
        elif move_effect in freeze_moves_list:
            self.apply_freeze()
        elif move_effect in paralysis_moves_list:
            self.apply_paralysis()

    def unapply_status_ailment(self):
        self.status = Status.none
        print(self.name + "'s status is restored")
    
    #applies paralysis and speed change; might need to apply speed change when pokemon exits and re-enters...
    def apply_paralysis(self):
        #can't be paralyzed if already affected by status condition or if ground type
        if self.check_status_affect(Status.paralysis):
            self.status = Status.paralysis
            self.curspeed = self.curspeed * 0.5
            print(self.name + " is paralyzed! It may not be able to move!")
    
    #unapplies paralysis/speed change
    def unapply_paralysis(self):
        self.status = Status.none
        self.curspeed = self.curspeed * 2

    def apply_sleep(self):
        if self.check_status_affect():
            self.status = Status.sleep
            self.sleep_counter = random.randint(1,3)
            print(self.name + " has fallen asleep...")

    def apply_poison(self):
        if self.check_status_affect(Status.poison):
            self.status = Status.poison
            print(self.name + " is poisoned!")

    def apply_freeze(self):
        if self.check_status_affect(Status.freeze):
            self.status = Status.freeze
            print(self.name + " is frozen!")
    
    def apply_burn(self):
        if self.check_status_affect(Status.burn):
            self.status = Status.burn
            print(self.name + " is burned!")

    def apply_confusion(self):
        if not(self.confusion):
            self.confusion = True
            self.confusion_counter = random.randint(2,5)
            print(self.name + " is confused!")

    #Status conditions / confusion may prevent pokemon from attacking
    def check_attack_status(self, move):
        if self.flinch:
            self.flinch = False
            print(self.name + " flinched!")
            return False
        if self.status == Status.sleep:
            if self.sleep_counter == 0:
                self.status = Status.none
                print(self.name + " has woke up!")
                return True
            print(self.name + " is still asleep")
            self.sleep_counter -= 1
            #Snore/Sleep Talk
            if move['id'] == 173 or move['id'] == 214:
                return True
            return False

        elif self.status == Status.paralysis:
            if random.random() < 0.25:
                print(self.name + " is paralyzed! It cannot move!")
                return False

        elif self.status == Status.freeze:
            if random.random() <= 0.20 or move['type'] == 10:
                print(self.name + " has defrosted!")
                return True
            print(self.name + " is frozen solid!")
            return False

        if self.confusion:
            if self.confusion_counter == 0:
                self.confusion = False
                print(self.name + " has snapped out of confusion!")
                return True
            print(self.name + " is confused!")
            self.confusion_counter -= 1
            #may hurt itself in confusion
            if random.random() <= 0.50:
                return True
            damage = math.floor((((22*40*self.curattack/self.curdefense) / 50) + 2) * (random.randint(85,100)*0.01))
            self.curhealth -= damage
            print(self.name + " has hurt itself in confusion! (" + str(damage) + "HP)")
            return False

        return True
    
    def attack_move(self, Pokemon2, index):
        #####self.attack(Pokemon2)
            move_used = movejson[self.moves[index-1]]
            print(self.name ,"used", move_used['name'])
            time.sleep(1)
            #move effect 18 are attacks that don't miss
            if (random.randint(1,100) > move_used['accuracy']) and (move_used['damage_class'] != 'non-damaging') and not(move_used['effect'] == 18) and not(move_used['effect'] == 79):
                print('The attack missed!')
                if move_used['effect'] == 46:
                    self.calculate_recoil_on_miss()

            elif (move_used['damage_class'] != 'non-damaging'):
                move_effectiveness = typesjson[str(move_used['type'])]['offense'][Pokemon2.types[0]]
                if len(Pokemon2.types) > 1: #compound effectiveness if target has 2 types
                    move_effectiveness *= typesjson[str(move_used['type'])]['offense'][Pokemon2.types[1]]

                #Multi-hit attacks
                num_hits = 1
                if move_used['effect'] in [45, 78]:
                    num_hits = 2
                elif move_used['effect'] == 30:
                    num_hits = [2,2,3,3,4,5][math.floor(random.randint(0,5))]
                # Determine damage taken
                damage = 0
                damage = calculate_damage(self, Pokemon2, move_used, move_effectiveness)
                Pokemon2.curhealth = math.floor(Pokemon2.curhealth - damage)
                Pokemon2.curhealth = max(Pokemon2.curhealth, 0)

                time.sleep(.2)
                if (damage < 1):
                    print("Move had no effect...")
                    return
                else:
                    print("Did " + str(math.ceil(damage)) + "HP damage!")
                    if  move_effectiveness > 0 and move_effectiveness < 1:
                        delay_print(string_2_attack)
                    elif move_effectiveness > 1:
                        delay_print(string_1_attack)
                    if num_hits > 1:
                        print("Hit " + str(num_hits) + " times!\n")

                #recoil damage moves
                if int(move_used['effect']) in recoil_moves_list:
                    self.calculate_recoil_damage(damage, move_used['effect'])
                elif int(move_used['effect']) in heal_moves_list:
                    self.calculate_heal(damage, move_used['effect'])
                #Confusion
                if move_used['effect'] in confusion_moves_list:
                    if random.random()*100 < move_used['effect_chance']:
                        Pokemon2.apply_confusion()
                #flinch
                if move_used['effect'] in flinch_moves_list:
                    if random.random()*100 < move_used['effect_chance']:
                        Pokemon2.flinch = True
                #status effect moves (burn/poison/paralysis/freeze)
                if move_used['effect'] in (burn_moves_list + freeze_moves_list + poison_moves_list + paralysis_moves_list):
                    if random.random()*100 < move_used['effect_chance']:
                        Pokemon2.apply_status_ailment(move_used['effect'])
                #stat change moves (increase/decrease you/opponent)
                if move_used['effect'] in stat_moves_attacker_list:
                    if random.random()*100 < move_used['effect_chance']:
                        self.change_stat_stage(move_used['effect'])
                if move_used['effect'] in stat_moves_defender_list:
                    if random.random()*100 < move_used['effect_chance']:
                        Pokemon2.change_stat_stage(move_used['effect'])
                #fire type damaging moves defrost
                if move_used['type'] == 10 and Pokemon2.status == Status.freeze:
                    Pokemon2.status = Status.none
                    print(Pokemon2.name + " is defrosted!")

            ###time.sleep(.5) print(self.name ,"health:", self.health) print(Pokemon2.name ,"health:", Pokemon2.health) time.sleep(.5)


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
        
        # Bucle while mientras tengan vida cada Pokémon
        turn_number = 0
        while (self.curhealth > 0) and (Pokemon2.curhealth > 0):
            #increment turn number; no Pokemon are flinched in the beginning
            turn_number += 1
            self.flinch = Pokemon2.flinch = False

            # Print turn and pokemon info
            print("_____TURN #" + str(turn_number) + "_____")
            print(self.name ,"health:", self.curhealth, self.get_status_string())
            print(Pokemon2.name ,"health:", Pokemon2.curhealth, Pokemon2.get_status_string())

            print("\nMoves for " + self.name )
            for i, x in enumerate(self.moves):
                print(i+1, movejson[x]['name'])
            index = int(input('Pick a move: '))

            print("\nMoves for " + Pokemon2.name)
            for i, x in enumerate(Pokemon2.moves):
                print(i+1, movejson[x]['name'])
            index2 = int(input('Pick a move: '))
            
            #if outspeed opponent (for equal priority) or your move has higher priority, you go first. Otherwise opponent goes first
            if ((movejson[self.moves[index-1]]['priority'] == movejson[Pokemon2.moves[index2-1]]['priority']) and (self.curspeed >= Pokemon2.curspeed)) \
                or (movejson[self.moves[index-1]]['priority'] > movejson[Pokemon2.moves[index2-1]]['priority']):
                if self.check_attack_status(movejson[self.moves[index-1]]):
                    self.attack_move(Pokemon2, index)
                if self.check_faint():
                    break
                if Pokemon2.check_faint(): 
                    break
                if Pokemon2.check_attack_status(movejson[Pokemon2.moves[index2-1]]):
                    Pokemon2.attack_move(self, index2)
            else:
                if Pokemon2.check_attack_status(movejson[Pokemon2.moves[index2-1]]):
                    Pokemon2.attack_move(self, index2)
                if self.check_faint():
                    break
                if Pokemon2.check_faint(): 
                    break
                if self.check_attack_status(movejson[self.moves[index-1]]):
                    self.attack_move(Pokemon2, index)
                
            if self.check_faint():
                break
            if Pokemon2.check_faint(): 
                break

            
            ### status damage
            self.apply_status_damage()
            Pokemon2.apply_status_damage()
            if self.check_faint():
                break

            if Pokemon2.check_faint():
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
    Venusaur = Pokemon('3', ['12', '4'], ['98', '202', '305', '206'],{'HP':1140, 'ATTACK':87, 'DEFENSE':88, 'SPATTACK':105, 'SPDEFENSE':105, 'SPEED':85})
    Charmander = Pokemon('4', ['10'], ['52', '10', '33', '7'],{'HP':99, 'ATTACK':57, 'DEFENSE':48, 'SPATTACK':65, 'SPDEFENSE':55, 'SPEED':70})
    Charmeleon = Pokemon('5', ['10'], ['52', '10', '53', '7'],{'HP':118, 'ATTACK':69, 'DEFENSE':63, 'SPATTACK':85, 'SPDEFENSE':70, 'SPEED':85})
    Charizard = Pokemon('6', ['10', '3'], ['53', '19', '307', '7'], {'HP':138, 'ATTACK':89, 'DEFENSE':83, 'SPATTACK':114, 'SPDEFENSE':90, 'SPEED':105})
    Squirtle = Pokemon('7', ['11'], ['61', '33', '29', '57'],{'HP':104, 'ATTACK':53, 'DEFENSE':70, 'SPATTACK':55, 'SPDEFENSE':69, 'SPEED':48})
    Wartortle = Pokemon('8', ['11'], ['61', '55', '29', '57'],{'HP':119, 'ATTACK':68, 'DEFENSE':85, 'SPATTACK':70, 'SPDEFENSE':85, 'SPEED':63})
    Blastoise = Pokemon('9', ['11'], ['221', '87', '305', '206'],{'HP':1139, 'ATTACK':88, 'DEFENSE':105, 'SPATTACK':90, 'SPDEFENSE':110, 'SPEED':83})


    
        
    


    Venusaur.fight(Blastoise) # Empezar batalla