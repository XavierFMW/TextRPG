import system as RPG
from random import randint
import sys
import characters


# Stage Setups

class fieldStage1(RPG.stage):
    """
    The starting stage of the game. Connected to the mines, the forest, the river, and the road to the village.
    """
    
    def active_stage(self, player):

        print("""You're in an open field. To your north is a dense forest, to your west is a mountain with a visible opening, to your south runs a deep river, and to your east is
a rough stone road leading beyond a hill. What do you want to do?\n""")

        player.run_command()



class forestStage1(RPG.stage):
    """
    A basic introduction to combat, filled with 3 basic enemies. Connected to the field stage.
    """

    def intro(self, player):

        print("As you enter the forest, you find yourself ambushed by 3 grey wolves. Your only escape to the field south of you is blocked in the ambush. What do you want to do?\n ")

        enemy1 = RPG.enemy("wolf1", randint(2, 6), 1, randint(4, 8), 0, 5, 2, 0, 10)
        enemy2 = RPG.enemy("wolf2", randint(2, 6), 1, randint(4, 8), 0, 5, 2, 0, 10)
        enemy3 = RPG.enemy("wolf3", randint(2, 6), 1, randint(4, 8), 0, 5, 2, 0, 10)

        self.visited = True

        player.start_encounter([enemy1, enemy2, enemy3])

        print("Winning the battle, you stand alone in the forest with only the paths south and east unblocked by trees. To the east is a dark and covered section of the forest. What do you want to do?\n")
        player.run_command()


    def repeat(self, player):

        print("You find an empty spot in the dense forest. To your south is a field, to the east is an even darker section of forest. All other directions are blocked by trees. What do you want to do?\n")
        player.run_command()


    def active_stage(self, player):

        if not self.visited:
            self.intro(player)

        else:
            self.repeat(player)



class forestStage2(RPG.stage):
    """
    A harder version of the previous forest stage, grants magic items.
    """

    def intro(self, player):

        self.visited = True
        print("As you enter the darkened section of forest, you meet a large brown bear. Noticing you just behind it, the bear prepares to charge. What do you want to do?\n ")

        enemy1 = RPG.enemy("bear", randint(9, 20), 2, randint(17, 20), 0, 10, 2, 1, 40)
        player.start_encounter([enemy1])

        print("After defeating the bear you notice the remains of its meal, a spellcaster. The man is covered in a navy blue cloak of silk and clutches a book within his hands.\n")

        armor1 = RPG.armor("magicRobe", "A vibrant navy blue cloak made of silk. Grants extra widom while equipped.", 25, 1, 1)
        spell1 = RPG.heal_spell("healingSpell", "A tome granting a small amount of healing, at a cost", 15, 5, 5)

        player.give_item([armor1, spell1], """You loot the cloak and book off of the mutilated body. To the west is a path leading out of the forest, to the north is an even darker patch of forest, through which comes the flickering 
of blueish light. What do you want to do?\n""")

        player.run_command()


    def repeat(self, player):

        print("""You stand in the dark spot of the forest, finding only the corpses of a bear and a man. To the north is an even darker area of forest, to the west is a path leading out of the forest What 
do you want to do?\n""")

        player.run_command()


    def active_stage(self, player):

        if not self.visited:
            self.intro(player)

        else:
            self.repeat(player)



class forestStage3(RPG.stage):
    """
    The final stage with encounters in the forest. Contains the item necessary for joining the king, leads to the potion seller.
    """
    
    def intro(self, player):

        self.visited = True
        print("""You enter the thickest part of the forest. The tree cover is so thick that almost all light is blocked. In the middle of the forest stands a tall, withering figure surrounded by bright blue flames
and the bodies of royal soldiers. The figure turns toward you, ready to fight. What do you want to do?\n""")

        enemy1 = RPG.enemy("lich", randint(15, 30), 3, 35, 35, 15, 3, 1, 45)
        player.start_encounter([enemy1])

        print("""You stand alone in the thick forest and remove the dog tags from the soldiers' bodies. From the lich's body you take a silver staff topped with a sapphire. To the south is the way out 
of the forest, but from the west comes natural light. What do you want to do?\n""")

        item1 = RPG.item("dogTags", "The dog tags of two deceased royal soldiers.", 0)
        item2 = RPG.magic_weapon("silverStaff", "A silver staff topped with a shining sapphire. Magical energy surges through it.", 20, 8, 7, 3)

        player.give_item([item1, item2])

        player.run_command()


    def repeat(self, player):

        print("""You stand in the almost pitch black forest, finding the rotting corpses of soldiers. To the south is the path leading out of the forest, to the west is a clearing. What do you want 
to do?\n""")

        player.run_command()


    def active_stage(self, player):

        if not self.visited:
            self.intro(player)

        else:
            self.repeat(player)



