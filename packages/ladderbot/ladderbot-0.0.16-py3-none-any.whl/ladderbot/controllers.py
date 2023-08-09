# import os
from time import sleep
from random import choice
from pathlib import Path
import importlib.resources
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from ladderbot.items import Weapon, Armor, Charm
from ladderbot.mappings import transmute_mapping, item_pickup_mapping, deposit_criteria, prices
#-----------------------------------------------
class LoginController:
    def __init__(self, driver, logger) -> None:
        self.name = "LoginController"
        self.logger = logger
        # self.username = username
        # self.password = password
        self.driver = driver
    # def login(self):
    #     self.driver.get('https://forums.d2jsp.org/login.php')
    #     # Enter login credentials and submit the form
    #     username_field = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.NAME, 'username'))
    #     )
    #     # username_field = self.driver.find_element(By.NAME, 'username')
    #     username_field.send_keys(self.username)  # Replace YOUR_USERNAME with your actual username
    #     username_field.send_keys(Keys.RETURN)

    #     # password_field = self.driver.find_element(By.NAME, 'pass')
    #     password_field = WebDriverWait(self.driver, 10).until(
    #         EC.visibility_of_element_located((By.NAME, 'pass'))
    #     )
    #     sleep(.1)
    #     password_field.send_keys(self.password)  # Replace YOUR_PASSWORD with your actual password
    #     sleep(10)
    #     password_field.send_keys(Keys.RETURN)
    #     sleep(2)
    #     return self.driver.current_url == 'https://forums.d2jsp.org/'
    # def logout(self):
    #     self.driver.get("https://forums.d2jsp.org/login.php?c=8")
    #     logout_button = WebDriverWait(self.driver, 5).until(
    #         EC.presence_of_element_located((By.XPATH, '/html/body/form/dl/dd/div[3]/input'))
    #     )
    #     logout_button.click()
    def check_for_element(self, class_name):
        status = False
        try:
            # check if game is started
            # self.driver.find_element(By.CLASS_NAME, class_name)
            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
            status = True
        except:
            # element wasnt found
            pass
        return status
    def check_location(self) -> bool:
        self.logger.info(f"{self.name}.check_location() --> Reading player location")
        indicators = {
            'town' : (By.CLASS_NAME, 'townOIcon'),
            'catacombs' : (By.CLASS_NAME, 'bgCata'),
            'pond' : (By.XPATH, '//*[@id="bg"]/img'),
            'character_selection' : (By.XPATH, '//*[@id="bg"]/div[1]/a'),
            'character_selected' : (By.XPATH, '//*[@id="bg"]/div[2]/div/a[2]'),
            'character_creation' : (By.XPATH, '//*[@id="bg"]/div/div[2]/div[1]'),
        }
        for location in indicators:
            try:
                WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located(indicators.get(location))
                )
                self.logger.info(f"{self.name}.check_location() --> {location=}")
                return location
            except Exception as e:
                pass
        else:
            self.logger.error(f"{self.name}.check_location() --> Location Unknown!")
            return False
    def leave_cata(self):
        self.logger.info(f"{self.name}.leave_cata() --> Leaving Catacombs")
        # Spams exiting the catacombs until we've left
        while self.check_location() == 'catacombs':
            try:
                to_town_button = self.driver.find_element(By.CLASS_NAME, "gradRed")
                to_town_button.click()
            except Exception as e:
                # Failed to leave catacombs, keep trying forever. or die...
                pass
    def start_game(self):
        html_file = Path(str(importlib.resources.files("ladderbot")) + "\\index.html")
        play_url = html_file.as_uri()
        self.logger.info(f"{self.name}.start_game() --> Starting Game {play_url=}")
        self.driver.get(play_url)
        try: 
            play_button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'abutGradBl'))
            )
            play_button.click()
        except TimeoutError as e:
            raise e
        try: 
            stage = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, 'stage'))
            )
            stage.click()
        except TimeoutError as e:
            raise e
    def select_character(self, name:str):
        self.logger.info(f"{self.name}.select_character() --> {name=}")
        character_list = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'charList'))
        )
        available_characters = character_list.find_elements(By.CLASS_NAME, 'cName')
        character = list(filter(lambda x:x.text == name, available_characters))[0]
        character.click()
        character_play_button = self.driver.find_element(By.CLASS_NAME, 'clPlay')
        character_play_button.click()
    def logout_character(self):
        self.logger.info(f"{self.name}.logout_character()")
        button_grouping = self.driver.find_element(By.CLASS_NAME, 'ctrlButtons')
        logout_character_button = button_grouping.find_elements(By.TAG_NAME, 'img')[-1]
        logout_character_button.click()
class Login:
    def __init__(self, controller:LoginController) -> None:
        self.controller = controller
    def run(self, character_name:str):
        # self.controller.login()
        # launch the game
        self.controller.start_game()
        current_location = self.controller.check_location()
        if current_location == 'catacombs':
            self.controller.leave_cata()
            self.controller.logout_character()
            self.controller.select_character(character_name)
        # already at the town
        elif current_location == 'town':
            # logout current character
            self.controller.logout_character()
            self.controller.select_character(character_name)
        # login desired character
        elif current_location == 'character_selection':
            self.controller.select_character(character_name)
