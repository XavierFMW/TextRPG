from random import randint
import math
import sys



# System Class

class system:

    def check_items(self, player, *args):
        """<NPC (optional)> - Displays all the items belonging to either you or an NPC."""

        if args:
            
            if args[0] in [x.name for x in player.stage.chars]:

                NPC = [x for x in player.stage.chars if x.name == args[0]][0]

                if not NPC.items:

                    print("This NPC has no items to view!\n")
                    player.run_command()

                else:
                    items = NPC.items

            else:
                print(f"Invalid NPC\n")
                player.run_command()

        else:
            items = player.items
        
        print("\nItem name, sell value, notes - Description")

        for item in items:

            if isinstance(item, weapon) or isinstance(item, magic_weapon):
                print(f"{item.name}, {item.value}g, {item.damage} damage - {item.desc}")

            elif isinstance(item, armor):
                print(f"{item.name}, {item.value}g, {item.defense} defense - {item.desc}")

            elif isinstance(item, consumable):
                print(f"{item.name}, {item.value}g, {item.health} hp, {item.mana} mp - {item.desc}")

            else:
                print(f"{item.name}, {item.value}g - {item.desc}")

        print("\n")
        player.run_command()


    def profile(self, player, *args):
        """- Displays your stats."""

        print(f"""
{player.name}, level {player.level}

Health: {player.current_hp}/{player.max_hp}
Mana: {player.current_mp}/{player.max_mp}
            
Armor: {player.armor.name}, {player.armor.defense} defense
Weapon: {player.weapon.name}, {player.weapon.damage} damage
Money: {player.gold}g

Strength: {player.str}
Fortitude: {player.fort}
Wisdom: {player.wis + player.armor.magic}
            """)

        # This indentation ISN'T breaking the program, which breaks my head. Because the quotes used to form the multi-line string are still
        # at the correct indentation level, nothing is broken, but it looks so ugly and wrong. If you indent these lines, however, the printed
        # string is indented an equal amount, which messes up the formatting, so Python has forced me to leave this mess.

        player.run_command()


    def use_item(self, player, item_name):
        """<item> - Use a specific item. Case sensitive."""

        if item_name in [x.name for x in player.items]:

            try:
                item = [x for x in player.items if x.name == item_name][0]
                item.use(player)
            
            except:
                print("Item cannot be used\n")

            player.run_command()

        else:
            print("Invalid item\n")
            player.run_command()


    def attack(self, player, *args):
        """<enemy or NPC> - Attack an enemy or NPC."""

        if args[0] in [x.name for x in player.stage.chars]:

            npc = [x for x in player.stage.chars if x.name == args[0]][0]
            special_npcs = ["bishop", "recruiter", "hiddenFigure", "Clement", "soldier", "guard", "Lucifer", "barkeep", "potionSeller", "oldMan", "theKing"]

            if isinstance(player.weapon, magic_weapon) and player.current_mp < player.weapon.cost:

                print("You don't have enough mana to use your current weapon!\n")
                player.run_command()

            elif npc.name in special_npcs:
                npc.fight(player)

            else:

                player.stage.chars = []
                print(f"You have killed {npc.name}, and everyone else has fled.\n")

                if player.royal > 0:
                    player.royal = -1

                else:
                    player.royal -= 1

                player.kills += 1
                player.run_command()

        
        elif player.encounter:

            if len(args) == 0 or args[0] not in [x.name for x in player.enemies]:

                print("Invalid enemy\n")
                player.run_command()

            elif isinstance(player.weapon, magic_weapon) and player.current_mp < player.weapon.cost:

                    print("You don't have enough mana to use your current weapon!\n")
                    player.run_command()

            else:

                weapon = player.weapon
                damage = randint(weapon.damage - weapon.variant, weapon.damage + weapon.variant)
                base_dam = damage

                if isinstance(weapon, magic_weapon):
                    player.change_mp(-weapon.cost)
                    damage += player.wis + player.armor.magic

                else:
                    damage += player.str

                target = [x for x in player.enemies if x.name == args[0]][0]

                old_hp = target.current_hp
                target.change_hp(-damage)
                new_hp = target.current_hp

                dam_dealt = abs(new_hp - old_hp)
                
                if base_dam == weapon.damage + weapon.variant:
                    print(f"Critical hit! You attack {target.name} with your {weapon.name}, dealing {dam_dealt} damage!")

                elif dam_dealt == 0:
                    print(f"Miss! You attack {target.name} with your {weapon.name}, dealing {dam_dealt} damage!")

                else:
                    print(f"You attack {target.name} with your {weapon.name}, dealing {dam_dealt} damage!")

                if target.current_hp <= 0:

                    print(f"You kill {target.name}!\n")
                    player.enemies.remove(target)

        else:
            print("Invalid input!\n")
            player.run_command()


    def view_enemies(self, player, *args):
        "- View all of the current enemies during a fight."

        if player.encounter:

            print("\n")

            for enemy in player.enemies:
                print(f"{enemy.name} ({enemy.current_hp}/{enemy.max_hp}), level {enemy.level}, {enemy.damage} damage, {enemy.defense} defense")

            print("\n")
            player.run_command()

        else:
            print("There are no enemies to view!\n")
            player.run_command()


    def view_npcs(self, player, *args):
        "- View all of the NPCs in your current area."

        if player.stage.chars:

            print("\n")

            for NPC in player.stage.chars:
                print(f"{NPC.name}, level {NPC.level}, {NPC.gold}g")

            print("\n")
            player.run_command()

        else:
            print("There are no NPCs in your area!\n")
            player.run_command()


    def move_stages(self, player, dir, *args):
        """<direction> - Move in a certain direction."""

        if player.encounter:
            print("You cannot walk away during a fight!\n")
            player.run_command()

        else:
            dir = dir.lower()[0]
            move_dict = {"n": player.stage.north, "w": player.stage.west, "s": player.stage.south, "e": player.stage.east}

            if dir not in move_dict:

                print("Invalid direction\n")
                player.run_command()

            elif move_dict[dir] == None:

                print("There's nothing in that direction\n")
                player.run_command()
                
            elif move_dict[dir] == "Blocked":

                print("That direction is blocked\n")
                player.run_command()
                

            else:
                player.change_mp(1)

                for item in [x for x in player.items if x.name == "bread"]:
                    item.age += 1

                    if item.age >= 750:
                        player.items.remove(item)
                        player.items.append(weapon("staleBread", "A piece of bread so old that it can be used as a weapon.", 0, 15, 2))

                names = [x.name for x in player.items]

                player.stage.visited = True
                player.stage = move_dict[dir]
                player.stage.active_stage(player)


    def speak(self, player, name, *args):
        """<NPC> - Speak to specific NPC."""

        if name in [x.name for x in player.stage.chars]:
            NPC = [x for x in player.stage.chars if x.name == name][0]

            if NPC.visited:
                NPC.greeting(player)

            else:
                NPC.introduction(player)

        else:
            print("There is no NPC by that name in your area!\n")
            player.run_command()


    def __init__(self):
        self.commands = {"items": self.check_items, "profile": self.profile, "use": self.use_item, "attack": self.attack, "enemies": self.view_enemies, "walk": self.move_stages, "who": self.view_npcs, "talk": self.speak}


    def game_help(self, player, *args):
        """
        - Displays each of the game's commands and their function.
        """

        print("\n")

        for cmd in self.commands:
            print(f"{cmd} {self.commands[cmd].__doc__}")

        print("\n")
        player.run_command()



