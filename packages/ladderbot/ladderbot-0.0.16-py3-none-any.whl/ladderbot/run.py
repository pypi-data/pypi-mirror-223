# import pdb
import json
import logging
import platform
import undetected_chromedriver as uc
from tkinter import Tk, Label, Entry, Button, Checkbutton, IntVar
from ladderbot.html_creator import make_game_html
from ladderbot.controllers import Login, LoginController, Player, Inventory, PlayerController, InventoryController, MarketController, VaultController, TransmuteController, LevelingController
import pkgutil
import importlib.resources
import json
#-----------------------------------------------
def bot():
    logo_icon = pkgutil.get_data('ladderbot', 'Logo.ico')
    root = Tk()
    root.geometry("230x200")
    root.title("LadderBot")
    root.iconbitmap(logo_icon)
    uname_label = Label(root, text="Username:")
    uname_label.pack()
    uname_entry = Entry(root)
    uname_entry.pack()
    uid_label = Label(root, text="UID:")
    uid_label.pack()
    uid_entry = Entry(root)
    uid_entry.pack()
    hash_label = Label(root, text="Hash:")
    hash_label.pack()
    hash_entry = Entry(root, show="*")
    hash_entry.pack()
    remember_var = IntVar()
    remember_checkbox = Checkbutton(root, text="Remember", variable=remember_var)
    remember_checkbox.pack()
    load_values(uname_entry, uid_entry, hash_entry, remember_checkbox)
    submit_button = Button(root, text="Submit", command=lambda: submit(uname_entry, uid_entry, hash_entry, remember_var, root))
    submit_button.pack()
    root.mainloop()
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=str(importlib.resources.files("ladderbot")) + "\\debug.log",
        filemode='w'
    )
    # Create logger
    logger = logging.getLogger()
    # Set the options for the Chrome driver
    chrome_options = uc.ChromeOptions()
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    # Set the window position
    chrome_options.add_argument("--window-position=-5,695")
    chrome_options.add_experimental_option("prefs", prefs)
    # Check the system's operating system
    platform_name = platform.system()
    logger.info(f"Running on {platform_name}")
    driver = uc.Chrome(options=chrome_options)
    # Set the window size
    driver.set_window_size(900, 705)
    # Initialize all controllers before interacting with the driver or driver de-sync can occur
    login_controller = LoginController(driver, logger)
    player_controller = PlayerController(driver, logger)
    leveling_controller = LevelingController(driver, logger)
    inventory_controller = InventoryController(driver, logger)
    transmute_controller = TransmuteController(driver, logger)
    market = MarketController(driver, logger, gold_password='temp')
    vault = VaultController(driver, logger)
    # Create Login instance and boot the game
    login = Login(login_controller)
    login.run(character_name='kdasje1')
    # Create Player and Inventory instances to maintain game data
    inventory = Inventory(inventory_controller)
    player = Player(logger, player_controller, inventory)
    while True:
            # try:
                leveling_controller.run()
                player.update_health()
                player.update_transmute_rank()
                player.inventory.load()
                transmute_controller.transmute_equipment(player.transmute_rank, player.inventory.equipment)
                vault.deposit_equipment(player.inventory.equipment)
                market.sell_equipment(player.inventory.equipment)
                if player.health['percent'] >= 100:
                    player.explore(exit_health_percent=30)
                else:
                    player.rest(100)
            # except:
            #     driver.close()
            #     return
#-----------------------------------------------
def submit(uname_entry, uid_entry, hash_entry, remember_var, root):
    username = uname_entry.get()
    uid = uid_entry.get()
    hash = hash_entry.get()
    if remember_var.get():
        save_values(username, uid, hash)
    root.destroy()
    while True:
        # try:
            make_game_html(username, uid, hash)
            bot(username, uid, hash)
        # except:
        #     pass
        
#-----------------------------------------------
def save_values(uname, uid, hash):
    data = {
        'uname': uname,
        'uid': uid,
        'hash': hash
    }
    with open(str(importlib.resources.files("ladderbot")) + "\\creds.json", "w") as file:
        json.dump(data, file)
#-----------------------------------------------
def load_values(uname_entry, uid_entry, hash_entry, remember_checkbox):
    with open(str(importlib.resources.files("ladderbot")) + "\\creds.json") as file:
        data = json.load(file)
    try:
        uname_entry.delete(0, 'end')
        uname_entry.insert('end', data['uname'])
        uid_entry.delete(0, 'end')
        uid_entry.insert('end', data['uid'])
        hash_entry.delete(0, 'end')
        hash_entry.insert('end', data['hash'])
        remember_checkbox.select()
    except FileNotFoundError:
        print("No saved values found")
        #-----------------------------------------------