#-----------------------------------------------
class InventoryController:
    def __init__(self, driver, logger) -> None:
        self.name = "InventoryController"
        self.driver = driver
        self.logger = logger
        self.action = ActionChains(self.driver)
        self.weapon = None
        self.armor = None
        self.charm = None
        self.acc_charm = None
    def open(self):
        self.action.send_keys(Keys.SPACE).perform()
        self.action.send_keys("i").perform()
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'pbInv'))
            )
        except TimeoutError as e:
            raise e
    def close_all(self):
        self.action.send_keys(Keys.SPACE).perform()
    def get_equipment_count(self):
        self.logger.info(f"{self.name} --> getting inventory capacity")
        self.open()
        equipment_label_element = WebDriverWait(self.driver, 1).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'invEqCountLabel'))
        )
        label_text = equipment_label_element.text
        current, capacity = [int(letter) for letter in label_text.split() if letter.isdigit()]
        self.logger.info(f"{self.name} --> {current=}, {capacity=}")
        self.close_all()
        return current, capacity
    def load_equipped_items(self):
        self.logger.info(f"{self.name} --> reading equipped items from inventory")
        self.open()
        equipped_items_container = WebDriverWait(self.driver, .5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'invEquipped'))
        ) 
        equipped_items = WebDriverWait(equipped_items_container, .5).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'itemSlotBox'))
        )
        weapon, armor, charm, acc_charm = equipped_items
        overlay_stats = weapon.text.replace('+',"").split('\n')
        if len(overlay_stats) == 1:
                    overlay_stats.insert(0, '0')
        self.action.move_to_element(weapon).perform()
        try:
            weapon_stats_popup = WebDriverWait(self.driver, .5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'tbItemDesc'))
            )
            weapon = Weapon(weapon_stats_popup, overlay_stats)
        except TimeoutException:
            self.logger.info(f"{self.name} --> TimeoutException: weapon not equipped")
            weapon = None
        overlay_stats = armor.text.replace('+',"").split('\n')
        if len(overlay_stats) == 1:
                    overlay_stats.insert(0, '0')
        self.action.move_to_element(armor).perform()
        try:
            armor_stats_popup = WebDriverWait(self.driver, .5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'tbItemDesc'))
            )
            armor = Armor(armor_stats_popup, overlay_stats)
        except TimeoutException:
            self.logger.info(f"{self.name} --> TimeoutException: armor not equipped")
            armor = None
        overlay_stats = charm.text.replace('+',"").split('\n')
        if len(overlay_stats) == 1:
                    overlay_stats.insert(0, '0')
        self.action.move_to_element(charm).perform()
        try:
            charm_stats_popup = WebDriverWait(self.driver, 1).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'tbItemDesc'))
            )
            charm = Charm(charm_stats_popup, overlay_stats)
        except TimeoutException:
            self.logger.info(f"{self.name} --> TimeoutException: charm not equipped")
            charm = None
        overlay_stats = acc_charm.text.replace('+',"").split('\n')
        if len(overlay_stats) == 1:
                    overlay_stats.insert(0, '0')
        self.action.move_to_element(acc_charm).perform()
        try:
            charm_stats_popup = WebDriverWait(self.driver, 1).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'tbItemDesc'))
            )
            acc_charm = Charm(charm_stats_popup, overlay_stats)
        except TimeoutException:
            self.logger.info(f"{self.name} --> TimeoutException: acc_charm not equipped")
            acc_charm = None
        return weapon, armor, charm, acc_charm
    def load_equipment(self):
        self.logger.info(f"{self.name} --> reading inventory equipment")
        equipment = {}
        self.action.send_keys(Keys.SPACE).perform()
        self.action.send_keys("i").perform()
        equipment_container = WebDriverWait(self.driver, 1).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'invEqBox'))
        )
        equipment_elements = WebDriverWait(equipment_container, 1).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'itemSlotBox'))
        )
        # Enumerate the equipment slots to see if there is an item,
        #   and if so in which slot
        for index, element in enumerate(equipment_elements):
            self.logger.info(f"{self.name} --> reading inventory item {index} icon tier/bonus overlay")
            try:
                item_element = element.find_element(By.CLASS_NAME, 'itemBox')
            except NoSuchElementException:
                self.logger.info(f"{self.name} --> NoSuchElementException: No equipment in slot {index}")
                equipment[index] = None
                continue
            overlay_stats = item_element.text.replace('+',"").split('\n')
            if len(overlay_stats) == 1:
                overlay_stats.insert(0, '0')
            self.action.move_to_element(item_element).perform()
            item_comparison_grouping = WebDriverWait(self.driver, 1).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'tbItemDesc'))
            )
            item_description_element = item_comparison_grouping.find_elements(By.XPATH, "./child::*")[0]
            item = self.convert_item_from_element(item_description_element, overlay_stats)
            equipment[index] = item
        return equipment
    def classify_item(self, item_name:str) -> str:
        self.logger.info(f"{self.name} --> classifying {item_name=}")
        weapon_types = ["sword","club","axe","dagger","staff","longsword","warhammer","battleaxe","spear","polearm"]
        charm_types = ["ice","fire","lightning","wind","earth","wild Heal","heal","focused heal"]
        armor_types = ["robe","padded Robe","leather armor","scale armor","chain mail","plate mail"]
        for weapon_type in weapon_types:
            if weapon_type in item_name.lower():
                self.logger.info(f"{self.name} --> {item_name=} is weapon")
                return "weapon"
        for armor_type in armor_types:
            if armor_type in item_name.lower():
                self.logger.info(f"{self.name} --> {item_name=} is armor")
                return "armor"
        for charm_type in charm_types:
            if charm_type in item_name.lower():
                self.logger.info(f"{self.name} --> {item_name=} is charm")
                return "charm"         
    def convert_item_from_element(self, item_popup_element, overlay_stats):
        item_name = item_popup_element.text.split("\n")[0]
        self.logger.info(f"{self.name} --> parsing {item_name=} into item object")
        item_classification = self.classify_item(item_name)
        if item_classification == "weapon":
            item = Weapon(item_popup_element, overlay_stats)
            self.logger.info(f"{self.name} --> {item_name=} parsed to weapon item object")
        elif item_classification == "armor":
            item = Armor(item_popup_element, overlay_stats)
            self.logger.info(f"{self.name} --> {item_name=} parsed to armor item object")
        elif item_classification == "charm":
            item = Charm(item_popup_element, overlay_stats)
            self.logger.info(f"{self.name} --> {item_name=} parsed to charm item object")
        else:
            self.logger.error(f"{self.name} --> could not parse {item_name=} to item object")
            item = None
        return item        
    def delete_item(self, item_element):
        inventory_window_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'invIWSide'))
        )
        trash_bin_element = inventory_window_element.find_element(By.XPATH, '//*[@id="stage"]/div[5]/div[4]/div[3]/div')
        self.action.drag_and_drop(item_element, trash_bin_element).perform()