# Character Class

class character:
    
    def __init__(self, name, money, lvl, xp, items, health=20, mana=20):

        self.name = name

        self.level = lvl
        self.xp = xp
        
        self.max_hp = health
        self.current_hp = health

        self.max_mp = mana
        self.current_mp = mana

        self.items = items
        self.gold = money
    

    def change_mp(self, num):

        if num > 0:

            for i in range(num):

                if self.current_mp < self.max_mp:
                    self.current_mp += 1

                else:
                    break

        elif num < 0:

            for i in range(-num):

                if self.current_mp > 0:
                    self.current_mp -= 1

                else:
                    break


class player(character):
    
    def __init__(self, stage, name=input("What is your name?: ").title(), money=0, lvl=1, xp=0, items=[], health=20, mana=20):

        if name == "Satan" or name == "Lucifer" or name == "The Devil":
            
            health = 10
            mana = 30

        super().__init__(name, money, lvl, xp, items, health, mana)

        print("""
Your character has 3 stats: Stength, fortitude, and wisdom, each on a scale from 0 to 10.

Strength determines how much extra damage your character does with melee weapons, such as swords or axes.
Fortitude determines how much defense your character naturally has.
Wisdom determines how effective your character is with spells and magic weapons.

Your character can put one point into one of their states every 2 levels. You have 7 points to invest into your character right now.\n""")

        # This block of code is really dumb and bad, but I can't find a better implementation.
    
        stats_dict = {"Strength": 0, "Fortitude": 0, "Wisdom": 0}

        for key in stats_dict:
            while True:

                try:

                    val = int(input(f"How many points would you like to put into {key}? "))

                    if val >= 0:

                        stats_dict[key] = val

                        if sum([stats_dict[x] for x in stats_dict]) > 7:

                            print("Invalid number\n")
                            stats_dict[key] = 0

                            pass

                        else:
                            break

                    else:
                        pass

                except ValueError:

                    print("Invalid entry\n")
                    pass

        # Too bad!

        self.str = stats_dict["Strength"]
        self.fort = stats_dict["Fortitude"]
        self.wis = stats_dict["Wisdom"]

        self.royal = 0
        self.rebel = 0
        self.holy = 0
        self.unholy = 0

        self.armor = armor("oldClothes", "Worn out cloth garments", 0, 0)
        self.weapon = weapon("fists", "Can you really call your fists 'items?'", -500, 1, 0)
        self.items.extend([self.armor, self.weapon])

        self.encounter = False
        self.enemies = []
        self.kills = 0

        self.xp_dict = {1: 100, 2: 125, 3: 150, 4: 200, 5: 250, 6: 300, 7: 350, 8: 450, 9: 500, }
        print("Enter the command 'help' to see all commands.\n")

        print(f"""
{self.name}, level {self.level}

Health: {self.current_hp}/{self.max_hp}
Mana: {self.current_mp}/{self.max_mp}
            
Armor: {self.armor.name}, {self.armor.defense} defense
Weapon: {self.weapon.name}, {self.weapon.damage} damage
Money: {self.gold}g

Strength: {self.str}
Fortitude: {self.fort}
Wisdom: {self.wis + self.armor.magic} 
            """)

        self.stage = stage
        stage.active_stage(self)

    
    def player_death(self):
    
        input("\nGAME OVER! You have died! Press ENTER to end this program.")
        sys.exit()


    def change_hp(self, num):

        if num > 0:

            for i in range(num):

                if self.current_hp < self.max_hp:
                    self.current_hp += 1

                else:
                    break

        elif num < 0:

            for i in range((-num) - (self.armor.defense + self.fort)):

                if self.current_hp > 0:
                    self.current_hp -= 1

                if self.current_hp <= 0:
                    self.player_death()


    def run_command(self, *args):

        try:
            cmd = input().strip().split(" ")

        except KeyboardInterrupt:

            print("Invalid input\n")
            self.run_command()

        while cmd[0] != "help" and cmd[0] not in system().commands:
            cmd = input("Invalid command\n").strip().split(" ")

        if cmd[0] == "help":
            system().game_help(self)

        elif len(cmd) == 1:

            try:
                system().commands[cmd[0]](self)

            except TypeError:
                print("Missing parameter(s)\n")
                self.run_command()

        elif len(cmd) == 2:
            system().commands[cmd[0]](self, cmd[1])

        else:
            print("Invalid command\n")
            self.run_command()


    def gain_xp(self, num):

        self.xp += num

        if self.xp >= self.xp_dict[self.level]:

            self.level += 1

            skill = input("\nYou've leveled up! You can choose to permanently increase either your max health or your max mana by 5 points. Which do you choose? (hp/mp): ").lower().strip()
            while skill != "hp" and skill != "mp":
                skill = input("Invalid input. Choose either your max health or max mana to permanently increase by 5 points. (hp/mp): ").lower().strip()


            if skill == "hp":
                self.max_hp += 5
                print("You're max health has been increased by 5 points!\n")

            else:
                self.max_mp += 5
                print("You're max mana has been increased by 5 points!\n")


            if self.level % 2 == 0:

                stat = input("Every 2 levels you may invest 1 point into your stats. Would you like to increase your strength, fortitude, or wisdom? (s/f/w): ").lower().strip()
                while stat != "s" and stat != "f" and stat != "w":
                    stat = input("Invalid input. Would you like to increase your strength, fortitude, or wisdom? (s/f/w): ").lower().strip()

                if stat == "s":
                    self.str += 1

                elif stat == "f":
                    self.fort += 1

                else:
                    self.wis += 1

            self.current_hp = self.max_hp
            self.current_mp = self.max_mp
            self.xp = self.xp - self.xp_dict[self.level - 1]


    def give_item(self, item, statement=None):

        if isinstance(item, list):
            self.items.extend(item)

        else:
            self.items.append(item)

        if statement:
            print(statement)


    def start_encounter(self, targets):

        self.enemies.extend(targets)
        self.encounter = True

        while self.enemies:

            self.change_mp(1)
            self.run_command()

            for enemy in self.enemies:
                enemy.enemy_attack(self)

        self.encounter = False

        xp = sum([x.xp for x in targets])
        gold = sum([x.gold for x in targets])
        items = []

        for enemy in targets:
            items.extend(enemy.items)
            
        print(f"You have won the battle, earning {gold}g and {xp} experience points!\n")

        self.gold += gold
        self.give_item(items)
        self.gain_xp(xp)


