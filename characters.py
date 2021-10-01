import system as RPG
import sys
import math
from random import randint
import stages


# NPC Setups

class shopKeeper(RPG.NPC):
    
    def info(self, player):
        
        answer = input(f"""\n{self.name}: Why, we're in the Kingdom of Talia, specifically the capital city of Manhet. I am the owner of this stand. Would you like to buy my wares?

1. Yes, I'd like to barter.
2. No thanks. (Goodbye)
""")

        answer_dict = {"1": self.barter, "2": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def greeting(self, player):

        answer = input(f"""\n{self.name}: Hello again traveler. Have you returned to purchase my wares?

1. Yes, I'd like to barter.
2. No thanks, (Goodbye)
""")

        answer_dict = {"1": self.barter, "2": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)

    
    def introduction(self, player):
        
        self.visited = True
        answer = input(f"""\n{self.name}: Hello traveler. Are you interested in purchasing supplies?

1. Yes, what do you sell?
2. Who are you? Where are we?
3. Goodbye\n
""")

        answer_dict = {"1": self.barter, "2": self.info, "3": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)



class blacksmith(RPG.NPC):

    def reforge(self, player):
        
        print(f"""{self.name}: I can improve the effectiveness of your weapons and armor for twice the cost of the item itself. What would you like improved?
        
(Improving weapons and armor will add 1 to the item's defense/damage. This will also increase the item's value by 50% of its current price. Enter the item's name to improve it, enter 'goodbye'
to end conversation with this NPC, and enter 'items' to see your items.)\n""")

        while True:

            answer = input().strip()

            if answer.lower() == "items":

                print("\n")
                for item in player.items:

                    if isinstance(item, RPG.weapon) or isinstance(item, RPG.magic_weapon):
                        print(f"{item.name}, {item.value}g, {item.damage} damage - {item.desc}")

                    elif isinstance(item, RPG.armor):
                        print(f"{item.name}, {item.value}g, {item.defense} defense - {item.desc}")

                    elif isinstance(item, RPG.consumable):
                        print(f"{item.name}, {item.value}g, {item.health} hp, {item.mana} mp - {item.desc}")

                    else:
                        print(f"{item.name}, {item.value}g - {item.desc}")

                print("\n")

            elif answer.lower() == "goodbye":
                self.end_speech(player)

            elif answer in [x.name for x in player.items]:

                item = [x for x in player.items if x.name == answer][0]

                if isinstance(item, RPG.magic_weapon):
                    print(f"{self.name}: Get this demonic magic away from me!\n")

                elif isinstance(item, RPG.weapon) and player.gold >= (item.value * 2):
                    
                    if item.name == "rustySword":
                        print(f"{self.name}: This weapon is too broken to improve.\n")

                    elif item.name == "fists" or item.name == "staleBread":
                        print(f"{self.name}: What?\n")

                    else:
                    
                        player.gold -= (item.value * 2)
                        self.gold += (item.value * 2)

                        item.damage += 1
                        item.value = math.floor(item.value * 1.5)

                        print(f"{self.name} has {self.gold}g, you have {player.gold}g\n")

                elif isinstance(item, RPG.armor) and player.gold >= (item.value * 2):
                    
                    if item.name == "oldClothes":
                        print("This armor is too old to improve.\n")

                    elif item.name == "guardArmor":
                        print("I'm afraid this armor is too good for me to improve.\n")
                    
                    else:

                        player.gold -= (item.value * 2)
                        self.gold += (item.value * 2)

                        item.defense += 1
                        item.magic += 1
                        item.value = math.floor(item.value * 1.5)

                        print(f"{self.name} has {self.gold}g, you have {player.gold}g\n")

                elif not isinstance(item, RPG.weapon) and not isinstance(item, RPG.armor):
                    print("Invalid entry")

                else:
                    print("Not enough gold!\n")


    def info2(self, player):

        if player.rebel == 0:
            player.rebel += 1
        
        answer = input(f"""\n{self.name}: Clement and his group of nutters that meet in the local saloon every now and again, they believe that our soldiers have been cruel in the way they expanded 
into tribal lands, saying that innocent civilians were slaughtered by out troops. These are just rumors, however, and there's no evidence of such things. Now, do you have any interet in 
purchasing equipment?

1. Yes, I'd like to see what you have in stock.
2. No thanks. (Goodbye)\n
""")

        answer_dict = {"1": self.barter, "2": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)

    
    def info1(self, player):
        
        answer = input(f"""\n{self.name}: We're in the Kingdom of Talia. Talia is a kingdom known for being somewhat aggressive on the world stage. Within the last 3 decades, Talia has expanded into the ancestral lands 
of local tribes. Some say our soldiers are rather barbaric, but I like to think of them as just doing their duty. Our king isn't the nicest, but he keeps us safe.

1. Have you got anything for sale?
2. Who says that the military is barbaric?
3. Goodbye.\n
""")

        answer_dict = {"1": self.barter, "2": self.info2, "3": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def greeting(self, player):

        if player.armor.name == "guardArmor":
            print(f"\n{self.name}: Hullo sir, what can I get you?\n")

        else:
            print(f"\n{self.name}: Hullo again, have you come to make a purchase?\n")

        print("""1. Yes, I'd like to barter.
2. I have equipment I need improved.
3. What did you say about Talia again?
4. Goodbye
""")

        answer_dict = {"1": self.barter, "2": self.reforge, "3": self.info1, "4": self.end_speech}

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)

    
    def introduction(self, player):
        
        self.visited = True

        if player.armor.name == "guardArmor":
            print(f"\n{self.name}: Hullo sir, what can I get you?\n")

        else:
            print(f"\n{self.name}: Hullo there, are you new in Manhet?\n")

        print("""1. I'm looking for equipment. What have you got for sale?
2. Are you able to improve my equipment?
3. What can you tell me about the kingdom we're currently in?
4. Goodbye
""")

        answer_dict = {"1": self.barter, "2": self.reforge, "3": self.info1, "4": self.end_speech}

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)