class forestStage4(RPG.stage):
    """
    The potion seller's cabin. Used to progress either non-religious ending.
    """

    def intro(self, player):

        self.visted = True

        print("""You find a clearing, the open light being a sharp contrast to the almost pitch black darkness you just arrived from. Within the clearing stands a large log cabin. As you enter the
cabin you're greeted by a tall, rigid, graying old man. He seems friendly. What do you want to do?\n""")
        player.run_command()


    def repeat(self, player):

        print(f"You enter the {self.chars[0].name}'s log cabin. To your east is the dark patch of forest. What do you want to do?\n")
        player.run_command()

    
    def empty(self, player):

        print("You enter the old log cabin. What do you want to do?\n")
        player.run_command()


    def royal(self, player):

        leader = [x for x in self.chars if x.name == "hiddenFigure" or x.name == "Clement"][0]
        print("You meet the rebels in the potion seller's cabin. The second they see you, they prepare for combat. What do you want to do?\n")

        leader.fight(player)


    def active_stage(self, player):

        if player.rebel == -5 and "hiddenFigure" in [x.name for x in self.chars] or "Clement" in [x.name for x in self.chars]:
            self.royal(player)

        elif not self.visited:
            self.intro(player)

        elif not self.chars:
            self.empty(player)

        else:
            self.repeat(player)



class riverStage1(RPG.stage):
    """
    Contains the first magic weapon of the game. Connected to the field stage.
    """

    def intro(self, player):

        old_hp = player.current_hp
        player.change_hp(-5)
        player.items.append(RPG.magic_weapon("oakWand", "A sloppily carved wooden wand, made from basic oak", 15, 4, 5, 2))

        print(f"""You find a river running out of a cave to the east. Wthin the river you see a floating piece of wood. You swim over and grab it, but get dragged across the rocks on your way to shore, 
causing you to take {abs(player.current_hp - old_hp)} damage. ({player.current_hp}/{player.max_hp}) The piece of wood is a basic wand made of oak. You are now alone, partially injuired. What do you want to do?\n""")

        self.visited = True
        player.run_command()


    def repeat(self, player):

        print("As your approach the river, remembering how you previously injuired yourself, you stay several feet away from the bank. You are alone. What do you want to do?\n")
        player.run_command()


    def active_stage(self, player):

        if not self.visited:
            self.intro(player)

        else:
            self.repeat(player)



class villageStage1(RPG.stage):
    """
    The main location of the game. Acts both as a place to resupply and a place to progress the story. Connects shops, the church, and the castle together. Connected to the field stage.
    """

    def intro(self, player):

        print("""As you walk along the stony road up the hill, you find a moderately sized city surrounded by a large stone wall. Within the village square are 2 market stands, one for a general store and 
one for a blacksmith. To the south is a road heading further into the village, all the way down to a stone castle. What would you like to do?\n""")
        player.run_command()


    def repeat(self, player):

        print("You enter the village center, finding the merchant and blacksmith within their respective market stands. To the south is a road heading to a castle. What do you want to do?\n")
        player.run_command()


    def empty(self, player):

        print("You enter the deserted town square, filled with empty market stands. To the south is a road going further into the village, to the west is an open field. What do you want to do?\n")
        player.run_command()


    def criminal(self, player):

        if self.chars:

            self.chars = []
            player.kills += 1

        print("guard: Stop! Kill this criminal!\n")
                
        enemies = [RPG.enemy(f"guard{x}", 0, 2, randint(15, 20), 0, 10, 3, 1, randint(20, 35)) for x in range(1, abs(player.royal) + 1)]
        player.start_encounter(enemies)

        player.royal = 0
        player.run_command()


    def active_stage(self, player):

        if self.chars:

            if player.royal < 0:
                self.criminal(player)

            elif not self.visited:
                self.intro(player)

            else:
                self.repeat(player)

        else:
            self.empty(player)