class Inventory:
    def __init__(self, inventory_controller:InventoryController) -> None:
        self.controller = inventory_controller
        self.weapon = None
        self.armor = None
        self.charm = None
        self.acc_charm = None
        self.equipment = None
    def load(self):
        self.weapon, self.armor, self.charm, self.acc_charm = self.controller.load_equipped_items()
        self.equipment = self.controller.load_equipment()
        self.controller.close_all()
    def is_full(self):
        return self.controller.get_equipment_count()[0] >= 9
#-----------------------------------------------
class PlayerController:
    def __init__(self, driver, logger) -> None:
        self.name = "PlayerController"
        self.driver = driver
        self.logger = logger
        self.action = ActionChains(self.driver)
        self.location_map = {
            'marketplace':0,
            'catacombs':1,
            'shrine':2,
            'vault':3,
            'pond':4,
            'cooking':5,
            'transmuting':6,
            'glyphing':7,
            'suffusencing':8
        }
        self.quickbar = {
            'q' : "",
            'e' : "",
            'r' : "",
            '1' : "",
            '2' : "",
            '3' : "",
            '4' : "",
            '5' : ""
        }
    # def clear_screen(self):
    # # Check if the operating system is Windows or Unix-like
    #     if os.name == 'nt':
    #         os.system('cls')  # For Windows
    #     else:
    #         os.system('clear')  # For Unix-like systems
    def check_health(self):
        # health_element = self.driver.find_element(By.CLASS_NAME, 'lifeMeter')
        health_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'lifeMeter'))
        )
        current_health, max_health = health_element.text.replace(' ', '').split('/')
        return {
            'current' : int(current_health),
            'max_health' : int(max_health),
            'percent' : int(100*(int(current_health)/int(max_health)))
        }
    def check_location(self) -> bool:
        indicators = {
            'town' : (By.CLASS_NAME, 'townOIcon'),
            'catacombs' : (By.CLASS_NAME, 'bgCata'),
            'pond' : (By.XPATH, '//*[@id="bg"]/img'),
            'character_creation' : (By.XPATH, '//*[@id="bg"]/div/div[2]/div[1]'),
            'character_selection' : (By.XPATH, '//*[@id="bg"]/div[1]/a'),
            'character_selected' : (By.XPATH, '//*[@id="bg"]/div[2]/div/a[2]'),
        }
        for location in indicators:
            try:
                self.driver.find_element(*(indicators.get(location)))
                return location
            except Exception as e:
                # If an exception occured check the next location indicator
                pass
        else:
            # print(f'could not determine location')
            return False
    def check_mana(self):
        mana_element = self.driver.find_element(By.CLASS_NAME, 'manaMeter')
        current_mana, max_mana = mana_element.text.replace(' ', '').split('/')
        return {
            'current' : int(current_mana),
            'max_mana' : int(max_mana),
            'percent' : int(100*(int(current_mana)/int(max_mana)))
        }
    def go(self, location:str):
        self.logger.info(f"{self.name}.go() --> traveling {location=}")
        travel_attempts = 0
        while self.check_location() != location:
            travel_attempts += 1
            self.close_all()
            location_button = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.ID, f'townObj{self.location_map[location]}'))
            )
            location_button.click()
            sleep(.2)
            if self.check_location() != location:
                self.logger.info(f"{self.name}.go() --> error traveling {location=}")
                sleep(8)
        return location
    def close_all(self):
        ActionChains(self.driver)\
        .send_keys(Keys.SPACE)\
        .perform()
    def move(self, direction:str):
        if direction == 'forward':
            ActionChains(self.driver)\
            .send_keys(Keys.UP)\
            .perform()
            return
        elif direction == 'backward':
            ActionChains(self.driver)\
            .send_keys(Keys.DOWN)\
            .perform()
            return
        elif direction == 'left':
            ActionChains(self.driver)\
            .send_keys(Keys.LEFT)\
            .perform()
            return
        elif direction == 'right':
            ActionChains(self.driver)\
            .send_keys(Keys.RIGHT)\
            .perform()
            return
        elif direction == 'whistle':
            ActionChains(self.driver)\
            .send_keys('g')\
            .perform()
    def exit_catacombs(self):
        # Spams exiting the catacombs until we've left
        while self.check_location() == 'catacombs':
            try:
                to_town_button =self.driver.find_element(By.CLASS_NAME, "gradRed")
                to_town_button.click()
            except Exception as e:
                # Failed to leave catacombs, keep trying forever. or die...
                pass
    def mobs_on_screen(self):
        mobs =  self.driver.find_elements(By.CLASS_NAME, "mob")
        return mobs
    def use_abilities(self):
        try:
            ability_elements = WebDriverWait(self.driver, 1).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, 'bbAbility'))
            )
        except:
            return
        try:
            ability_elements.reverse()
            for element in ability_elements:
                if 'gradRed' in element.get_attribute('class').split():
                    return
                if int(element.text.split()[0].replace('%', '')) >= 50:
                    element.click()
                    return
        except StaleElementReferenceException as e:
            # an ability was used and disappeared unexpectedly
            return
        except TypeError as e:
            # no ability elements were found
            return
    def attack_mob(self):
        ActionChains(self.driver)\
            .send_keys('q')\
            .perform()
        try:
            mob = self.driver.find_elements(By.CLASS_NAME, "mob")[0]
            mob.click()
        except Exception as e:
            # print('Mob died before it could be clicked')
            self.move("whistle")      
    def check_for_drops(self):
        drop_elements = None
        try:
            drops_container = self.driver.find_element(By.CLASS_NAME, "dropItemsBox")
            drop_elements = drops_container.find_elements(By.CLASS_NAME, "itemBox")
        except:
            # if finding this container errors out, there's no drops
            pass
        return drop_elements
    def _should_pickup_drop(self, item):
        self.action.send_keys("p").perform()
        proficiencies_container_element = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'pbProfs'))
        )
        transmute_proficiency_element = WebDriverWait(proficiencies_container_element, 3).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'profStat'))
        )[-2]
        player_transmute_rank = int(transmute_proficiency_element.text)
        self.action.send_keys("p").perform()
        tier_mapping = item_pickup_mapping.get(item.tier)
        if item.rarity.lower() in tier_mapping['rarity_levels']:
            if tier_mapping["ranks"]["min"] <= player_transmute_rank <= tier_mapping["ranks"]["max"]:
                return True
        return False
    def should_pickup_drop(self, item):
        if item.type == "weapon" and item.max_damage > self.inventory.weapon.max_damage:
            # print(f"Found {item}")
            return True
        elif item.type == "armor" and item.max_phys_defense > self.inventory.armor.max_phys_defense:
            # print(f"Found {item}")
            return True
        elif item.type == "charm" and item.max_spell_effect > self.inventory.charm.max_spell_effect:
            # print(f"Found {item}")
            return True
        else:
            # print(f"Ignoring: {item}")
            pass
        return False
