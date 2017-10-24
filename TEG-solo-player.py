# -*- coding: utf-8 -*-
"""
Created: Saturday, ‎June ‎17, ‎2017, ‏‎12:51:18 PM
Stephen Redlack

This is an implementation of the Beginner Rogue Player for Solo Tiny Epic Galaxies.
All credit for the game goes to Gamelyn Games and I'm just using this as a useful
means to explore classes in Python.
"""
import random

TEST_MODE = False

DICE = ['MOVE A SHIP',
        'ADVANCE COLONIZATION: DIPLOMACY',
        'ADVANCE COLONIZATION: ECONOMY',
        'ACQUIRE RESOURCES: ENERGY',
        'ACQUIRE RESOURCES: CULTURE',
        'ATTACK']


PLANET_CARDS = {'jak':['Jakks',2,3,1,1],
                'and':['Andellouxian-6',2,6,2,6],
                'lea':['Leandra',1,3,1,3],
                'gle':['Gleam-Zanier',1,6,1,5],
                'hoe':['Hoefker',2,4,2,2],
                'nak':['Nakagawakozi',1,5,1,3],
                'jac':['Jac-110912',2,6,2,5],
                'clj':['Clj-0517',1,4,2,2],
                'bru':['Brumbaugh',1,5,1,3],
                'pie':['Piedes',1,7,2,7],
                'omi':['Omicron-fenzi',2,5,1,3],
                'gor':['Gort',1,7,2,7],
                'mj-':['Mj-120210',1,4,1,2],
                'mai':['Maia',2,6,1,5],
                'umb':['Umbra-Forum',2,5,2,3],
                'zav':['Zavodnick',1,6,2,5],
                'zal':['Zalax',2,4,1,2],
                'bir':['Birkomius',2,3,1,1],
                'k-w':['K-Widow',2,7,2,7],
                'dre':['Drewkaiden',2,3,2,1],
                'hel':['Helios',2,4,1,2],
                'vic':['Vici-Ks156',1,3,2,1],
                'pad':['Padraigin-3110',2,5,2,3],
                'lur':['Lureena',2,4,2,2],
                'gyo':['Gyore',2,7,2,7],
                'aug':['Aughmoore',1,7,1,7],
                'tif':['Tifnod',2,3,2,1],
                'nag':['Nagato',1,5,2,3],
                'ter':['Terra-Bettia',1,7,1,7],
                'jor':['Jorg',2,5,1,3],
                'wal':['Walsfeo',1,6,2,5],
                'nib':['Nibiru',2,7,1,7],
                'viz':['Vizcarra',1,3,1,1],
                'sar':['Sargus-36',2,6,1,5],
                'pem':['Pembertonia-Major',1,5,2,3],
                'la-':['La-Torres',2,4,1,2],
                'bis':['Bisschop',1,3,2,1],
                'sho':['Shouhua',1,7,1,7],
                'bsw':['Bsw-10-1',1,6,1,5],
                'mar':['Mared',1,4,2,2],}

class Planet(object):
    def __init__(self):
        """ Initialize the Planet class.
        A Planet represents a planet card drawn from the deck.
        If the TEST_MODE flag is on, then assign random values for the planet attributes.
        Otherwise, initialize the planet card based on the first few characters in the name.
        """
        if TEST_MODE == False:
            card = input('First 3 letters of planet name: ')
            self.name=PLANET_CARDS[card][0]
            self.resource = PLANET_CARDS[card][1]
            self.size = PLANET_CARDS[card][2]
            self.advancer = PLANET_CARDS[card][3]
            self.points = PLANET_CARDS[card][4]          
        else:
            self.name = random.randint(1000,2000)
            self.resource = random.randint(1,2)
            self.size = random.randint(1,7)
            self.advancer = random.randint(1,2)
            self.points = random.randint(1,5)
            
    def display(self):
        """ Display the planet card attributes """
        if self.resource == 1:
            resource = 'ENERGY'
        else:
            resource = 'CULTURE'
        if self.advancer == 1:
            advancer = 'DIPLOMACY'
        else:
            advancer = 'ECONOMY'
        print(self.name, resource, self.size, advancer, self.points)

class Planets(object):
    def __init__(self):
        """ Initialize the set of planets on the board tableau."""
        self.planet_list = []
        for p in range(4):
            print('Setup planet',p,'...')
            self.planet_list.append(Planet())
    
    def display(self):
        """ Display all planets on the board. """
        print('Planets...')
        print('--------------------')
        for planet in self.planet_list:
            planet.display()
        print('--------------------')
        
    def replace(self, planet_id):
        """ Replace a planet with a new one.
        This typically happens after it has been colonized by a player.
        
        planet_id --- The index of the planet on the board.
        """
        print('Replacing planet',planet_id,'...')
        self.planet_list[planet_id] = Planet()
        