class villageStage2(RPG.stage):
    """
    The road heading south to the church, saloon, and keep.
    """

    def intro(self, player):
        
        print("""You walk down the southern road. Smaller dirt paths lead off the main road into sprawling neighborhoods filled with homes. To your west is a bar filled with patrons. To your east 
is a large cathedral, and to your south is the large stone keep surrounded by guards and a tall stone wall. In the middle of the road is a soldier yelling and swinging a bell. What would 
you like to do?\n""")

        player.run_command()


    def repeat(self, player):
        
        print("You walk down the road and find a soldier looking for military recruits in the center of town. To your west is the bar, to your east is the cathedral, and to your south is the keep. What do you want to do?\n")
        player.run_command()


    def rebel(self, player):

        self.chars = []
        print("""\nguard: Halt! The royal general has been murdered, and as such we must search for any suspicious activity. What are all of you doing around and about?
            
Clement: We have slaughtered the General! Long live the revolution!

guard: You're under arrest from crimes against the king! You shall be put to death!

The group of guards guards prepare for a fight, what do you want to do?
""")
        enemy1 = RPG.enemy("guard1", 0, 2, randint(15, 20), 0, 8, 3, 1, 10)
        enemy2 = RPG.enemy("guard2", 0, 2, randint(15, 20), 0, 8, 3, 1, 10)
        enemy3 = RPG.enemy("guard3", 0, 2, randint(15, 20), 0, 8, 3, 1, 10)
                
        enemies = [enemy1, enemy2, enemy3]
        player.start_encounter(enemies)

        player.royal = 0
        player.rebel = 6

        print("Your comrades continue south to the castle, what do you want to do?\n")
        player.run_command()


    def criminal(self, player):
        
        if self.chars:

            self.chars = []
            player.kills += 1

        print("guard: There's a criminal here! Arrest them!\n")
                
        enemies = [RPG.enemy(f"guard{x}", 0, 2, randint(15, 20), 0, 10, 3, 1, randint(20, 35)) for x in range(1, abs(player.royal) + 1)]
        player.start_encounter(enemies)

        player.royal = 0
        player.run_command()


    def empty(self, player):
        
        print("""You walk down the quiet road to find only the drying bloodstains of royal guards. To the west is the bar, to the east is the cathedral, and to the south is the gate to the King's castle.
What do you want to do?\n""")
        player.run_command()


    def active_stage(self, player):

        if player.rebel == 5:
            self.rebel(player)

        elif self.chars:

            if player.royal < 0:
                self.criminal(player)

            elif not self.visited:
                self.intro(player)

            else:
                self.repeat(player)

        else:
            self.empty(player)



class villageStage3(RPG.stage):
    """
    The bar. Used to advance the revolutionary ending.
    """


    def royal(self, player):

        print("As you enter the bar, you notice a small group of people shuffle past you out of the bar. What do you want to do?")

        self.flee()
        player.run_command()


    def empty(self, player):
        
        print("You walk into the deserted bar. What do you want to do?\n")
        player.run_command()


    def intro(self, player):

        print("""You enter the bar to find it full of food, drink, and noise. The tavern is filled and busy. One table stands out to you, shrouded in hushed voices and headed by a suspicious figure. Behind 
the counter stands 2 barkeepers, one of whom is fully surrounded by customers. What do you want to do?\n""")
        player.run_command()


    def repeat(self, player):

        print("You walk into the tavern, filled to capacity as per usual. What do you want to do?\n")
        player.run_command()


    def flee(self):

        leader = [x for x in self.chars if x.name == "hiddenFigure" or x.name == "Clement"][0]

        self.chars.remove(leader)
        self.indirects[0].chars.append(leader)


    def active_stage(self, player):

        if self.chars:

            if player.armor.name == "guardArmor" and len(self.chars) == 2: 
                self.royal(player)

            elif not self.visited:
                self.intro(player)

            else:
                self.repeat(player)

        else:
            self.empty(player)