class NPC(character):

    def __init__(self, name, money, lvl, xp, items, health=20, mana=0):

        super().__init__(name, money, lvl, xp, items, health, mana)
        self.visited = False

    
    def end_speech(self, player):

        print(f"{self.name}: Goodbye\n")
        player.run_command()


    def barter(self, player):

        if self.items:
        
            print(f"""{self.name}: Here's what I have available:
            
Item name, sell value, notes - Description
""")

            for item in self.items:

                if isinstance(item, weapon) or isinstance(item, magic_weapon):
                    print(f"{item.name}, {item.value}g, {item.damage} damage - {item.desc}")

                elif isinstance(item, armor):
                    print(f"{item.name}, {item.value}g, {item.defense} defense - {item.desc}")

                elif isinstance(item, consumable):
                    print(f"{item.name}, {item.value}g, {item.health} hp, {item.mana} mp - {item.desc}")

                else:
                    print(f"{item.name}, {item.value}g - {item.desc}")

            print(f"""\nWrite 'buy' followed by an item name to buy it. Write 'sell' followed by an item in yout inventory to sell it. Write 'items' to see your items. Write an integer after an 
item name to buy or sell in bulk. Write 'goodbye' to end conversation with this NPC.

{self.name}: {self.gold}g\n""")

            while True:

                answer = input().split()
                if len(answer) < 3:
                    answer.append(1)

                if answer[0].lower() == "buy" and answer[1] in [x.name for x in self.items]:

                    item = [x for x in self.items if x.name == answer[1]][0]
                    num = int(answer[-1])

                    if isinstance(item, consumable) or len([x for x in self.items if x.name == answer[1]]) >= num:
                        for x in range(num):

                            if player.gold >= item.value:

                                player.gold -= item.value

                                if not isinstance(item, consumable):
                                    item.value = item.value // 1.5

                                player.items.append(item)
                                self.gold += item.value

                                if not isinstance(item, consumable):
                                    self.items.remove(item)

                            else:
                                print("Not enough gold!\n")
                                break

                        print(f"{self.name} has {self.gold}g, you have {player.gold}g\n")
                    
                    else:
                        pass

                elif answer[0].lower() == "sell" and answer[1] in [x.name for x in player.items]:

                    item = [x for x in player.items if x.name == answer[1]][0]
                    num = int(answer[-1])

                    if item == player.weapon or item == player.armor:
                        print("You cannot sell an item that you have equipped.")

                    elif isinstance(item, consumable) or len([x for x in player.items if x.name == answer[1]]) >= num:
                        for x in range(num):

                            if self.gold >= item.value:

                                self.gold -= item.value

                                player.gold += item.value
                                player.items.remove(item)

                                if not isinstance(item, consumable):
                                    item.value = math.floor(item.value * 1.5)

                                self.items.append(item)

                            else:
                                print("This NPC cannot afford this item!\n")

                        print(f"{self.name} has {self.gold}g, you have {player.gold}g\n")

                    else:
                        pass

                elif answer[0].lower() == "items":
                    
                    print("\n")
                    for item in player.items:

                        if isinstance(item, weapon) or isinstance(item, magic_weapon):
                            print(f"{item.name}, {item.value}g, {item.damage} damage - {item.desc}")

                        elif isinstance(item, armor):
                            print(f"{item.name}, {item.value}g, {item.defense} defense - {item.desc}")

                        elif isinstance(item, consumable):
                            print(f"{item.name}, {item.value}g, {item.health} hp, {item.mana} mp - {item.desc}")

                        else:
                            print(f"{item.name}, {item.value}g - {item.desc}")

                    print("\n")

                elif answer[0].lower() == "goodbye":
                    self.end_speech(player)

                else:
                    print("Invalid entry\n")

        else:
            print(f"{self.name}: Sorry, I've got nothing to sell. Goodbye")
            player.run_command()