class Player:
    def __init__(self, logger, player_controller:PlayerController, inventory:Inventory) -> None:
        self.name = "Player"
        self.logger = logger
        self.controller: PlayerController = player_controller
        self.health: dict = self.controller.check_health()
        self.mana: dict = self.controller.check_mana()
        self.location: str = self.controller.check_location()
        self.inventory: Inventory = inventory
        if self.location == "catacombs":
            self.exit_catacombs()
        self.transmute_rank: int = self.update_transmute_rank()
        # self.inventory.load()
    def enter_catacombs(self):
        self.controller.go('catacombs')
    def exit_catacombs(self):
        self.logger.info(f"{self.name}.exit_catacombs() --> Leaving Catacombs")
        self.controller.exit_catacombs()
    def update_health(self):
        self.health = self.controller.check_health()
    def update_transmute_rank(self):
        self.controller.action.send_keys(Keys.SPACE).perform()
        self.controller.action.send_keys("p").perform()
        proficiencies_container_element = WebDriverWait(self.controller.driver, 3).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'pbProfs'))
        )
        transmute_proficiency_element = WebDriverWait(proficiencies_container_element, 3).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'profStat'))
        )[-2]
        self.transmute_rank = int(transmute_proficiency_element.text)
        self.controller.action.send_keys(Keys.SPACE).perform()
    def explore(self, exit_health_percent):
        # self.controller.clear_screen()
        # print("---GOING EXPLORING---")
        # print(f"Will return at {exit_health_percent}% health")
        retreat = False
        self.controller.go('catacombs')
        while retreat == False:
            combat_occurred = False
            movement_direction = choice(['forward', 'left', 'right'])
            # sleep(.3)
            self.controller.move(movement_direction)
            # Continiously look to see if there's a mob on screen
            while True:
                self.update_health()
                # Pick up drops if there are any and get True/False result
                dropped_item_elements = self.controller.check_for_drops()
                if dropped_item_elements:
                    # work the list from back to front to preserve element order
                    dropped_item_elements.reverse()
                    for item_element in dropped_item_elements:
                        try:
                            self.inventory.controller.action.move_to_element(item_element).perform()
                        except StaleElementReferenceException:
                            self.logger.info(f"{self.name} --> StaleElementReferenceException: Element in dropped items container became stale")
                            continue
                        try:
                            item_comparison_grouping = self.controller.driver.find_element(By.CLASS_NAME, 'tbItemDesc')
                        except NoSuchElementException:
                            self.logger.info(f"{self.name} --> NoSuchElementException: item_comparison_grouping could not be located")
                            continue
                        try:
                            item_description_element = item_comparison_grouping.find_elements(By.XPATH, "./child::*")[0]
                        except StaleElementReferenceException:
                            self.logger.info(f"{self.name} --> StaleElementReferenceException: item_comparison_grouping stale")
                            continue
                        overlay_stats = item_element.text.replace('+',"").split('\n')
                        if len(overlay_stats) == 1:
                            overlay_stats.insert(0, '0')
                        item = self.inventory.controller.convert_item_from_element(item_description_element, overlay_stats)
                        if self.controller._should_pickup_drop(item):
                            item_element.click()
                # If we picked something up the inventory might've become full
                if dropped_item_elements and self.inventory.is_full():
                    # print("Inventory full, breaking combat loop")
                    retreat = True
                    break
                if self.health['percent'] <= exit_health_percent:
                    # print("Health too low, breaking combat loop")
                    retreat = True
                    break
                # if there are 9 mobs on screen likely they replicate too fast to be killed
                # joining and leaving a group will reset the catacombs and mobs
                active_mobs = self.controller.mobs_on_screen()
                if len(active_mobs) == 9:
                    self.logger.info(f"{self.name}.explore() --> Too many mobs to combat")
                    # command to join a goup
                    self.logger.info(f"{self.name}.explore() --> Joining group")
                    command = "njs.sendBytes(60, 3, 2, 5)"
                    self.controller.driver.execute_script(command)
                    sleep(2)
                    self.logger.info(f"{self.name}.explore() --> Leaving group")
                    # command to leave a group
                    command = "njs.sendBytes(60, 5)"
                    self.controller.driver.execute_script(command)
                    break
                # See if there are any mobs attacking the player
                if 0 < len(active_mobs) < 9:
                    mob_names = []
                    for name in active_mobs:
                        try:
                            mob_names.append(name.text)
                        except:
                            pass
                    # If this is the first time we've noticed the group attacking us
                    if combat_occurred == False:
                        # Show which mobs we are in battle with
                        # print(f"\nIn battle with: {mob_names}")
                        combat_occurred = True
                    # use an ability if it is ready
                    self.controller.use_abilities()
                    # and attack them!
                    self.controller.attack_mob()
                
                else:
                    break
            # If the player saw combat
            if combat_occurred == True:
                # Get how much health is remaining
                self.health = self.controller.check_health()
                # then to re-engage with the maze
                self.controller.move("whistle")
        self.exit_catacombs()
    def rest(self, stop_resting_health=100):
        while self.health['percent'] < stop_resting_health:
            self.update_health()
            # self.controller.clear_screen()
            # print("---Resting---")
            # print(f"Health:\t{self.health['current']}/{self.health['max_health']}")
            # print(f"Pack:\t{len(list(self.inventory.equipment.items()))}/9")
            # print(f"Weapon:\t{self.inventory.weapon.name.title()}")
            # print(f"Armor:\t{self.inventory.armor.name.title()}")
            # print(f"Charm:\t{self.inventory.charm.name.title()}")
            # print(f"Charm:\t{self.inventory.acc_charm.name.title()}")
            sleep(.25)