class villageStage4(RPG.stage):
    """
The cathedral. Used to advance the holy ending.
    """


    def intro(self, player):
        
        print("""You enter the massive cathedral, struck by its beauty. Colorful portraits and landscapes line the walls, displaying the history of the church up to this point. Within the center of the large 
cathedral, between a set of pews, sits a large rock. Within the rock stands a sword, stabbed downward into it. On the rock is carved the phrase "here stands the blade of a great crusader, 
King, and preist." At the front of the cathedral stands a bishop, watching you read the inscription. What do you want to do?\n""")

        player.run_command()


    def repeat(self, player):
        
        print("You walk into the cathedral and find the bishop standing at the front of the room. What do you want to do?\n")
        player.run_command()


    def empty(self, player):
        
        print("You enter the cold and empty cathedral to find only a boulder and a shattered blade inside. What do you want to do?\n")
        player.run_command()


    def active_stage(self, player):

        if not self.visited:
            self.intro(player)

        elif self.chars:
            self.empty(player)

        else:
            self.repeat(player)



class castleStage1(RPG.stage):
    """
    The castle walls. The enterance to the keep and barracks.
    """


    def intro(self, player):
        
        print("""You walk up to walls guarding a large stone keep, the home of the King and the seat of military power in Manhet. You walk towards the large portcullis guarding the walls. What do you want to do?\n""")
        player.run_command()


    def repeat(self, player):
        
        print("You walk up to the walls' portcullis. To the south is the inside of the castle walls. To the north is a road into the center of the village. What do you want to do?\n")
        player.run_command()


    def rebel(self, player):
        
        self.chars = []
        print("""\nguard: You've all commit crimes against the king! You must pay wih your blood!
    
The group of guards prepare for a fight, what do you want to do?
""")
        enemy1 = RPG.enemy("guard1", 0, 2, randint(15, 20), 0, 8, 3, 1, 10)
        enemy2 = RPG.enemy("guard2", 0, 2, randint(15, 20), 0, 8, 3, 1, 10)
        enemy3 = RPG.enemy("guard3", 0, 2, randint(15, 20), 0, 8, 3, 1, 10)
        enemy4 = RPG.enemy("guard4", 0, 2, randint(15, 20), 0, 8, 3, 1, 10)
                
        enemies = [enemy1, enemy2, enemy3, enemy4]
        player.start_encounter(enemies)

        player.royal = 0
        player.rebel = 7

        print("Your comrades continue south inside of the castle walls, what do you want to do?\n")
        player.run_command()


    def empty(self, player):
        
        print("You walk up to the abondoned castle gate, the bodies of the guards lie against the bloodstained stone wall. To the south is the road to the barracks and keep. What do you want to do?\n")
        player.run_command()


    def criminal(self, player):
        
        if self.chars:

            self.chars = []
            player.kills += 1

        print("guard: Criminal on the loose!\n")
                
        enemies = [RPG.enemy(f"guard{x}", 0, 2, randint(15, 20), 0, 10, 3, 1, randint(20, 35)) for x in range(1, abs(player.royal) + 1)]
        player.start_encounter(enemies)

        player.stage.south = castleStage2(player.stage, None, "Blocked", castleStage3(None, None, None, "Blocked", [characters.recruiter2("recruiter", 0, 1, 0, [])]) , [])

        player.royal = 0
        player.run_command()


    def active_stage(self, player):

        if player.rebel == 6:
            self.rebel(player)

        elif self.chars:
        
            if player.royal < 0:
                self.criminal(player)

            elif not self.visited:
                self.intro(player)

            else:
                self.repeat(player)

        else:
            self.empty(player)