class enemy(character):

    def __init__(self, name, money, lvl, health, mana, damage, variant, defense, xp, items=[]):
        super().__init__(name, money, lvl, xp, items, health, mana)

        self.damage = damage
        self.variant = variant
        self.defense = defense

    
    def enemy_attack(self, player):

        damage = randint(self.damage - self.variant, self.damage + self.variant)

        old_hp = player.current_hp
        player.change_hp(-damage)
        new_hp = player.current_hp

        dam_dealt = abs(new_hp - old_hp)

        if damage == self.damage + self.variant:
            print(f"Critical hit! {self.name} attacks you, dealing {dam_dealt} damage! ({player.current_hp}/{player.max_hp} health)\n")

        elif dam_dealt == 0:
            print(f"Miss! {self.name} attacks you, dealing {dam_dealt} damage! ({player.current_hp}/{player.max_hp} health)\n")

        else:
            print(f"{self.name} attacks you, dealing {dam_dealt} damage! ({player.current_hp}/{player.max_hp} health)\n")

    
    def change_hp(self, num):

        if num > 0:

            for i in range(num):

                if self.current_hp < self.max_hp:
                    self.current_hp += 1

                else:
                    break

        elif num < 0:

            for i in range((-num) - self.defense):

                if self.current_hp > 0:
                    self.current_hp -= 1

                else:
                    break


    