class barkeep(RPG.NPC):

    def fight(self, player):

        player.stage.chars.remove(self)
        enemy = RPG.enemy(f"barkeep", randint(10, 20), 2, 20, 0, 10, 3, 1, 30)

        print(f"{self.name}: To hell with the king! Vive la revolution!\n")
        player.start_encounter([enemy])

        player.royal = 4
        player.rebel = -5

        player.kills += 1

        print("""The young man you've just slaughtered lies on the ground, and everyone in the bar has left. You have found the evidence of anti-king sentiment you were looking for.
What do you want to do?\n""")

        if player.stage.chars:
            player.stage.flee()

        player.run_command()


    def info3(self, player):
        
        answer = input(f"""\n{self.name}: Indeed I am, hence why I host them here and provide them with food and drink. If you tell the guards you're getting shanked.

1. What can I buy, comrade?
2. Goodbye
""")

        answer_dict = {"1": self.barter, "2": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)



    def info2(self, player):
        
        answer = input(f"""\n{self.name}: Aye, those are our comrades. They don't much like the King either.

1. What do you have for sale?
2. Are you a member of the rebellion?
2. Goodbye
""")

        answer_dict = {"1": self.barter, "2": self.info3, "3": self.info3}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def info1(self, player):
        
        answer = input(f"""\n{self.name}: That's none of your business. Are you here to buy refreshments or not?

1. What do you have? 
2. No thanks
""")

        answer_dict = {"1": self.barter, "2": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)

    
    def introduction(self, player):
        
        if player.rebel >= 3:
            print("What can I get you, comrade?\n")

        elif player.armor.name == "guardArmor" or player.royal >= 3:
            print("What do *you* want?\n")

        else:
            print("Hungry, thirsty, or both?\n")

        print("""1. Nevermind (Goodbye)
2. What've you got?""")

        answer_dict = {"1": self.end_speech, "2": self.barter}

        if player.armor.name == "guardArmor":

            print("3. Excuse me, there have been reports of sentiment against the king within your establishment. Are you aware of this?")
            answer_dict["3"] = self.fight

        elif len(player.stage.chars) == 2:

            print("3. Who's in that quiet group over there?")

            if player.rebel >= 3:
                answer_dict["3"] = self.info2
            else:
                answer_dict["3"] = self.info1
 
        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)



class recruiter1(RPG.NPC):

    def fight(self, player):

        player.stage.chars.remove(self)
        enemy1 = RPG.enemy("soldier", 0, 5, 35, 20, 15, 5, 2, 60, [])

        player.start_ecounter([enemy1])
        player.royal = -2

        player.kills += 1
        player.run_command()


    def info2(self, player):

        self.visited = True
        answer = input(f"""\n{self.name}: To join the military, speak to the recruiter in the barracks just passed the castle gate south of here. The guards'll let you passed if you're joining the army.

1. Thank you, goodbye.
""")
        
        player.royal += 1
        answer_dict = {"1": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)

    
    def info1(self, player):
        
        answer = input(f"""\n{self.name}: Serving the Kingdom of Talia provides a good line of work with many rewards. Soldiers are given all the equipment they need, and are paid much better than the peasantry.

1. Where do I go to join the army?
2. I'm not interested
""")

        answer_dict = {"1": self.info2, "2": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def greeting(self, player):

        answer = input(f"""\n{self.name}: What is it?

1. Nothing.
""")

        answer_dict = {"1": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)

    
    def introduction(self, player):
        
        answer = input(f"""\n{self.name}: DO YOUR DUTY TO THE KING, JOIN THE MILITARY! 

1. Why should I join the army?
2. Where do I go to join the army?
3. ... (Goodbye)
""")

        answer_dict = {"1": self.info1, "2": self.info2, "3": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)



class king(RPG.NPC):

    def fight(self, player):

        player.stage.chars.remove(self)
        enemy1 = RPG.enemy("King", 0, 10, 65, 0, 20, 5, 3, 0)

        print(f"{self.name}: You dare challenge your lord to a fight? I'll gut you like a fish!\n")
        player.start_encounter([enemy1])

        if player.rebel >= 3:
            print("""
            
You have slain the king, the tyrant of Talia. You and your comrades celebrate your victory and announce your plans to all of Manhet. Together, you form a commune where all citizens
are equal, end Talia's unnecessary wars, and increase the overall standard of living. Manhet becomes a city-state and the rest of Talia becomes fractured, but free.
            
REBEL ENDING: Kill the King as a member of the revolutionaries. Ending 4/5""")

            sys.exit()

        elif player.unholy >= 4:

            player.kills += 1
            print("You stand alone in the now empty palace. What do you want to do?\n")

            player.run_command()

        else:
            print("""
            
You have backstabbed the King himself. You stand above as the strongest warrior of the land, and therefore hailed as the new monarch. You rule with a deadly, iron fist. You expand
Talia into a massive empire while doing whatever you can to expand your own power, no matter the cost.
            
BETRAYAL ENDING: Kill the King as a member of the Royal Army. Ending 5/5""")


    def ending(self, player):

        print(f"""{self.name}: Welcome aboard, General {player.name}.
        

You are sent to lead on the front lines of Talia's ongoing war of conquest. You lead several successful military campaigns and help expand Talia's borders. You become a prestigious
military leader and live a well off life. The only struggle you face is your slight regret in the face of all those you've killed along the way.

ROYAL ENDING: Join the King. Ending 3/5""")

        sys.exit()

    
    def info1(self, player):
        
        answer = input(f"""\n{self.name}: Well then, you may just have secured my crown. For this, in spite of the fact that you're a relatively new recruit, I offer you a job as a general for the Kingdom of Talia
on the front lines of the ongoing war. You've proven yourself to be an adequet warrior, and they need all the hands they can get at the front lines. What are your thoughts on this?

1. I accept your proposal.
2. Death to tyrants!
""")

        answer_dict = {"1": self.ending, "2": self.fight}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)

    
    def introduction(self, player):
        
        answer = input(f"""\n{self.name}: So, you're the soldier they tell me fought off the so-called "rebellion," is this true?

1. Yes sir.
2. I *am* the revolution!
""")

        answer_dict = {"1": self.info1, "2": self.fight}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)