class castleStage2(RPG.stage):
    """
    The area inside the wall. Leads to the barracks and keep
    """


    def intro(self, player):
        
        print("""You enter the area behind the large stone wall, finding it packed with guards. The cobblestone road leads east to a stone fortress, the barracks and armory for the King's personal gaurd. To the
south stands a large stone keep visible from all over the city. What do you want to do?\n""")
            
        player.run_command()
    

    def repeat(self, player):
        
        print("You stand within the castle's courtyard. To the south is the King's keep, to the east is the soldier's barracks, and to the north is the castle gate. What do you want to do?\n")
        player.run_command()
    

    def criminal(self, player):
        
        print("soldier: Soldiers, kill this criminal!\n")

        enemy1 = RPG.enemy("soldier1", 0, 3, 15, 0, 10, 2, 2, 20, [])
        enemy2 = RPG.enemy("soldier2", 0, 3, 15, 0, 10, 2, 2, 20, [])
        enemy3 = RPG.enemy("soldier3", 0, 3, 15, 0, 10, 2, 2, 20, [])
        
        player.start_encounter([enemy1, enemy2, enemy3])

        print("You stand above the soldier bodies within the courtyard of the castle. To the north is the castle gate, and to the east is the barracks. What do you want to do?\n")
        player.run_command()
    

    def rebel(self, player):
        
        self.chars = []
        print("""\nsoldier: Stop! Treason!
    
The soldiers charge at you, what do you want to do?
""")
        enemy1 = RPG.enemy("soldier1", 0, 3, 15, 0, 10, 2, 2, 20)
        enemy2 = RPG.enemy("soldier2", 0, 3, 15, 0, 10, 2, 2, 20)
        enemy3 = RPG.enemy("soldier3", 0, 3, 15, 0, 10, 2, 2, 20)
                
        enemies = [enemy1, enemy2, enemy3]
        player.start_encounter(enemies)

        player.royal = 0
        player.rebel = 8

        king1 = characters.king("theKing", 0, 10, 0, [])
        self.south = castleStage5(self, None, None, None, [king1])

        print("Your comrades continue south inside of the keep itself, what do you want to do?\n")
        player.run_command()
    

    def unholy(self, player):
        
        king1 = characters.king("theKing", 0, 10, 0, [])
        self.south = castleStage5(self, None, None, None, [king1])

        print("You watch as the gates leading south into the King's palace are shot open by an unknown force. To the east is the barracks, to the north is the castle's gate. What do you want to do?\n")
        player.run_command()
    

    def active_stage(self, player):

        if player.rebel == 7:
            self.rebel(player)

        elif player.unholy >= 4:
            self.unholy(player)

        elif player.royal < 0:
            self.criminal(player)

        elif not self.visited:
            self.intro(player)

        else:
            self.repeat(player)



class castleStage3(RPG.stage):
    """
    The city barracks. Use to either join the army or steal the armory's key. 
    """


    def intro(self, player):
        
        print("""You enter the city barracks and are greeted by an army recruiter. Within the barracks stands the Royal General, the King's second in command. On the general's hip sits a large silver key. 
The barracks itself is a cobblestone struture filled with beds, crates of food, soldiers, and recruits. To the east of the main chamber is a large, locked steel door. What do you want to do?\n""")

        player.run_command()
    

    def repeat(self, player):
        
        print("You enter the barracks and meet the recruiter and the general. What do you want to do?\n")
        player.run_command()
        

    def empty(self, player):
        
        print("""You enter the barracks and stand above the bodies of the army recruiter and the royal general. To the east is the royal armory, to the west is the castle courtyard. What do you
want to do?\n""")

        player.run_command()
    

    def active_stage(self, player):

        if self.chars:

            if not self.visited:
                self.intro(player)

            else:
                self.repeat(player)

        else:
            self.empty(player)



class castleStage4(RPG.stage):
    """
    The city armory within the barracks. Used to progress the rebel ending.
    """


    def intro(self, player):
        
        print("""You use your key to enter the armory. You find swords, bows, food, medicine, and other supplies. You promptly take hold of a large crate containing a wide variety of the supplies. What do
you want to do?\n""")

        item1 = RPG.item("suppliesCrate", "A crate filled with military supplies.", 35)
        player.give_item(item1)

        player.run_command()


    def repeat(self, player):
        
        print("You enter the looted and empty armory. What do you want to do? What do you want to do?\n")
        player.run_command()


    def active_stage(self, player):

        if not self.visited:
            self.intro(player)

        else:
            self.repeat(player)