#-----------------------------------------------
class MarketController:
    def __init__(self, driver, logger, gold_password) -> None:
        self.name = "MarketController"
        self.logger = logger
        self.gold_password = gold_password
        self.driver = driver
        self.action = ActionChains(self.driver)  
    def open(self):
        self.action.send_keys(Keys.SPACE).perform()
        self.action.send_keys("m").perform()
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'marketTabs'))
            )
        except TimeoutError as e:
            raise e
    def _open_sell_tab(self):
        self.open()
        market_tabs = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'marketTabs'))
        )
        search, sell, transfer = market_tabs.find_elements(By.CLASS_NAME, 'njRB')
        sell.click()
        return
    def search(self, type:str=None, subtype:str=None, min_level:int=None, max_level:int=None, min_magic:int=None, max_magic:int=None, min_cost:int=0, max_cost:int=999999, attribute1:str=None, attribute2:str=None, attribute3:str=None, only_equipable:bool=False):
        market_controls = self.driver.find_element(By.CLASS_NAME, 'marketControls')
        selection_fields = Select(market_controls.find_elements(By.TAG_NAME, 'select'))
        if type:
            type_select = selection_fields[0]
            type_select.select_by_visible_text(type)
        if subtype:
            subtype_select = selection_fields[1]
            subtype_select.select_by_visible_text(subtype)
        level_map = {
                1: "I (0)",
                2: "II (0)",
                3: "III (0)",
                5: "IV (5)",
                10: "V (10)",
                15: "VI (15)",
                20: "VII (20)",
                25: "VIII (25)",
                30: "IX (30)",
                35: "X (35)",
                40: "XI (40)",
                45: "XII (45)",
                50: "XIII (50)",
                55: "XIV (55)"
            }        
        if min_level:
            min_level_select = selection_fields[2]
            min_level_select.select_by_visible_text(level_map[min_level])
        if max_level:
            max_level_select = selection_fields[3]
            max_level_select.select_by_visible_text(level_map[max_level])
        if min_magic:
            min_magic_select = selection_fields[4]
            min_magic_select.select_by_visible_text(level_map[min_magic])
        if max_magic:
            max_magic_select = selection_fields[5]
            max_magic_select.select_by_visible_text(level_map[max_magic])
        if min_cost:
            self.driver.find_element(By.XPATH, '//*[@id="stage"]/div[5]/div[2]/div[1]/div[5]/input[1]').send_keys(str(min_cost))
        if max_cost and max_cost != 999999:
            self.driver.find_element(By.XPATH, '//*[@id="stage"]/div[5]/div[2]/div[1]/div[5]/input[2]').send_keys(str(max_cost))
        if attribute1:
            attribute1 = {
                'Enhanced Effect' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[2]',
                'Strength' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[3]',
                'Dexterity' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[4]',
                'Vitality' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[5]',
                'Intelligence' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[6]',
                'Max Life' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[7]',
                'Max Mana' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[2]',
                'Experience Gained' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[8]',
                'Magic Luck' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[9]',
                'Life Regen' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[10]',
                'Mana Regen' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[11]',
                'Extra Equipment Slots' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[12]',
                'Critical Strike' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[13]',
                'Life per Attack' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[14]',
                'Mana per Attack' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[15]',
                'Life per Kill' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[16]',
                'Mana per Kill' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[17]',
                'Life Steal' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[18]',
                'Damage Return' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[19]',
                'Mind Numb' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[20]',
                'Armor Pierce' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[22]',
                'Parry' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[22]',
                'Critical Flux' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[22]',
                'Physical Damage Reduction' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[24]',
                'Magical Damage Reduction' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[25]',
                'Mana Syphon' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[26]',
                'Quick Draw' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[27]',
                'Mana Consumption' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[28]',
                'Heal Mastery' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[29]',
                'Mana Skin' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[30]',
                'Power Shot' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[31]',
                'Glancing Blow' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[32]',
                'Jubilance' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[33]',
                'Ice Mastery' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[34]',
                'Fire Mastery' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[35]',
                'Lightning Mastery' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[36]',
                'Wind Mastery' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[37]',
                'Earth Mastery' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[38]',
                'Quantity' : '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/select/option[39]'
            }
            self.driver.find_element(By.XPATH, '//*[@id="stage"]/div[5]/div[2]/div[1]/div[6]/input').send_keys(str(1))
            self.driver.find_element(By.XPATH, attribute1['Vitality']).click()
        if attribute2:
            attribute2 = {k:v.replace('div[6]','div[7]') for k,v in attribute1.items()}
            self.driver.find_element(By.XPATH, '//*[@id="stage"]/div[5]/div[2]/div[1]/div[7]/input').send_keys(str(1))
            self.driver.find_element(By.XPATH, attribute2['Vitality']).click()
        if attribute3:
            attribute3 = {k:v.replace('div[6]','div[8]') for k,v in attribute1.items()}
            self.driver.find_element(By.XPATH, '//*[@id="stage"]/div[5]/div[2]/div[1]/div[8]/input').send_keys(str(1))
            self.driver.find_element(By.XPATH, attribute3['Vitality']).click()

    def sell_equipment(self, player_equipment):
        for item_index in player_equipment:
            if player_equipment[item_index] is None:
                self.logger.info(f"{self.name} --> No equipment in slot {item_index}")
                continue
            rarity = player_equipment[item_index].rarity
            tier = player_equipment[item_index].tier
            price = self._should_sell(rarity, tier)
            if price is not None:
                self._sell(item_index, price)
        self.action.send_keys(Keys.SPACE).perform()
    def _sell(self, equipment_item_index, price):
        self.action.send_keys(Keys.SPACE).perform()
        self.action.send_keys("m").perform()
        self._open_sell_tab()
        equipment_container = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'invEqBox'))
        )
        equipment_elements = WebDriverWait(equipment_container, 3).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'itemSlotBox'))
        )
        equipment_element_to_sell = equipment_elements[equipment_item_index]
        ActionChains(self.driver) \
        .key_down(Keys.SHIFT) \
        .click(equipment_element_to_sell) \
        .key_up(Keys.SHIFT) \
        .perform()
        cost_field = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.ID, 'mkSellCost'))
        )
        cost_field.clear()
        cost_field.send_keys(f"{price}")  # Replace YOUR_USERNAME with your actual username
        gold_pw_field = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.ID, 'mkGpwd'))
        )
        gold_pw_field.clear()
        gold_pw_field.send_keys(self.gold_password)
        sell_item_button = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.ID, 'mkBuySell'))
        )
        sell_item_button.click()
        sleep(1)
    
    def _should_sell(self, item_rarity, item_tier):
        prices_per_level = prices.get(item_rarity)
        if prices_per_level == None:
            return False
        price = prices_per_level.get(item_tier)
        # print(f"{price=}")
        return price