class recruiter2(RPG.NPC):

    def fight(self, player):
        
        print(f"{self.name}: Guards, kill them!\n")
        player.stage.chars.remove(self)

        enemy1 = RPG.enemy("soldier", 0, 3, 20, 0, 12, 5, 2, 30, [])
        enemy2 = RPG.enemy("royalGeneral", 0, 5, 35, 0, 14, 5, 5, 30, [])

        player.start_encounter([enemy1, enemy2])
        player.royal = -3

        player.stage.east = stages.castleStage4(None, player.stage, None, None, [])

        item1 = RPG.item("barracksKey", "The key to the barracks of the royal army of Manhet.", 0)
        player.give_item(item1, "You slaughter the recruiter and royal general, looting the key to the armory to your east. What do you want to do?")
        player.kills += 1

        player.run_command()

    
    def success2(self, player):

        player.royal = 7

        king1 = king("theKing", 0, 10, 0, [])
        player.stage.west.south = stages.castleStage5(player.stage.west, None, None, None, [king1])
        
        answer = input(f"""\n{self.name}: You eliminated them all by yourself? In all honesty, I was sending you alone as a reacon mission rather than an actual fighting force. If you've eliminated the revolutionaries,
then you've done a great service to the King. As such, I think it's only right for you to speak to him. He may have a reward in mind for you. Enter the large stone keep to the south west.

1. Yes sir!
""")

        answer_dict = {"1": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")


    def deny(self, player):
        
        answer = input(f"""\n{self.name}: You don't seem right for military service. I ask that you please leave the castle grounds immediately.

1. Vive la révolution! (fight)
2. Yes sir.
""")
        answer_dict = {"1": self.fight, "2": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def prefight(self, player):

        answer = input(f"""\n{self.name}: Excuse me? Only military personnel and recruits are allowed within the barracks.

1. ...
""")
        answer_dict = {"1": self.fight}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def info6(self, player):

        print(f"""\n{self.name}: We need you to head into the forest up north to look for these "revolutionaries." End their little resistance.

1. Understood!""")

        answer_dict = {"1": self.end_speech}

        if player.royal == 6:

            print("2. I've eliminated the rebels.")
            answer_dict["2"] = self.success2

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def success1(self, player):
        
        player.royal = 5
        answer = input(f"""\n{self.name}: A revolution? Well that explain the attack at the front gate earlier. A group of people had attacked a guard while running towards the forest after your left to go investigate.
I'll need you to go into the forest to try and find these "revolutionaries." Put this rebellion down once and for all.

1. Yes sir!
""")

        answer_dict = {"1": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)        


    def info5(self, player):

        answer = input(f"""\n{self.name}: That soldier is healing his wounds from battle on the front lines, so we had him act as a recruiter. Any more questions?

1. Nope, I understand my assignment.
""")

        answer_dict = {"1": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)        


    def info4(self, player):

        print(f"""\n{self.name}: There've been reports of sentiment against the king in to local tavern. We'll need you to investigate.

1. Understood!
2. There's a soldier stationed just outside the bar, why can't he investigate?""")

        answer_dict = {"1": self.end_speech, "2": self.info5}

        if player.royal == 4:

            print("3. I investigated the bar, I was forced to kill the barkeep. He mentioned something about a revolution before he attacked me.")
            answer_dict["3"] = self.success1

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)        


    def goal(self, player):

        if player.royal <= 4:
            self.info4(player)

        elif player.royal <= 6:
            self.info6(player)


    def join(self, player):
        
        player.royal = 3
        player.items.remove([x for x in player.items if x.name == "dogTags"][0])

        food1 = RPG.consumable("bread", 5, 1, 0)
        food2 = RPG.consumable("sausage", 5, 1, 0)
        weapon1 = RPG.weapon("steelSword", "A run-of-the-mill steel sword", 25, 5, 3)
        armor1 = RPG.armor("guardArmor", "The armor and uniform worn by the guards of the city of Manhet", 10, 3)

        equipment = [food1, food2, weapon1, armor1]
        player.items.extend(equipment)

        answer = input(f"""\n{self.name}: A lich? Well that explains why we've lost so many soldiers. Well then, it appears you've proven yourself to be in service of the King. Here's your equipment and provisions.
Take some coin for your work. Check in with me when you're ready for your first assignment

1. What's my first assignment?
2. Understood! (goodbye)
""")

        answer_dict = {"1": self.info4, "2": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        player.gold += 15

        answer_dict[answer](player)


    def info3(self, player):

        answer = input(f"""\n{self.name}: We can't risk losing military equipment. The new frontier to the east is very taxing on supplies, so we need to ensure every new recruit doesn't pawn off whatever we give them 
before they're registered. As a citizen of Talia it's your duty to serve the King, anyhow. Now, get to it!

1. ... (goodbye)
""")

        answer_dict = {"1": player.run_command}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def info2(self, player):

        self.visited = True
        player.royal += 1

        print(f"""\n{self.name}: There've been reports of wild life killing soldiers in the forest north of the city. If you kill off the wild life and retrieve the soldiers' dog tags then you will be offically
registered for military service. Understood?

1. Understood! (goodbye)
2. This sounds like a ploy for free labor.""")

        answer_dict = {"1": self.end_speech, "2": self.info3}

        if "dogTags" in [x.name for x in player.items]:
            
            print("3. I found these dogtags in the forest after fighting a lich.")
            answer_dict["3"] = self.join

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def info1(self, player):

        answer = input(f"""\n{self.name}: Well then, we'd better get you outfitted. Before we can trust you with military equipment, we need you to prove you won't run off with whatever we give you and sell it to the nearest
merchant. We'll need to mark down your name and have you complete a some basic work. After that, you'll be provided with your uniform and supplies and given your first assignment. Understood?

1. Understood. My name is {player.name}. What's the job I need to complete?
2. Now I'm not sure if I should join, I need some time to think. (goodbye)
""")

        answer_dict = {"1": self.info2, "2": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def final_greeting(self, player):

        answer = input(f"""\n{self.name}: Go speak to the King in the keep, he most likely has a reward for your work.

1. Yes sir.
""")

        answer_dict = {"1": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)
        


    def friendly_greeting(self, player):

        answer = input(f"""\n{self.name}: Greetings, soldier. What are you here for?

1. What's my current assignment?
2. Nevermind
""")

        answer_dict = {"1": self.goal, "2": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def neutral_greeting(self, player):

        print(f"""\n{self.name}: Have you retrieved the dog tags from the forest?

1. Not yet. (goodbye)""")

        answer_dict = {"1": self.end_speech}

        if "dogTags" in [x.name for x in player.items]:

            print("2. Yes, here they are.")
            answer_dict["2"] = self.join

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def greeting(self, player):

        if player.royal == 7:
            self.final_greeting(player)

        elif player.royal >= 3:
            self.friendly_greeting(player)

        elif player.royal < 0:
            self.fight(player)

        else:
            self.neutral_greeting(player)

    
    def introduction(self, player):

        if player.royal < 0:
            self.fight(player)
        
        else:
        
            print(f"""\n{self.name}: Have you come to join the military?

1. Yes, I have.
2. No, just looking around.""")

            answer_dict = {"2": self.prefight}

            if player.rebel >= 2:
                answer_dict["1"] = self.deny
                
            else:
                answer_dict["1"] = self.info1

            answer = input("\n")
            while answer not in answer_dict:
                answer = input("Invaid response\n")

            answer_dict[answer](player)



class church(RPG.NPC):

    def fight(self, player):
        
        print(f"{self.name}: Mercy! Mercy! Please, I beg you!\n")

        enemy1 = RPG.enemy("bishop", 0, 1, 5, 0, 0, 0, 0, 0)

        player.stage.chars.remove(self)
        player.start_encounter([enemy1])

        player.unholy = 3
        player.holy = -5
        
        if player.royal < 0:
            player.royal -= 2
        
        else:
            player.royal = -2
        
        player.kills += 1
        player.give_item(RPG.item("brokenSword", "The hilt of a great warrior's shattered sword. The handle is beautifully carved.", 0), "\nAs you stand in front of the Bishop's body, you walk over to the impaled stone. You grab the sword at the hilt and shatter the blade. What do you want to do?\n")
        player.run_command()


    def info2(self, player):

        answer = input(f"""\n{self.name}: There is only one thing left for the church to accomplish, but it's exceptionally dangerous. To ultimately serve the lord, we must banish Lucifer from this world. If you
think yourself strong enough, you must kill satan himself!

1. For the lord, I shall risk my life!
2. I need to think this over...
""")

        answer_dict = {"1": self.end_speech, "2": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def sword(self, player):

        print(f"""\n{self.name}: Be my guest. It is written that only a truly holy warrior can successfully pull the sword, a true heir to Arthur. Many try their hand thinking they're a miracle to the
world, when they never can pull it. You, however, have shown yourself to be dedicated to the church. Perhaps you'll pull it.

As you approach the stone in the middle of the church, you grasp the handle of the sword. You feel a burst of adrenaline and strength like never before. As you pull with all your might,
the sword gives and is pulled from the stone. You have been chosen to carry on the sword's legacy. What do you want to do?
""")
        player.items.append(RPG.weapon("holySword", "The sword of a great, holy warrior. The handle is beautifully carved and the blade shines with the brightest silver.", 100, 20, 5))
        player.run_command()


    def reward2(self, player):

        answer = input(f"""\n{self.name}: Why, of course. You've done a great service for the lord, take these to salve yourself. Is there anything else you require?

1. No father, goodbye.
2. Is there anything else I can do to assist the church?""")

        answer_dict = {"1": self.end_speech, "2": self.info2}

        if player.max_mp <= 20 and player.str >= 5 and player.wis == 0:

            print("3. I'd like to try my hand at pulling the sword.")
            answer_dict["3"] = self.sword

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def join(self, player):
        
        player.items.remove([x for x in player.items if x.name == "holyText"][0])
        player.holy = 4

        print(f"""\n{self.name}: By Jehovah, you've recovered the ancient texts! You've proven yourself to be a true servant of god, and I cannot thank you enough for recovering this priceless artifact.
Is there anything I could do for you? Anything at all?

1. No father, my work for the lord is priceless (Goodbye)
2. Satan has greatly weakened me in exhange for the text, I require holy water.
3. Is there any more work to be done for the church?""")

        answer_dict = {"1": self.end_speech, "2": self.reward2, "3": self.info2}

        if player.max_mp <= 20 and player.str >= 5 and player.wis == 0:

            print("4. I'd like to try my hand at pulling the sword.")
            answer_dict["4"] = self.sword

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def reward1(self, player):
        
        player.items.remove([x for x in player.items if x.name == "demonHorn"][0])

        item1 = RPG.consumable("holyWater", 20, 15, -30)
        player.items.append(item1)

        print(f"""\n{self.name}: Ah, you've slayed a demon! Great job, you're serving the lord well. As a reward, I grant you a vile of holy water to salve yourself with in combat. May it serve you well.

1. Thank you, father. (goodbye)""")

        answer_dict = {"1": self.end_speech}

        if "holyText" in [x.name for x in player.items]:

            print("2. I've recovered the ancient text.")
            answer_dict["2"] = self.join

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def lore(self, player):

        answer = input(f"""\n{self.name}: The church was created to preserve the legacy of the holy warrior King Arthur. It is written that Arthur was the first king of the Kingdom of Talia, and that he was devoted to the
service of the lord. It is said that the Lady of the Lake, her arm clad in the purest shimmering samite, held aloft Excalibur from the bosom of the water, signifying by divine providence 
that he, Arthur, was to carry a magical sword. His sword is embedded in that rock in the center of the church. We preserve his legacy by ridding the world of demons, hoping to one day kill
Lucifer himself, the source of all evil.

1. What can I do to help the church?
2. Interesting (Goodbye)
""")
        answer_dict = {"1": self.info1, "2": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def info1(self, player):

        if player.holy < 2:
            player.holy = 2

        print(f"""\n{self.name}: Currently, the church has two main goals. The first being to remove demons from the world, which we verify by requesting all who slay a demon bring a horn from the beast. This
is rewarded with a vile a healing holy water. Next, the church seeks to recover one of the lord's ancient holy text, one which was stolen decades ago by a demon. 

1. Interesting. I'll do what I can. (Goodbye)""")

        answer_dict = {"1": self.end_speech}

        if "demonHorn" in [x.name for x in player.items]:

            num = len(answer_dict) + 1

            print(f"{num}. I have the horn of a demon I've slain.")
            answer_dict[str(num)] = self.reward1

        if "holyText" in [x.name for x in player.items]:

            num = len(answer_dict) + 1

            print(f"{num}. I've recovered the holy text.")
            answer_dict[str(num)] = self.join

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def greeting(self, player):

        print(f"""\n{self.name}: Greetings, my child. What is it you require?

1. Nothing (Goodbye)
2. What is the history of the church?
3. Your church is corrupt, prepare to die!
4. How may I assist the church?""")

        answer_dict = {"1": self.end_speech, "2": self.lore, "3": self.fight}

        if player.holy < 4:
            answer_dict["4"] = self.info1
        else:
            answer_dict["4"] = self.info2

        if "demonHorn" in [x.name for x in player.items] and player.holy >= 2:

            num = len(answer_dict) + 1

            print(f"{num}. I have the horn of a demon I've slain.")
            answer_dict[str(num)] = self.reward1

        if "holyText" in [x.name for x in player.items] and player.holy >= 2:

            num = len(answer_dict) + 1

            print(f"{num}. I've recovered the holy text.")
            answer_dict[str(num)] = self.join

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)

    
    def introduction(self, player):
        
        self.visited = True
        answer = input(f"""\n{self.name}: Greetings, my child. What is it you require?

1. How may I assist the church?
2. What is the history of the church?
3. Your church is corrupt, prepare to die!
4. Nothing (Goodbye)
""")

        answer_dict = {"1": self.info1, "2": self.lore, "3": self.fight, "4": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)



class guard(RPG.NPC):

    def fight(self, player):
        
        player.stage.chars.remove(self)
        enemy = RPG.enemy(f"guard", 0, 2, randint(15, 20), 0, 10, 3, 1, randint(20, 35))

        print("guard: Then pay with your blood!\n")
        player.start_encounter([enemy])
        player.royal = -2

        player.kills += 1

        player.stage.south = stages.castleStage2(player.stage, None, "Blocked", stages.castleStage3(None, None, None, "Blocked", [recruiter2("recruiter", 0, 1, 0, [])]) , [])
        print("With the guards blocking the way south dead on the ground, you are now free to enter the castle's courtyard. What do you want to do?")
        player.run_command()


    def info1(self, player):

        player.stage.south = stages.castleStage2(player.stage, None, "Blocked", stages.castleStage3(None, None, None, "Blocked", [recruiter2("recruiter", 0, 1, 0, [])]) , [])
        self.visited = True

        print(f"{self.name}: Well then, continue south to the barracks.\n")
        player.run_command()


    def greeting(self, player):
        
        answer = input(f"""\n{self.name}: What is it?

1. Nothing (Goodbye)""")

        answer_dict = {"1": player.run_command}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)

    
    def introduction(self, player):
        
        print(f"""\n{self.name}: Military personnel only!

1. ... (Goodbye)""")

        answer_dict = {"1": player.run_command}

        if player.royal >= 1:

            print("2. I've come to join the army.")
            answer_dict["2"] = self.info1

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)



class potionSeller(RPG.NPC):

    def fight(self, player):
        
        player.stage.chars.remove(self)
        enemy = RPG.enemy("potionSeller", randint(20, 35), 3, 30, 20, 10, 3, 2, 35)

        print(f"{self.name}: You'll never take me alive!\n")
        player.start_encounter([enemy])

        player.rebel = -5
        player.unholy = 1

        print("The old man lays dead on the ground. What do you want to do?\n")
        player.run_command()


    def rebel_quest(self, player):
        
        player.rebel = 4
        answer = input(f"""\n{self.name}: Of course, I'd be happy to host the rebels here. It'd do Manhet good to be run by the people anyhow.

1. Thank you for your help, goodbye.
""")

        answer_dict = {"1": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def info(self, player):

        print(f"""\n{self.name}: Talia is cruel and imperialist. The king is greedy and has no regard for the common man. I built my home and business away from Manhet for a reason.

1. Interesting (Goodbye)""")

        answer_dict = {"1": player.run_command}

        if player.armor.name == "guardArmor":
            num = len(answer_dict)
            
            print(f"{num}. As a representative of the King I demand that you pay taxes on your earnings.")
            answer_dict[str(num)] = self.fight

        elif player.rebel == 3:
            num = len(answer_dict)

            print(f"{num}. I've been sent by the rebellion within Manhet to request you provide shelter if the rebels need to escape the city.")
            answer_dict[str(num)] = self.rebel_quest

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def deny(self, player):
        
        answer = input(f"""\n{self.name}: My potions are to strong for you, traveler. Seek your potions elsewhere.

1. You have no respect, potion seller. No respect for anything other than your potions. (Goodbye)
""")

        answer_dict = {"1": player.run_command}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)

    
    def introduction(self, player):
        
        self.name = "potionSeller"
        
        print(f"""\n{self.name}: Hello there. Have you come to purchase one of my many elixirs? 

1. No thanks.
2. Potion seller, I am going into battle, I require your strongest potions.
3. What's your stance on the kingdom of Talia?""")

        answer_dict = {"1": self.end_speech, "3": self.info}

        if player.level >= 3:
            answer_dict["2"] = self.barter

        else:
            answer_dict["2"] = self.deny


        if player.armor.name == "guardArmor":
            num = len(answer_dict) + 1
            
            print(f"{num}. As a representative of the King I demand that you pay taxes on your earnings.")
            answer_dict[str(num)] = self.fight

        elif player.rebel == 3:
            num = len(answer_dict) + 1

            print(f"{num}. I've been sent by the rebellion within Manhet to request you provide shelter if the rebels need to escape the city.")
            answer_dict[str(num)] = self.rebel_quest

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)



class rebelLeader(RPG.NPC):

    def fight(self, player):
        
        print(f"{self.name}: Kill them, comrades!\n")

        enemy1 = RPG.enemy("rebel1", 0, 5, 20, 10, 10, 3, 2, 60, [])
        enemy2 = RPG.enemy("rebel2", 0, 5, 20, 10, 10, 3, 2, 60, [])
        enemy3 = RPG.enemy("rebelLeader", 10, 7, 45, 25, 15, 5, 2, 60, [])

        enemies = [enemy1, enemy2, enemy3]

        if "oldMan" in [x.name for x in player.stage.chars] or "potionSeller" in [x.name for x in player.stage.chars]:
            enemies.append(RPG.enemy("potionSeller", randint(20, 35), 3, 30, 20, 10, 3, 2, 35))

        player.stage.chars = []
        player.start_encounter(enemies)

        player.rebel = -5
        player.royal = 6

        player.kills += 1

        if type(player.stage).__name__ == "forestStage4":
            print("You have defeated the leader of the rebellion against the king. To the east stands the dark forest from which you entered. What do you want to do?\n")
        
        else:
            print("You have defeated the leader of the rebellion against the king. To the east is the center of the city. What do you want to do?\n")

        player.run_command()


    def success1(self, player):

        answer = input(f"""\n{self.name}: Great work comrade. This, in addition to the preparations completed by other members of the rebellion, allows us to begin our final plan. We begin a formal seige against
the castle just south of here and kill the king himself! It won't be easy, but we must fight our way to the king himself and end his rule. 

1. Let us finally revolt!
2. I'll need a second to prepare.
""")

        if answer == "1":
            player.rebel = 5

        self.end_speech(player)


    def info5(self, player):

        answer = input(f"""\n{self.name}: Our final step is to seige the king's castle and fight our way to the king himself. We must end his rule permanently.

1. Let us revolt to end tyranny!
2. I need some more time to prepare.
""")

        if answer == "1":
            player.rebel = 5

        self.end_speech


    def info4(self, player):

        print(f"""\n{self.name}: In case we need to flee during an ambush from the guards, we need a path to one of our allies deep in the forest up north. Recently wildlife has made this difficult. We'll
need you to kill any aggressive wildlife that blocks the path so we can have an emergency escape if necessary. 

1. Understood.""")

        answer_dict = {"1": self.end_speech}

        if player.rebel == 4:

            print("2. I have cleared the way and asked the potion seller to prepare in case must escape.")
            answer_dict["2"] = self.success1

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def goal(self, player):

        if player.rebel <= 4:
            self.info4(player)

        else:
            self.info5(player)

    
    def join(self, player):
        
        player.rebel = 3
        
        item1 = [x for x in player.items if x.name == "suppliesCrate"][0]
        player.items.remove(item1)

        answer = input(f"""\n{self.name}: The general herself?? You must be a skilled fighter. Thank you for the supplies, you've earned our trust and we can depend on you. 

1. What can I do to help next?
2. Goodbye
""")

        answer_dict = {"1": self.goal, "2": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        player.gold += 15

        answer_dict[answer](player)


    def neutral(self, player):
        
        answer = input(f"""\n{self.name}: What we're up to is none of your business, now kindly leave.

1. Nobody talks back to me! (Fight)
2. Sorry for interupting. (Goodbye)
""")

        answer_dict = {"1": self.fight, "2": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def lore(self, player):

        answer = input(f"""\n{self.name}: Our main goal is to start a revolution and to overthrow the king, replacing the monarchy with an anarcho-syndicalist commune where we take it in turns to act as a sort of 
executive officer for the week, but all the decisions of that officer have to be ratified at a special bi-weekly meeting by a simple majority in the case of purely internal affairs, but by 
a two-thirds majority in the case of purely external affairs. An autonomous collective of sorts.

1. Interesting. (Goodbye)
""")

        answer_dict = {"1": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def info3(self, player):
        
        print(f"""\n{self.name}: You can earn our trust by stealing some supplies from the royal barracks, as we're running low and could use the weaponry. It's dangerous, but members of our group need to 
be able to handle themselves in a fight. Make sure you're well prepared in case you find any trouble.

1. I'll get you those supplies.
2. I need time to think it over. (Goodbye)""")

        answer_dict = {"1": "Special response, no method", "2": self.end_speech}

        if "suppliesCrate" in [x.name for x in player.items]:

            print("3. I've already stolen supplies from the armory, I had to fight the royal general.")
            answer_dict["3"] = self.join

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        if answer == "1":

            print(f"{self.name}: Good luck, you're going to need it. Now go! We've all been standing here for too long.")
            player.rebel = 2
            player.run_command()

        else:
            answer_dict[answer](player)
    

    def info2(self, player):
        
        answer = input(f"""\n{self.name}: So, you want to join us? How do we know you weren't sent as a spy from the king? 

1. How may I assist you to earn your trust?
2. Your suspicions serve you well, now prepare to die! (Fight)
3. I need time to think that over. (Goodbye)
""")

        answer_dict = {"1": self.info3, "2": self.fight, "3": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)

    
    def info1(self, player):
        
        self.visited = True
        self.name = "Clement"

        print(f"""\n{self.name}: Who the hell told you that? Who are you? 

1. I'm a traveler interested in your cause. I heard you're against the milirary's expansion into tribal land, and I'm interested in your group.
2. I'm just a traveler who heard your name from the blacksmith, what are you up to?
3. Sorry, I was looking for someone else. (goodbye)""")

        answer_dict = {"1": self.info2, "2": self.neutral, "3": self.end_speech}

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def friendly_greeting(self, player):
        
        answer = input(f"""{self.name}: Hello comrade, what have you come to discuss?

1. How can I assist the revolution?
2. What is the main goal of our rebellion?
3. Nothing. (Goodbye)
""")

        answer_dict = {"1": self.goal, "2": self.lore, "3": self.end_speech}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def neutral_greeting(self, player):

        if player.rebel < 2:
        
            answer = input(f"""{self.name}: What do you want?
        
1. I heard you're against the milirary's expansion into tribal land, and I'm interested in your group.
2. You seem awfully quiet, are you breaking the law? (Fight)
3. Nothing, sorry for interupting. (Goodbye)
""")

            answer_dict = {"1": self.info2, "2": self.fight, "3": self.end_speech}

            while answer not in answer_dict:
                answer = input("Invaid response\n")

            answer_dict[answer](player)

        else:

            print(f"""\n{self.name}: Have you returned with the supplies?

1. Not yet. (Goodbye)""")

            answer_dict = {"1": self.end_speech, }

            if "suppliesCrate" in [x.name for x in player.items]:

                print("2. Yes, I have the supplies. I had to fight the royal general to get them.")
                answer_dict["2"] = self.join

            answer = input("\n")
            while answer not in answer_dict:
                answer = input("Invaid response\n")

            answer_dict[answer](player)


    def negative_greeting(self, player):
        
        answer = input(f"""\n{self.name}: Get out of my sight, you pig!

1. I'll make you eat those words! (Fight)
2. ... (Goodbye)
""")

        answer_dict = {"1": self.fight, "2": player.run_command}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def greeting(self, player):
        
        if player.rebel >= 3:
            self.friendly_greeting(player)

        elif player.rebel < 0 or player.royal >= 2 or player.armor.name == "guardArmor":
            self.negative_greeting(player)

        else:
            self.neutral_greeting(player)

    
    def introduction(self, player):
        
        print(f"""\n{self.name}: What do you want?

1. You seem awfully quiet, are you breaking the law? (Fight)
2. Nothing, sorry for interputing. (Goodbye)""")

        answer_dict = {"1": self.fight, "2": self.end_speech}

        if player.rebel >= 1:
            
            num = len(answer_dict) + 1

            print(f"{num}. Are you Clement?")
            answer_dict[str(num)] = self.info1

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)



class lucifer(RPG.NPC):

    def fight(self, player):

        print(f"{self.name}: You've made a grave mistake.\n")
        player.stage.chars.remove(self)

        enemy = RPG.enemy("Lucifer", 200, 10, 65, 100, 20, 5, 3, 100)
        player.start_encounter([enemy])

        print("""\n\nAs you deliver the final blow, you see the confidence in Lucifer's eyes turn to pure panic. You, a single human, has slain the prince of darkness and removed suffering from the world.
You have performed a great service to the world, a great service to humanity. As such, you feel all sensation stop and a feeling of great bliss come over you. The lord has freed you 
from this world to live out an entirnity of peace. You have died, but lived enternally. 

HOLY ENDING: Kill the devil. Ending 1/5""")

        sys.exit()


    def ending(self, player):

        print(f"""\n{self.name}: You have truly helped me bring suffering to this world. I hereby grant you your reward, your eternal reward.
        

Lucifer grabs you by the neck and lifts you off of the ground. Before you can get a word in, you get torn to shreds and thrown into the lake of fire. You live out an enternity of pain as
recompense for all the pain you've brought the rest of the world.

UNHOLY ENDING: Complete all of satan's quests. Ending 2/5""")

        sys.exit()


    def quest3(self, player):

        print(f"""\n{self.name}: You've served me well, and I such I have one final mission for you. Kill every single person alive in Manhet. Slaughter everyone you can find. Kill the King, kill the rebels,
kill the merchants, kill them all. I have a special reward for you if you can manage this.

1. Yes, my lord.""")

        answer_dict = {"1": self.end_speech}

        if player.kills >= 7:   

            print(f"2. It is done, I have wiped out Manhet's inhabitants.")
            answer_dict["2"] = self.ending

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)
    

    def success2(self, player):

        print(f"""\n{self.name}: Excellent work. For all you've done, I grant you some knowledge of my domain.\n""")

        player.unholy = 4
        player.gain_xp((player.xp_dict[player.level] - player.xp) + 5)

        print("\nYou stand within hell, what do you want to do?\n")
        player.run_command()


    def quest2(self, player):

        print(f"""\n{self.name}: The church within the city of Manhet hold the sword of a warrior who, long ago, slaughtered many of my slaves. Either destroy the sword and bring it to me, and kill that damned
bishop. 

1. Yes, my lord.""")

        answer_dict = {"1": self.end_speech, "2": self.fight}

        if "brokenSword" in [x.name for x in player.items]:

            print(f"2. I have shattered the holy sword and killed the bishop.")
            answer_dict["2"] = self.success2

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)

    
    def success1(self, player):

        print(f"""\n{self.name}: So he is. As a reward, take some coin.

1. Thank you, my lord.
2. How else may I serve you?""")

        answer_dict = {"1": self.end_speech, "2": self.goal}

        player.gold += 25
        player.unholy = 2

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def quest1(self, player):

        print(f"""\n{self.name}: I recently learned that an old fool who tricked me twice lives in the forest far north of here. Go bash his skull in for me.

1. Yes, my lord.""")

        answer_dict = {"1": self.end_speech, "2": self.fight}

        if player.unholy == 1:

            print(f"2. It is done, the old man is dead.")
            answer_dict["2"] = self.success1

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def goal(self, player):

        if player.unholy <= 1:
            self.quest1(player)

        elif player.unholy <= 3:
            self.quest2(player)

        else:
            self.quest3(player)


    def reforge(self, player):
        
        print(f"""{self.name}: For a cost equal to that of the weapon or spell, I can improve its effectiveness but double its mana cost. What would you like improved?
        
(Improving magic weapons and spells will double their damage/healing but also double their mana cost. This will also increase the item's value by 50% of its current price. Enter the 
item's name to improve it, enter 'goodbye' to end conversation with this NPC, or enter 'items' to see your items.)\n""")

        while True:

            answer = input().strip()

            if answer.lower() == "items":

                print("\n")
                for item in player.items:

                    if isinstance(item, RPG.weapon) or isinstance(item, RPG.magic_weapon):
                        print(f"{item.name}, {item.value}g, {item.damage} damage - {item.desc}")

                    elif isinstance(item, RPG.armor):
                        print(f"{item.name}, {item.value}g, {item.defense} defense - {item.desc}")

                    elif isinstance(item, RPG.consumable):
                        print(f"{item.name}, {item.value}g, {item.health} hp, {item.mana} mp - {item.desc}")

                    else:
                        print(f"{item.name}, {item.value}g - {item.desc}")

                print("\n")

            elif answer.lower() == "goodbye":
                self.end_speech(player)

            elif answer in [x.name for x in player.items]:

                item = [x for x in player.items if x.name == answer][0]

                if isinstance(item, RPG.magic_weapon) and player.gold >= item.value:
            
                    player.gold -= item.value
                    self.gold += item.value

                    item.damage *= 2
                    item.cost *= 2

                    item.value = math.floor(item.value * 1.5)

                    print(f"{self.name} has {self.gold}g, you have {player.gold}g\n")

                elif isinstance(item, RPG.heal_spell) and player.gold >= item.value:
                    

                    player.gold -= item.value
                    self.gold += item.value

                    item.heal *= 2
                    item.cost *= 2

                    item.value = math.floor(item.value * 1.5)

                    print(f"{self.name} has {self.gold}g, you have {player.gold}g\n")

                elif not isinstance(item, RPG.magic_weapon) and not isinstance(item, RPG.heal_spell):
                    print("Invalid entry")

                else:
                    print("Not enough gold!\n")


    def reward2(self, player):

        player.gold -= 100 
        player.items.append(RPG.item("holyText", "The ancient holy texts. The church has been seeking these for centuries.", 0))

        player.max_hp //= 2
        player.current_hp = 1

        if player.max_hp <= 0:
            player.player_death()

        print(f"\n{self.name}: As you wish.")

        print("""You feel yourself grow weaker and weaker, to the point that you fall to the ground. You are, however, given the ancient holy texts, perfectly preserved. You lay in fornt of the devil 
himself having just paid a great price. What do you want to do?\n""")

        player.run_command()


    def reward1(self, player):

        self.visited = True

        answer = input(f"""\n{self.name}: You're a sorcerer? Well, as I appriciate the dark art of magic, unlike most, I offer to improve your magical items for a price. 

1. I don't have anything I need improved at the moment.
2. I'd like to have some items improved
""")

        answer_dict = {"1": self.end_speech, "2": self.reforge}

        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def info2(self, player):

        print(f"""\n{self.name}: Those old stone tablets? You may have them, but for a great cost. I require 100 gold coins and part of your soul.

1. That's a price too steep at the moment, goodbye.
2. I'll loot them off of your corpse!""")

        answer_dict = {"1": self.end_speech, "2": self.fight}

        if player.gold >= 100:

            print(f"3. Deal.")
            answer_dict["3"] = self.reward2

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def info1(self, player):

        print(f"""\n{self.name}: How ignorant are you? I am Lucifer, the devil himself.

1. Goodbye
2. Prepare to die!""")

        answer_dict = {"1": self.end_speech, "2": self.fight, }

        if player.holy >= 2:

            print(f"3. I've been sent to recover the holy texts from you.")
            answer_dict["3"] = self.info2

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)


    def greeting(self, player):

        print(f"""\n{self.name}: Greetings mortal. What do you desire?

1. To end this conversation.
2. Who are you?
3. To turn you into dust!
4. I have a magic item I need improved.
5. How may I serve you?""")

        answer_dict = {"1": self.end_speech, "2": self.info1, "3": self.fight, "4": self.reforge, "5": self.goal}

        if player.holy == 2:

            print(f"6. To recover the ancient holy texts.")
            answer_dict["6"] = self.info2

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)

    
    def introduction(self, player):
        
        print(f"""\n{self.name}: Greetings mortal. What do you desire?

1. To end this conversation.
2. Who are you?
3. To turn you into dust!
4. To discover the secrets of magic.
5. How may I serve you?""")

        answer_dict = {"1": self.end_speech, "2": self.info1, "3": self.fight, "4": self.reward1, "5": self.goal}

        if player.holy == 2:
            num = len(answer_dict) + 1

            print(f"{num}. To recover the ancient holy texts.")
            answer_dict[str(num)] = self.info2

        answer = input("\n")
        while answer not in answer_dict:
            answer = input("Invaid response\n")

        answer_dict[answer](player)