class castleStage5(RPG.stage):
    """
    The King's throneroom. 
    """


    def repeat(self, player):
        
        print("""\nYou and your comrades enter the King's palace. It's filled with golden furniture and many decorations. On the throne sits the king himself.
                
Clement: We've come to end your rule! The revolution shall bring freedom!\n""")

        self.chars[0].fight(player)
    

    def repeat(self, player):
        
        print("You enter the King's gilded chamber and look upon the scarred old man. What do you want to do?\n")
        player.run_command()
    

    def intro(self, player):
        
        print(f"""You enter the King's palance and are led to the throneroom. The halls are filled with fine art, trophies, and flags. The flag of Talia is royal purple and sage green with a jet black 
eagle in the center. You enter the throneroom, filled with golden furniture, and meet the King himself. In a gilded chair, covered in his armor, sits the King himself. A battle-hardened 
warrior, the King sits scarred and graying, watching the guards bring him a peasant by the name of {player.name}. What do you want to do?\n""")

        player.run_command()
    

    def empty(self, player):
        
        print("You enter the empty palace to find the King's corpse. What do you want to do?\n")
        player.run_command()
    

    def active_stage(self, player):

        if self.chars:

            if player.rebel == 8:
                self.rebel(player)

            elif not self.visited:
                self.intro(player)

            else:
                self.repeat(player)

        else:
            self.empty(player)



class caveStage1(RPG.stage):
    """
    The first area of the game filled with basic supplies. Connected to the field stage and the second cave stage.
    """

    def intro(self, player):

        print("""As you enter the small cave you are greeted by human remains withered to the bone. The skeleton is surrounded by a pickaxe, a rusty iron sword, a stange bottle of liquid, and a firepit 
filled with ash. To the southern side of the cave there appears to be a wooden staircase.\n""")

        player.give_item([RPG.weapon("rustySword", "An old, dull iron sword", 5, 3, 2), RPG.consumable("strangeBrew", 15, 15, -5)], "You grab the sword and the bottle of liquid. What do you want to do?\n")
        self.visited
        player.run_command()


    def repeat(self, player):
        
        print("Within the small cave you find only the old, unmoving skeleton and an ash filled firepit. To the south is a set of old wooden stairs. What do you want to do?\n")
        player.run_command()


    def active_stage(self, player):

        if not self.visited:
            self.intro(player)

        else:
            self.repeat(player)



class caveStage2(RPG.stage):
    """
    Grants harder combatatants compared to previous stages, sends the player down the path to Hell.
    """


    def intro(self, player):
        
        print("""You find your way into an abandoned mineshaft. As soon as you cross the threshold into the mine you find 2 skeletons wielding pickaxes. The corpses stand and prepare for battle. What do 
you want to do?\n""")

        enemy1 = RPG.enemy("skeleton1", randint(9, 20), 2, randint(14, 18), 0, 8, 3, 1, 30)
        enemy2 = RPG.enemy("skeleton2", randint(9, 20), 2, randint(14, 18), 0, 8, 3, 1, 30)
        player.start_encounter([enemy1, enemy2])

        print("""You stand alone in the old mineshaft. To the east is an opening, through which comes the sound of running water. To the west is a set of stone steps descending further into the Earth, the
sound of grinding and growling echoing back up to you. To the north is a set of old wooden stairs leading to sunlight. What do you want to do?\n""")
        player.run_command()


    def repeat(self, player):
        
        print("""In the old mine you find 2 old, unmoving skeletons. There is a set of wooden steps leading upward on the northern side of the mine, to the east is the sound of running water, and to the west 
is a set of stone steps leading to echoing growls. What do you want to do?\n""")

        player.run_command()


    def active_stage(self, player):

        if not self.visited:
            self.intro(player)

        else:
            self.repeat(player)



class caveStage3(RPG.stage):
    """
    Serves as a harder combat stage and a resupply area. Will lead to harder levels in the future.
    """


    def intro(self, player):
        
        print("""Walking down the firm stone steps, you hear the growling grown nearer. You feel a slight heat come over you as you get deeper into the Earth. After walking the decsending steps for waht feels
like forever, you reach a closed off stone chamber. The room smells of rot and the floor is covered in bodies. In the middle of the room stands a large, wailing, rotting corpse. Held together
by loose skin and tough armor, the creature growls at you as it prepares its charge. What do you want to do?\n""")

        enemy1 = RPG.enemy("warrior", randint(10, 30), 3, 35, 0, 14, 3, 2, 55)
        weapon1 = RPG.weapon("battleaxe", "A double-ended battleaxe made of steel.", 30, 7, 3)
        player.start_encounter([enemy1])

        player.give_item(weapon1, "From the body of the now truly dead warrior you grab a battleaxe made of steel.\n")

        print("Now alone in the chamber, a set of stairs to the west lead even further into the Earth. From the passage comes the sound of distant screaming. What do you want to do?\n")
        player.run_command()


    def repeat(self, player):
        
        print("""You enter the chamber filled with the smells of rot and death, finding only the bodies of the undead warrior and its victims. To the east is a set of stone steps heading upward. To the west 
is a set of stairs leading even deeper underground. What do you want to do?\n""")

        player.run_command()


    def active_stage(self, player):

        if not self.visited:
            self.intro(player)

        else:
            self.repeat(player)