#-----------------------------------------------
class VaultController:
    def __init__(self, driver, logger) -> None:
        self.name = "VaultController"
        self.logger = logger
        self.driver = driver
        self.action = ActionChains(self.driver)
    def open(self):
        self.action.send_keys(Keys.SPACE).perform()
        self.action.send_keys("v").perform()
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'vaultTabs'))
            )
        except TimeoutError as e:
            raise e
    def _open_deposit_tab(self):
        self.open()
        market_tabs = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'vaultTabs'))
        )
        vault, withdraw, deposit, transfer = market_tabs.find_elements(By.CLASS_NAME, 'njRB')
        deposit.click()
        return
    def deposit_equipment(self, player_equipment):
        self.action.send_keys(Keys.SPACE).perform()
        self._open_deposit_tab()
        for item_index in player_equipment:
            if player_equipment[item_index] is None:
                self.logger.info(f"{self.name} --> no equipment in slot {item_index}")
                continue
            stats = player_equipment[item_index].stats
            tier = player_equipment[item_index].tier
            if self._should_deposit(tier, stats):
                self._deposit(item_index)
        self.action.send_keys(Keys.SPACE).perform()
    def _deposit(self, equipment_item_index):
        equipment_container = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'invEqBox'))
        )
        equipment_elements = WebDriverWait(equipment_container, 3).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'itemSlotBox'))
        )
        equipment_element_to_deposit = equipment_elements[equipment_item_index]
        ActionChains(self.driver) \
        .key_down(Keys.SHIFT) \
        .click(equipment_element_to_deposit) \
        .key_up(Keys.SHIFT) \
        .perform()
        sell_item_button = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'vDepB'))
        )
        sell_item_button.click()
        sleep(1)
    def _should_deposit(self, item_tier, item_stats):
        stats_per_tier = deposit_criteria.get(item_tier)
        if stats_per_tier == None:
            return False
        for stat in item_stats:
            if stat in stats_per_tier:
                return True
        return False