# Item Classes

class item:

    def __init__(self, name, desc, value, age=0):
        
        self.name = name
        self.desc = desc
        self.value = value
        self.age = age


class weapon(item):

    def __init__(self, name, desc, value, dam, var, *args):
        super().__init__(name, desc, value)

        self.damage = dam
        self.variant = var

    
    def use(self, player):

        player.weapon = self
        print(f"You ready your {self.name}, granting {self.damage} damage.\n")


class magic_weapon(item):

    def __init__(self, name, desc, value, dam, cost, var, *args):
        super().__init__(name, desc, value)

        self.damage = dam
        self.variant = var
        self.cost = cost

    
    def use(self, player):

        player.weapon = self
        print(f"You ready your {self.name}, granting {self.damage} damage at the cost of {self.cost} mana.\n")


class armor(item):

    def __init__(self, name, desc, value, defense, *args):
        super().__init__(name, desc, value)

        self.defense = defense

        if args:
            self.magic = args[0]
        else:
            self.magic = 0

    
    def use(self, player):
        
        player.armor = self
        print(f"You equip your {self.name}, granting {self.defense} defense.\n")


class consumable(item):

    def __init__(self, name, value, hp, mp, *args):
        super().__init__(name, f"Grants {hp} health and {mp} mana", value)

        self.health = hp
        self.mana = mp

    
    def use(self, player):

        old_hp = player.current_hp
        old_mp = player.current_mp
        
        player.change_hp(self.health)
        player.change_mp(self.mana)

        hp_change = player.current_hp - old_hp
        mp_change = player.current_mp - old_mp

        player.items.remove(self)
        print(f"You consume your {self.name}, granting {hp_change} health and {mp_change} mana.\n")