class hellStage1(RPG.stage):
    """
    Serves as the first "hell" stage. The player faces off against an even more difficult enemy.
    """


    def intro(self, player):
        
        print("""As you walk down the steps, you notice small piles of bone and ash along the floor. The further down you walk, the more intense the heat and smell of sulfur becomes. You enter a chamber
with blackened and dirtied brick walls. The floor is covered in ash and blood as you look upon a beast in the center of the room. A blood-covered monster standing 7 feet tall stares at
you with amber eyes. The horns of a goat twist their was off of the creatures head. You've encountered a demon, hungry for their next meal. What do you want to do?\n""")

        enemy1 = RPG.enemy("demon", randint(20, 35), 4, 40, 0, 15, 3, 3, 65)
        item1 = RPG.item("demonHorn", "The horn of a demon. Used as proof a warrior has slain a demon.", 10)
        player.start_encounter([enemy1])

        player.give_item(item1, "As a token of your success against the creature, you cut the demon's horn off as a trophy.\n")

        print("""As you stand above the beast's body, you realize the room has yet another passage downward, to the south. The passage, marked by a skull, is the source of the endless screaming and 
smell of sulfur. What do you want to do?""")
        player.run_command()


    def repeat(self, player):
        
        print("""You walk into the hot, dirty room and sulfur fills your nose. You stand above the slaughtered demon and piles of ash. To the east is the path upward, so the south is the passage downward. 
What do you want to do?\n""")

        player.run_command()


    def active_stage(self, player):

        if not self.visited:
            self.intro(player)

        else:
            self.repeat(player)



class hellStage2(RPG.stage):
    """
    Serves as an extremely hard encounter, as well as the gate to hell.
    """


    def intro(self, player):
        
        print("""You walk down the set of steps, finding the once ash covered floor to be smeared with blood. As you descend further, the smell of sulfur grows almost unbreable, the ambient heat is 
almost burning you, and the endless screams are defeaning. As you reach a large stone room, the walls flowing with blood, you're greeted by 2 more demons. The second they see you,
you can sense the excitement in their eyes as they prepare to fight. They stand in front of a large steel door. What do you want to do?""")

        enemy1 = RPG.enemy("demon1", randint(20, 35), 4, randint(30, 40), 0, 14, 3, 3, 65)
        enemy2 = RPG.enemy("demon2", randint(20, 35), 4, randint(30, 40), 0, 14, 3, 3, 65)

        item1 = RPG.item("demonHorn", "The horn of a demon. Used as proof a warrior has slain a demon.", 10)
        player.start_encounter([enemy1, enemy2])

        player.give_item([item1, item1], "You remove the horns of each demon you've killed, marking your continued victory.\n")

        print("Having reached the final level, you stand alone in front of a large steel door to your south. The door is marked in blood with the words 'Welcome to Hell.' What do you want to do?\n")
        player.run_command()


    def repeat(self, player):
        
        print("""You enter the bloodied stone room that houses the gates to hell. What do you want to do?\n""")
        player.run_command()


    def active_stage(self, player):

        if not self.visited:
            self.intro(player)

        else:
            self.repeat(player)



class hellStage3(RPG.stage):
    """
    Houses the devil. The basis for either religious ending.
    """


    def intro(self, player):
        
        print("""You walk through the large steel doors to find a monsterous sight. You find a large, open area filled with flowing lava, fires, and screams. You have reached the lowest level, hell itself.
Sitting on a brick throne in front of you is a monster of a man. An even further demented version of the demons you've fought so far, you meet the devil himself. The man is seems 
surprised, but not aggressive. What do you want to do?\n""")

        player.run_command()


    def repeat(self, player):
        
        print("""You enter hell and are greeted by the devil. What do you want to do?\n""")
        player.run_command()


    def active_stage(self, player):

        if not self.visited:
            self.intro(player)

        else:
            self.repeat(player)