#-----------------------------------------------
class TransmuteController:
    def __init__(self, driver, logger) -> None:
        self.name = "TransmuteController"
        self.logger = logger
        self.driver = driver
        self.action = ActionChains(self.driver)
    def transmute_equipment(self, player_transmute_rank, player_equipment):
        self.logger.info(f"{self.name} --> Starting transmute routine")
        self.action.send_keys(Keys.SPACE).perform()
        for item_index in player_equipment:
            item = player_equipment[item_index]
            if item and self._should_transmute(item, player_transmute_rank):
                self._transmute(item_index)
    def _should_transmute(self, item, player_transmute_rank):
        self.logger.info(f"{self.name} --> checking if {item} should be transmuted")
        tier_mapping = transmute_mapping.get(item.tier)
        if item.rarity.lower() in tier_mapping['rarity_levels']:
            if tier_mapping["ranks"]["min"] <= player_transmute_rank <= tier_mapping["ranks"]["max"]:
                return True
        return False
    def _transmute(self, equipment_item_index):
        self.logger.info(f"{self.name} --> transmuting item {equipment_item_index}")
        self.action.send_keys(Keys.SPACE).perform()
        # open transmute menu
        transmute_town_element = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.ID, 'townObj6'))
        )
        transmute_town_element.click()
        # get equipment container
        equipment_container = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'invEqBox'))
        )
        # get equipment elements
        equipment_elements = WebDriverWait(equipment_container, 3).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'itemSlotBox'))
        )
        element_to_transmute = equipment_elements[equipment_item_index]
        ActionChains(self.driver) \
        .key_down(Keys.SHIFT) \
        .click(element_to_transmute) \
        .key_up(Keys.SHIFT) \
        .perform()
        begin_transmute_button = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'skBut'))
        )
        begin_transmute_button.click()
        sleep(.25)
        # container that appears after starting the transmute skill 'mini-game'
        transmute_skill_container = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'skillBody'))
        )
        # buttons from within the transmute mini-game container
        transmute_skill_element_buttons = WebDriverWait(self.driver, 3).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'skBut'))
        )
        transmute_button = transmute_skill_element_buttons[0]
        stabilize_button = transmute_skill_element_buttons[1]
        if transmute_button.text.strip() == "Stabilize":
            transmute_button, stabilize_button = stabilize_button, transmute_button
        self.logger.info(f"{self.name} --> starting transmutation minigame")
        while True:
            try:
                volatality_progress_meter, transmute_progress_meter = WebDriverWait(transmute_skill_container, 3).until(
                    EC.visibility_of_all_elements_located((By.CLASS_NAME, 'meterBoxProg'))
                )
            except TimeoutException:
                self.logger.info(f"{self.name} --> TimeoutException: couldn't locate volatility or transmutation progress meter")
                break
                # transmute_progress_value = 100 - int(transmute_progress_meter.value_of_css_property('width').replace("%", ''))
            volatality_progress_value = int(volatality_progress_meter.get_attribute("style").split(";")[2].replace(' ', '').replace('%', '').split(":")[1])
            if volatality_progress_value >= 50:
                try:
                    stabilize_button.click()
                except:
                    self.logger.info(f"{self.name} --> TimeoutException: couldn't click stabilize button")
                    break
            else:
                try:
                    transmute_button.click()
                except StaleElementReferenceException as e:
                    self.logger.info(f"{self.name} --> TimeoutException: couldn't click transmute button")
                    break
                # elements will change if the transmute is complete or volatility completes
                # this will raise an exception indicating and indicates the action is complete
                # return
        self.action.send_keys(Keys.SPACE).perform()
        self.logger.info(f"{self.name} --> done transmuting item {equipment_item_index}")
        return