class Rogue(object):
    def __init__(self, planets):
        self.energy = 0
        self.culture = 0
        self.level = 1
        self.points = 0
        self.ship_positions = [0,0,0,0]
        self.dice_per_level = [5,5,6,6,7]
        self.planets = planets
        
    def display(self):
        """ Display the Rouge player stats. """
        print('----------------------')
        print('Rogue level =',self.level, '/ 6')
        print('Rogue points =',self.points, '/ 21')
        print('Rogue energy =',self.energy, '/ 6')
        print('Rogue culture =',self.culture, '/ 6')
        for i in range(4):
            print('Rogue ship',i,'=',self.ship_positions[i], '/', self.planets.planet_list[i].size)
        print('----------------------')
    
    def move_a_ship(self):
        """ Move a ship from home to orbit the next available planet. """
        for i in range(4):
            if self.ship_positions[i] == 0:
                self.ship_positions[i] = 1
                break
        return
    
    def move_home(self, ship):
        """ Move a ship from a planet back home.
        Typically done if the player has colonized the planet before the rogue.
        
        ship --- planet index of the ship coming home
        """
        self.ship_positions[ship] = 0
    
    def follow_cap_check(self):
        if input('Did you capture a planet by following the Rogue? (N/y)') == 'y':
            planet_id = -1
            while planet_id < 0:
                try:
                    planet_id = input('Which planet (0-3)? ')
                    if planet_id > 3: planet_id = -1
                except Exception:
                    planet_id = -1
            self.move_home(planet_id)
            self.planets.replace(planet_id)
                
    def advance_colonization_diplomacy(self):
        self.follow_cap_check()
        for i in range(4):
            # Advance the ship
            if self.ship_positions[i] > 0:
                if self.planets.planet_list[i].advancer == 1:
                    self.ship_positions[i] += 1
            # Capture the planet if applicable
            if self.ship_positions[i] == planets.planet_list[i].size:
                print('Planet',i,'captured...')
                self.ship_positions[i] = 0
                self.points += self.planets.planet_list[i].points
                self.planets.replace(i)
        return    
    
    def advance_colonization_economy(self):
        self.follow_cap_check()
        for i in range(4):
            # Advance the ship
            if self.ship_positions[i] > 0:
                if self.planets.planet_list[i].advancer == 2:
                    self.ship_positions[i] += 1
            # Capture the planet if applicable
            if self.ship_positions[i] == self.planets.planet_list[i].size:
                print('Planet',i,'captured...')
                self.ship_positions[i] = 0
                self.points += self.planets.planet_list[i].points
                self.planets.replace(i)
        return 
    
    def acquire_resources_energy(self):
        for i in range(4):
            if self.ship_positions[i] > 0:
                if self.planets.planet_list[i].resource == 1:
                    self.energy += 1
            if self.ship_positions[i] == 0:
                self.energy += 1
        return    
    
    def acquire_resources_culture(self):
        for i in range(4):
            if self.ship_positions[i] > 0:
                if self.planets.planet_list[i].resource == 2:
                    self.culture += 1
            if self.ship_positions[i] == 0:
                self.culture += 1
        return
    
    def attack(self):
        if self.level == 1: input('Lose 1 energy. Press enter to continue')
        if self.level == 2: input('Lose 1 culture. Press enter to continue')
        if self.level == 3:
            steal = 'y'
            steal = input('Does Rogue steal 1 culture (Y/n)')
            if steal == 'y': self.culture += 1
        if self.level == 4: input('Regress a ship by -1. Press enter to continue')
        if self.level == 5:
            print('Rogue steals 2 resources of your choice')
            try:
                energy = int(input('How many energy? '))
            except ValueError:
                energy = 0
            try:
                culture = int(input('How many culture? '))
            except ValueError:
                culture = 0
            self.energy += energy
            self.culture += culture
        return
    
    def roll_dice_bundle(self, count):
        for i in range(count):
            reroll = True
            the_roll = ''
            while reroll:
                the_roll = DICE[random.randint(0, len(DICE)-1)]
                print(i, ':', the_roll)
                reroll = False
                to_reroll = input('Spend 1E & 1C to reroll (y/N)? ')
                if to_reroll == 'y':
                    reroll = True
            if the_roll == 'MOVE A SHIP':
                self.move_a_ship()
            if the_roll == 'ADVANCE COLONIZATION: DIPLOMACY':
                self.advance_colonization_diplomacy()
            if the_roll == 'ADVANCE COLONIZATION: ECONOMY':
                self.advance_colonization_economy()
            if the_roll == 'ACQUIRE RESOURCES: ENERGY':
                self.acquire_resources_energy()
            if the_roll == 'ACQUIRE RESOURCES: CULTURE':
                self.acquire_resources_culture()
            if the_roll ==  'ATTACK':
                self.attack()
            self.display()
    
    def roll_dice(self):
        self.roll_dice_bundle(self.dice_per_level[self.level-1])
        
        # Check energy
        if self.energy >= 6:
            self.energy = 0
            print('Level up...')
            self.level += 1
            if self.level == 2: self.points += 1
            if self.level == 3: self.points += 1
            if self.level == 4: self.points += 2
            if self.level == 5: self.points += 3
            if self.level == 6:
                print('Rogue level 6! Game Over...')
                return
        
        # Check culture
        if self.culture >= 6:
            self.culture = 0
            input('Rolling culture bonus actions. Press enter to contine')
            self.roll_dice_bundle(3)



if __name__ == "__main__":
    
    planets = Planets()
    planets.display()
    input('Planets setup, hit enter when ready...')
      
    rogue = Rogue(planets)
    turn_count = 0

    while True:
        turn_count += 1
        print('Turn', turn_count)
        rogue.display()
        rogue.roll_dice()
        if rogue.level == 6: break
        if rogue.points >= 21:
            print('Rogue achieved 21 points! Game Over...')
            break
        print('Rogue turn done...')
        input('Your turn. Hit enter to continue..')
        capture = 'n'
        capture = input('Did you capture a planet this round (y/N)? ')
        if capture == 'y':
            captured_planet = int(input('Which one (0-3)? '))
            rogue.move_home(captured_planet)
            planets.replace(captured_planet)
        planets.display()
        to_continue = input('turn done. Another round (Y/n)? ')
        if to_continue == 'n':
            break
    print()
    print('All done. Exiting...')