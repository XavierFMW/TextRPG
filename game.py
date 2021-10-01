import system as RPG
from random import randint
import math
import sys
import stages
import characters


# Defining items and NPCs

potion1 = RPG.consumable("healthPotion", 30, 15, 0)
potion2 = RPG.consumable("manaPotion", 25, 0, 15)
armor1 = RPG.armor("leatherArmor", "Basic armor made of woven strips of leather", 20, 1)
merchant1 = characters.shopKeeper("merchant", 250, 1, 0, [armor1, potion1, potion2])

sword1 = RPG.weapon("steelSword", "A run-of-the-mill steel sword", 30, 5, 3)
sword2 = RPG.weapon("gamblersSword", "A steel sword coated in fool's gold with the shape of a spade carved decoratively into the base of its handle.", 150, 10, 10)
armor2 = RPG.armor("ironArmor", "Thick leather garments covered with plates of iron", 45, 2)
armor3 = RPG.armor("steelArmor", "A full set of steel plate armor.", 60, 3)
merchant2 = characters.blacksmith("blacksmith", 175, 1, 0, [sword1, sword2, armor2, armor3])

food1 = RPG.consumable("bread", 5, 1, 0)
food2 = RPG.consumable("sausage", 5, 1, 0)
food3 = RPG.consumable("beer", 5, -1, 0)
merchant3 = characters.barkeep("barkeep", 300, 1, 0, [food1, food2, food3])

army1 = characters.recruiter1("soldier", 0, 1, 0, [])
army2 = characters.guard("guard", 0, 1, 0, [])
clement = characters.rebelLeader("hiddenFigure", 56, 7, 0, [])
bishop = characters.church("bishop", 0, 1, 0, [])

potion3 = RPG.stat_potion("warriorsBrew", 100, "Permanently doubles your health and halves your mana.", 2, -2, False)
potion4 = RPG.stat_potion("magesBrew", 100, "Permanently halves your health and doubles your mana.", 2, -2, False)
merchant4 = characters.potionSeller("oldMan", 50, 3, 0, [potion3, potion4])

satan = characters.lucifer("Lucifer", 200, 10, 100, [])


# Defining and connecting stages

river1 = stages.riverStage1(None, None, None, None, [])

hell3 = stages.hellStage3(None, None, None, None, [satan])
hell2 = stages.hellStage2(None, None, hell3, None, [])
hell1 = stages.hellStage1(None, None, hell2, None, [])
cave3 = stages.caveStage3(None, hell1, None, None, [])
cave2 = stages.caveStage2(None, cave3, None, river1, [])
cave1 = stages.caveStage1(None, None, cave2, None, [])

forest4 = stages.forestStage4(None, None, None, None, [merchant4])    # Potion Seller
forest3 = stages.forestStage3(None, forest4, None, None, [])
forest2 = stages.forestStage2(forest3, None, None, None, [])
forest1 = stages.forestStage1(None, None, None, forest2, [])

castle1 = stages.castleStage1(None, None, "Blocked", None, [army2])     # Castle Gate

village4 = stages.villageStage4(None, None, None, None, [bishop])    # Cathedral
village3 = stages.villageStage3(None, None, None, None, [merchant3, clement], forest4)    # Bar  
village2 = stages.villageStage2(None, village3, castle1, village4, [army1])    # Southern Road
village1 = stages.villageStage1(None, None, village2, None, [merchant1, merchant2])    # Village Center

startingStage = stages.fieldStage1(forest1, cave1, river1, village1, [])


# Beginning the game

player = RPG.player(startingStage)