#-----------------------------------------------
class LevelingController:
    def __init__(self, driver, logger) -> None:
        self.name = "LevelingController"
        self.logger = logger
        self.driver = driver
        self.action = ActionChains(self.driver)
    def run(self):
        self.logger.info(f"{self.name} --> Performing leveling routine")
        while self.stat_points_available():
            self.use_stat_point("vitality")
        while self.ability_points_available():
            self.use_ability_point("powerstrike")
    def stat_points_available(self):
        self.logger.info(f"{self.name} --> Checking for available stat points")
        self.action.send_keys(Keys.SPACE).perform()
        self.action.send_keys("c").perform()
        stat_points_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.ID, 'CS7'))
        )
        available_points = int(stat_points_element.text)
        self.action.send_keys(Keys.SPACE).perform()
        if available_points > 0:
            return True
        else:
            return False
    def use_stat_point(self, stat_name:str):
        self.logger.info(f"{self.name} --> Using stat point on {stat_name}")
        self.action.send_keys(Keys.SPACE).perform()
        self.action.send_keys("c").perform()
        # get vitality container
        if stat_name == "vitality":
            stat_container = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.ID, 'CS6'))
            )
        try:
            increase_stat_button = WebDriverWait(stat_container, 3).until(
                EC.presence_of_element_located((By.TAG_NAME, 'svg'))
            )
            increase_stat_button.click()
        except TimeoutException:
            self.logger.info(f"{self.name} --> Could not locate increase_stat_button")
        self.action.send_keys(Keys.SPACE).perform()
    def ability_points_available(self):
        self.logger.info(f"{self.name} --> Checking for available ability points")
        self.action.send_keys(Keys.SPACE).perform()
        self.action.send_keys("c").perform()
        ability_points_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.ID, 'CS8'))
        )
        available_points = int(ability_points_element.text)
        self.action.send_keys(Keys.SPACE).perform()
        if available_points > 0:
            return True
        else:
            return False
    def use_ability_point(self, ability_name):
        self.logger.info(f"{self.name} --> Using ability point on {ability_name}")
        self.action.send_keys(Keys.SPACE).perform()
        self.action.send_keys("c").perform()
        # get vitality container
        weapon_abilities_container = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.ID, 'sWAbs'))
        )
        ability_elements = WebDriverWait(weapon_abilities_container, 3).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'abilityIcon'))
        )
        if ability_name == "powerstrike":
            ability_element = ability_elements[0]
        ability_element.click()
        self.action.send_keys(Keys.SPACE).perform()
#-----------------------------------------------   
class GroupHandler:
    def __init__(self, driver, logger) -> None:
        self.name = "GroupHandler"
        self.logger = logger
        self.driver = driver
    def create(self):
        command = "njs.sendBytes(60, 3, 2, 5)"
        self.driver.execute_script(command)
    def leave(self):
        command = "njs.sendBytes(60, 5)"
        self.driver.execute_script(command)
#-----------------------------------------------   