class heal_spell(item):

    def __init__(self, name, desc, value, heal, cost, *args):
        super().__init__(name, desc, value)

        self.heal = heal
        self.cost = cost

    
    def use(self, player):

        if player.current_mp < self.cost:

            print("You don't have enough mana to use this spell!\n")
            return

        old_hp = player.current_hp
        player.change_hp(self.heal + player.wis + player.armor.magic)
        hp_change = player.current_hp - old_hp

        player.change_mp(-self.cost)

        print(f"Using your {self.name}, you gain {hp_change} health at the cost of {self.cost} mana.\n")


class stat_potion(item):

    def __init__(self, name, value, desc, hp, mp, add, *args):
        super().__init__(name, desc, value)

        self.health = hp
        self.mana = mp
        self.add = add

    
    def use(self, player):

        if self.add:

            if self.health != 0:

                player.max_hp += self.health
                player.current_hp = player.max_hp

                if player.max_hp <= 0:
                    player.player_death()

            if self.mana != 0:

                player.max_mp += self.mana
                player.current_mp = player.max_mp

                if player.max_mp < 0:

                    player.max_mp = 0
                    player.current_mp = 0

        else:

            if self.health > 0:

                player.max_hp = math.floor(player.max_hp * self.health)
                player.current_hp = player.max_hp

            elif self.health < 0:

                self.health = abs(self.health)

                player.max_hp //= self.health
                player.current_hp = player.max_hp

                if player.max_hp <= 0:
                    player.player_death()


            if self.mana > 0:

                player.max_mp = math.floor(player.max_mp * self.mana)
                player.current_mp = player.max_mp

            elif self.mana < 0:

                self.mana = abs(self.mana)

                player.max_mp //= self.mana
                player.current_mp = player.max_mp

                if player.max_mp <= 0:
                    
                    player.max_mp = 0
                    player.current_mp = 0

        player.items.remove(self)
        print(f"You consume your {self.name}! Your stats have changed.\n")
            


# Stage Class

class stage:

    def __init__(self, north, west, south, east, npcs, *args):

        self.north = north
        self.west = west
        self.south = south
        self.east = east
        self.indirects = args

        if isinstance(north, stage):
            north.south = self

        if isinstance(west, stage):
            west.east = self

        if isinstance(south, stage):
            south.north = self

        if isinstance(east, stage):
            east.west = self

        self.chars = npcs
        self.visited = False
