import pygame
import random
import math
import dan_gui
import pickle


# Class for a rectangle that is drawn to the screen and has a collision hit box
# Represents a metal terminal
class MetalRect:

    # Takes x, y, width and height as parameters
    # Used in drawing the rectangle
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # Creates a pygame Rect object to manage collisions
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    # Draws the rectangle to the screen
    def draw(self, screen, colour):
        pygame.draw.rect(screen, colour, (self.x, self.y, self.width, self.height))


# Class that models the behaviour of a photon
class Photon:

    # All photon objects are held in this static one-dimensional list
    PhotonList = []
    # Constant value for radius of each photon in pixels
    Radius = 4
    # Static value that keeps track of how many frames it has been since the last photon was emitted
    LastEmitted = 0

    # Photon object takes a tuple of 3 integers between 0 and 255 as the colour
    # Also takes a real number as the kin_energy to represent the kinetic energy of the photon
    def __init__(self, colour, kin_energy):
        self.colour = colour
        self.kinEnergy = kin_energy
        # Randomises x and y co-ords along the bottom of the lamp image
        self.x = 500 + 16 + random.randint(0, 180)
        self.y = 150 + 54 + random.randint(0, 100)
        # the speed variables represent how many pixels the photon moves in each axis per frame
        self.h_speed = -10
        self.v_speed = 4
        # Creates a pygame Rect object to handle collisions with metal terminal
        self.rect = pygame.Rect(self.x, self.y, 2*Photon.Radius, 2*Photon.Radius)

    # Destroys the object by removing itself by the list then deleting itself
    def destroy(self):
        index = self.find_self()
        Photon.PhotonList.pop(index)
        del self

    # Allows a photon to find itself in the PhotonList by comparing itself to each item in the list
    # Returns the index of that photon in the PhotonList
    def find_self(self):
        index = -1
        for i in range(len(Photon.PhotonList)):
            if Photon.PhotonList[i] == self:
                index = i
                break
        return index

    # Alters the x and y co-ords of the photon by the respective speed variable
    def move(self):
        self.x += self.h_speed
        self.y += self.v_speed
        # Moves the pygame Rect object for collisions
        self.rect.move_ip(self.h_speed, self.v_speed)

    # Checks if the photon object's collision Rect collides with the parameter rect
    # Takes stop_voltage for should_create_electron
    # If collision detected, checks if electron should be made
    # Electron object made if necessary, then photon is deleted
    def check_collision(self, rect, stop_voltage):
        if self.rect.colliderect(rect):
            if self.should_create_electron(stop_voltage):
                self.create_electron()
            self.destroy()
        # If photon goes off screen (either too far left or too far right) then it is deleted
        elif self.x < -2*Photon.Radius or self.y > 800 + 2*Photon.Radius:
            self.destroy()

    # Creates an electron object with the same y co-ord and kinetic energy
    def create_electron(self):
        Electron.ElectronList.append(Electron(self.y, self.kinEnergy))

    # If the kinetic energy of the photon (minus stopping voltage) is greater than 0, returns true
    def should_create_electron(self, stop_voltage):
        stop_voltage = stop_voltage * 1.6 * math.pow(10, -19)
        if (self.kinEnergy - stop_voltage) > 0 * math.pow(10, -19):
            # Only affects actual variable once electron is about to be made
            # Prevents stopping voltage being taken away multiple times
            self.kinEnergy = self.kinEnergy - stop_voltage
            return True
        else:
            return False

    # Draws a circle to the screen to represent the photon
    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), Photon.Radius)


# Class to model an electron particle
class Electron:

    # The one-dimensional list of all electrons between the 2 metal plates
    ElectronList = []
    # The one-dimensional list of all electrons that have hit the right metal plate in the last second
    # Constant value used in drawing the circle that represents the electron
    Radius = 5
    # Constant value for the mass of an electron
    Mass = 9.11 * math.pow(10, -31)

    # Takes in the y co-ord and kinetic energy as parameters
    def __init__(self, y, kin_energy):
        self.kinEnergy = kin_energy
        self.x = 60
        self.y = y
        self.draw_x = round(self.x)
        self.draw_y = round(self.y)
        # Creates a pygame Rect object to handle collisions
        self.rect = pygame.Rect(self.draw_x, self.draw_y, 2 * Electron.Radius, 2 * Electron.Radius)
        # Gets the speed of the electron in pixels per frame by multiplying it by 10^19
        self.speed = kin_energy * math.pow(10, 19)

    # Destroys electron by removing from ElectronList then deleting it
    def destroy(self):
        index = self.find_self()
        Electron.ElectronList.pop(index)
        del self

    # Finds self in ElectronList by comparing each object to itself then returns the index
    def find_self(self):
        index = -1
        for i in range(len(Electron.ElectronList)):
            if Electron.ElectronList[i] == self:
                index = i
                break
        return index

    # Changes the x co-ord and the top-left co-ord of the Rect of the electron by its speed
    # Only moves in x axis, electrons moving horizontally only.
    def move(self):
        self.x += self.speed
        self.draw_x = round(self.x)
        self.rect = pygame.Rect(self.draw_x, self.draw_y, 2 * Electron.Radius, 2 * Electron.Radius)

    # If the electron is colliding with the Rect parameter rect
    # Deletes electron object
    def check_pos(self, rect):
        if self.rect.colliderect(rect):
            self.destroy()

    # Draws a circle to represent the electron
    def draw(self, screen):
        # Draw inner part
        pygame.draw.circle(screen, (60, 230, 255), (self.draw_x, self.draw_y), Electron.Radius - 1)
        # Draw border
        pygame.draw.circle(screen, (0, 0, 0), (self.draw_x, self.draw_y), Electron.Radius, 2)


# Class to represent a metal
class Metal:

    # Static list of metal objects
    MetalList = []
    # Static list of the names of all metal objects
    MetalNames = []

    # Parameters:
    # name - The Metal's name
    # work_func - The work function of the metal
    # colour - an tuple of 3 ints from 0-255 to represent an RGB colour
    def __init__(self, name, work_func, colour):
        self.name = name
        self.work_func = work_func
        self.colour = colour
        # On Initialisation adds the metal's name to a list of metal names
        Metal.MetalNames.append(name)


# Beginning of actual code
# Initialise all pygame modules before they can be used
pygame.init()

# These variables hold the dimensions of the screen, should be kept constant
display_width = 800
display_height = 600

# Colour definitions for referring to later
black = (0, 0, 0)
white = (255, 255, 255)
grey = (100, 100, 100)
lightGrey = (180, 180, 180)

# Initialise main drawing surface
screen = pygame.display.set_mode((display_width, display_height))
# Set title of window
pygame.display.set_caption("Photoelectric Effect Simulator")
# Create clock object for timing
clock = pygame.time.Clock()

# Tuple of min wavelengths for UV, violet, blue, cyan, yellow and red
wlValues = (850, 750, 620, 570, 495, 450, 380, 0)
wlValues2 = (0, 380, 450, 495, 570, 620, 750, 850)


# Basic method to convert a string to an integer
def get_int_from_str(text):
    # Try statement catches errors in case of invalid input
    try:
        i = int(text)
    except ValueError:
        i = 0
    return i


# Basic method to convert a string to a float
def get_float_from_string(text):
    # Try statement catches error in case of invalid input
    try:
        i = float(text)
    except ValueError:
        i = 0
    return i


# Called 30 times a second to check if an photon should be emitted
def emit_photon(current_metal, intensity, wavelength):
    # firstly checks if intensity is above 0, if not, no photons are being released
    if intensity > 0:
        # Photon.LastEmitted is a timer, whenever it reaches 0, a photon should be emitted
        if Photon.LastEmitted == 0:
            # Creates frequency, needed for calculations
            frequency = (3 * math.pow(10, 8)) / wavelength
            # Determines the total energy of an electron
            tot_energy = (6.62607004 * math.pow(10, -34)) * frequency
            # Kinetic energy is leftover energy from breaking off of surface of metal.
            # If its positive, it has escaped the metal surface
            kin_energy = tot_energy - current_metal.work_func
            # Creates a new Photon
            Photon.PhotonList.append(Photon((set_light_colour(wavelength)), kin_energy))
            # Sets LastEmitted to a value inversely proportional to intensity
            # Higher the intensity, the sooner the next photon with be released
            Photon.LastEmitted = math.ceil((1/intensity) * 100)
        else:
            # If timer not yet at 0, decrement it
            Photon.LastEmitted -= 1


# Given a string name, finds the first metal in the MetalList that has the same name
# Returns that metal object
def find_metal(name):
    new_metal = None
    for m in Metal.MetalList:
        if name == m.name:
            new_metal = m
    return new_metal


# Loads any custom made metals the user has previously created
# Loads it from data/custom_metals.dat - a binary file
# Parameter: drop - A DropDown object to add the metals to
def load_custom_metals(drop):
    # Tries to open the file, if it can't, catches exception and tells user
    i = 0
    try:
        f = open("data/custom_metals.dat", "rb")
        # Once the file is open, keeps trying to read it until it reaches the end of the file
        while 1:
            try:
                # Uses the pickle module to deserialised the Metal object in the file
                new_metal = pickle.load(f)
                # Adds the metal's name to the MetalNames list
                Metal.MetalNames.append(new_metal.name)
                # Adds the custom metal to the drop-down list
                drop = add_new_metal(new_metal, drop)
            except (EOFError, pickle.UnpicklingError):
                break
        # Closes the file to prevent using unnecessary memory
        f.close()
    except FileNotFoundError:
        print("ERROR: Cannot find data/custom_metals.dat")
    # Returns the modified DropDown item
    return drop


# Adds a new metal object to the MetalList and updates the dropdown box that stores the metals
def add_new_metal(new_metal, drop):
    Metal.MetalList.append(new_metal)
    drop.data = Metal.MetalNames
    drop.options = drop.data
    return drop


# Calculates the alpha value for the colour of the light
# Takes in a wavelength between 100 and 850
# And an intensity between 0 and 100
def set_light_alpha(wavelength, intensity):
    # wMod is the modifier to the alpha that the wavelength causes
    w_mod = 1
    wavelength = wavelength * math.pow(10, 9)
    # If no light, fully transparent
    if intensity == 0:
        return 0
    else:
        # If the wavelength is between 350 and 300 nm, wMod decreases as wavelength does
        if wavelength < 350:
            if wavelength > 300:
                w_mod = 1 - ((350 - wavelength) / 50)
            else:
                # If wavelength below 300nm it's fully transparent as its below wavelength of visible light
                w_mod = 0
        # If the wavelength is between 750 and 800nm, wMod decreases as wavelength increases
        elif wavelength > 750:
            if wavelength < 800:
                w_mod = (800 - wavelength) / 50
            else:
                # If wavelength is above 800nm, it's fully transparent as its above wavelength of visible light
                w_mod = 0
        # alpha is capped at 128 (half of opaque value). Is proportional to intensity and wMod
        alpha = 100 * (intensity / 100) * w_mod
        # Rounds alpha to integer
        alpha = round(alpha)
        return alpha


# Used in setting the colour of the light and photons
# Uses the tuples min_wavelength and max_wavelength
# These tuples are wavelength boundaries for specific colours
# Given a wavelength, finds the upper and lower bounds of it to find what colour it is
def set_min_max(wavelength):
    min_wavelength = 0
    max_wavelength = 0
    for i in range(len(wlValues) - 1):
        if wavelength <= wlValues[i]:
            min_wavelength = wlValues[i]
            max_wavelength = wlValues[i+1]
    return min_wavelength, max_wavelength


# Returns an RGB colour tuple given a wavelength
# Finds the upper and lower bounds of the colour the wavelength causes
# Sets the colour proportionally to how far the wavelength value is between the boundaries
# For example: if the wavelength is half way between the boundary between yellow and red
# The colour is half-way between yellow and orange
def set_light_colour(wavelength):
    wavelength = wavelength * math.pow(10, 9)
    min_wavelength, max_wavelength = set_min_max(wavelength)
    # In this system, there are 3 colour variables, R G and B
    # One will always by 0, 1 will always be 255 (except for violet)
    # and the other will be var_colour
    # var_colour is highest when the wavelength is at the upper boundary and at lowest at lower boundary
    var_colour = round(((wavelength - min_wavelength) / (max_wavelength - min_wavelength)) * 255)
    r = 0
    g = 0
    b = 0
    # If ir to red
    if min_wavelength == wlValues[0]:
        r = 255
    # If red to yellow
    elif min_wavelength == wlValues[1]:
        r = 255
        g = var_colour
    # If yellow to green
    elif min_wavelength == wlValues[2]:
        r = 255 - var_colour
        g = 255
    # If green to cyan
    elif min_wavelength == wlValues[3]:
        g = 255
        b = var_colour
    # If cyan to blue
    elif min_wavelength == wlValues[4]:
        g = 255 - var_colour
        b = 255
    # If blue to purple
    elif min_wavelength == wlValues[5]:
        r = round((var_colour / 255) * 180)
        b = 255
    # If purple to UV
    elif min_wavelength == wlValues[6]:
        r = 180
        b = 255
    return r, g, b


# Loads from settings.dat
# Reads a boolean from the file that shows individual photons when True
def load_settings():
    # Checkbox holds value of the boolean in the binary file
    # Set to True by default
    checkbox = True
    try:
        # Opens the settings.dsy file, if it can't tells the user
        f = open("data/settings.dat", "rb")
        # Deserialises the boolean value saved to the file
        checkbox = pickle.load(f)
        # Closes the file to prevent unneeded memory use
        f.close()
    except(EOFError, pickle.UnpicklingError):
        print("Error reading settings.dat")
        # If file can't be read, checkbox is set to True by default
    except(FileNotFoundError):
        print("settings.dat is missing, creasing a new one")
        f = open("data/settings.dat", "wb")
        # Serialises boolean value of True as a default
        pickle.dump(True, f)
        # Closes file to prevent unnecessary memory usage
        f.close()
    return checkbox


# Deletes the contents of file f
def delete_file(f):
    f.seek(0)
    f.truncate()

# The main game code is run here
def game_loop():
    # Creating the loop boolean, this is false until the game exits
    game_exit = False

    # Starting value definitions
    wavelength = 0
    intensity = 0

    # Appends default metals to the metal list
    Metal.MetalList.append(Metal("Sodium", 3.65 * math.pow(10, -19), (100, 100, 100)))
    Metal.MetalList.append(Metal("Copper", 7.53 * math.pow(10, -19), (145, 88, 4)))
    Metal.MetalList.append(Metal("Zinc", 6.89 * math.pow(10, -19), (185, 195, 185)))
    Metal.MetalList.append(Metal("Magnesium", 5.90 * math.pow(10, -19), (205, 205, 205)))
    # Sets starting metal to the first one in the list (sodium)
    current_metal = Metal.MetalList[0]

    # Defines the fonts that the program will use for drawing text
    my_font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 25)

    # Text objects used to describe the different GUI elements
    wave_txt = my_font.render("Wavelength: ", 1, (0, 0, 0))
    wave_txt2 = my_font.render("nm", 1, (0, 0, 0))
    intensity_txt = my_font.render("Intensity: ", 1, black)
    intensity_txt2 = my_font.render("%", 1, black)
    metal_txt = my_font.render("Metal: ", 1, black)
    stop_txt = my_font.render("Stopping Voltage: ", 1, black)
    stop_txt2 = my_font.render("V", 1, black)

    # Rectangles on left and right to represent metals
    left_rect = MetalRect(10, 400, 50, 150)
    right_rect = MetalRect(740, 400, 50, 150)

    # Wavelength Slider bar creation
    wv_slider = dan_gui.Slider(150, 5, 200, 25, small_font, (100, 850))
    # Setting default wavelength
    wavelength = wv_slider.get_pos()

    # Intensity slider bar creation
    int_slider = dan_gui.Slider(150, 40, 200, 25, small_font, (0, 100))
    # Setting default intensity
    intensity = int_slider.get_pos()
    # Stopping voltage slider creation
    stop_slider = dan_gui.Slider(300, 550, 200, 25, small_font, (-3, 3), 0.5, 1)
    stop_voltage = stop_slider.get_pos()
    # Dropdown menu creation
    drop = dan_gui.DropDown(90, 90, 120, 25, Metal.MetalNames, my_font)
    # Loads custom metals from the file
    drop = load_custom_metals(drop)
    # 'Create new metal' button creation
    btn = dan_gui.Button(250, 90, my_font, "Create New Metal")
    # Adding electron speed text to screen
    speed_obj = my_font.render("Average speed: 0 ms^-1", 1, (0, 0, 0))

    # Settings button
    settings_btn = dan_gui.ImageButton(730, 10, my_font, "options")

    # Adding buttons to save and load settings
    save_button = dan_gui.Button(270, 130, my_font, "Save Values")
    load_button = dan_gui.Button(270, 160, my_font, "Load Values")

    # Creating surface for transparent light texture
    surf = pygame.Surface((display_width, display_height), pygame.SRCALPHA)
    surf.set_alpha(set_light_alpha(wavelength, intensity))

    # Image for the lamp
    lamp_img = pygame.image.load("img/lamp.png")

    # Creating menu
    cnm_menu = dan_gui.Menu(200, 200, 450, 280, my_font, "Create New Metal")
    # Creating text box to add to menu
    menu_name_txt = dan_gui.Textbox(80, 5, 200, 25, my_font, ["|"], 15)
    # Tuple of values containing each letter of the alphabet
    # Used for the 'blocked characters' for a text entry box, also contains symbols
    alphabet = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
                "v", "w", "x", "y", "z", "!", "\"", "£", "$", "%", "^", "&", "*", "(", ")", "_", "-", "+", "=", "?", "\\", "|", "<", ">", "{", "}", "[", "]", "/", ",")
    # Creates a text entry box for the work function, does not allow alphabet characters
    menu_work_txt = dan_gui.Textbox(170, 40, 80, 25, my_font, alphabet, 5)
    # Creates a button to close the 'Create New Metal' menu and add the metal created
    menu_ok_button = dan_gui.Button(390, 230, my_font, "Add")
    # Creates a button to close the 'Create New Metal' menu without adding a metal
    menu_close_button = dan_gui.Button(10, 230, my_font, "Close")
    # Creating RGB elements
    r_slider = dan_gui.Slider(80, 90, 200, 25, my_font, (0, 255), 0)
    g_slider = dan_gui.Slider(80, 130, 200, 25, my_font, (0, 255), 0)
    b_slider = dan_gui.Slider(80, 170, 200, 25, my_font, (0, 255), 0)
    # Sets starting values for each slider
    r = round(r_slider.get_pos())
    g = round(g_slider.get_pos())
    b = round(b_slider.get_pos())
    # Creates a colour patch object for displaying the colour from the 3 sliders
    patch = dan_gui.ColourPatch(330, 110, 100, 100, my_font, (r, g, b))
    # Creating checkbox to allow user to choose to save the file
    checkbox = dan_gui.Checkbox(140, 200, my_font)

    # Adding menu elements to menu, for explanation, see Menu object in dan_gui.py
    # Adding textboxes to menu
    cnm_menu.add(menu_name_txt)
    cnm_menu.add(menu_work_txt)
    # Add RGB sliders
    cnm_menu.add(r_slider)
    cnm_menu.add(g_slider)
    cnm_menu.add(b_slider)
    cnm_menu.add(patch)
    # Adding buttons to menu
    cnm_menu.add(menu_ok_button)
    cnm_menu.add(menu_close_button)
    # Adding Checkbox
    cnm_menu.add(checkbox)
    # Adding text
    cnm_menu.add_text("Name: ", (5, 5))
    cnm_menu.add_text("Work Function: ", (5, 40))
    cnm_menu.add_text("x 10^-19 J", (260, 40))
    cnm_menu.add_text("Colour: ", (5, 70))
    cnm_menu.add_text("Red: ", (5, 100))
    cnm_menu.add_text("Green: ", (5, 140))
    cnm_menu.add_text("Blue: ", (5, 180))
    cnm_menu.add_text("Save to file?", (5, 200))

    # Making Settings Menu
    settings_menu = dan_gui.Menu(200, 200, 450, 250, my_font, "Settings")
    # Creating objects for settings menu
    photon_checkbox = dan_gui.Checkbox(200, 10, my_font)
    # Initialises variable to hold whether checkbox is on or off
    photon_checkbox.on = True
    photon_draw = photon_checkbox.on
    # Storage Settings Button
    store_btn = dan_gui.Button(10, 50, my_font, "Storage Settings")
    # Creating button for saving settings
    save_set_btn = dan_gui.Button(10, 200, my_font, "Save Settings")
    # Adding Elements to Settings menu
    settings_menu.add(photon_checkbox)
    settings_menu.add(store_btn)
    settings_menu.add(save_set_btn)
    # Adding text to settings menu
    settings_menu.add_text("Show Photons:", (5, 10))

    # Creates Storage Settings Menu
    store_menu = dan_gui.Menu(150, 200, 600, 250, my_font, "Storage Settings")
    # Creating objects for menu
    clear_v_btn = dan_gui.Button(10, 30, my_font, "Clear File")
    clear_c_btn = dan_gui.Button(10, 100, my_font, "Clear File")
    back_btn = dan_gui.Button(10, 160, my_font, "Back")
    # Adding objects to menu
    store_menu.add(clear_v_btn)
    store_menu.add(clear_c_btn)
    store_menu.add(back_btn)
    # Adding text to menu
    store_menu.add_text("values.dat - Holds data of saved values", (10, 10))
    store_menu.add_text("custom_metals.dat - Holds data of saved custom metals", (10, 80))

    # Last thing: load in settings
    photon_checkbox.on = load_settings()
    photon_draw = photon_checkbox.on

    # All code in this loop runs 30 times a second until the program is closed
    while not game_exit:
        # This gets all events pygame detects in one list
        events = pygame.event.get()
        # Gets the position as a pair of co-ords of the mouse in the current frame
        x, y = pygame.mouse.get_pos()

        # Updates the pointer for each of the sliders
        wv_slider.update(x)
        int_slider.update(x)
        stop_slider.update(x)
        # Checks if buttons are clicked with built in delay to prevent accidental muliple clicks
        btn.update(x, y)
        save_button.update(x, y)
        load_button.update(x, y)
        settings_btn.update(x, y)
        # Updates all elements in cnm menu - see Menu object in dan_Gui.py for explanation
        cnm_menu.update(x, y)
        # Updates colours in RGB slider base on slider position
        r = round(r_slider.get_pos())
        g = round(g_slider.get_pos())
        b = round(b_slider.get_pos())
        # Updates colour of ColourPatch
        patch.rgb = (r, g, b)
        # Updates elements in settings menu
        settings_menu.update(x, y)
        # Updates elements in storage menu
        store_menu.update(x, y)

        # Input management
        # Checks if each event in the events list matches certain types
        for event in events:
            # Checking for mouse clicked, gives position
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the drop down box is changed
                changed = drop.on_click(x, y)
                # If it has been changed then the current_metal is set to the metal selected by the drop down box
                if changed:
                    name = drop.data[drop.current_opt]
                    current_metal = find_metal(name)
                # Passes mouse co-ords onto sliders when click registered
                wv_slider.on_click(x, y)
                int_slider.on_click(x, y)
                stop_slider.on_click(x, y)
                # passes mouse co-ords onto buttons when clicked
                btn.on_click(x, y)
                save_button.on_click(x, y)
                load_button.on_click(x, y)
                settings_btn.on_click(x, y)
                # Checks clicks in the menus if open
                if cnm_menu.visible:
                    cnm_menu.on_click(x, y)
                elif settings_menu.visible:
                    settings_menu.on_click(x, y)
                elif store_menu.visible:
                    store_menu.on_click(x, y)

            # Checking for mouse unclicked
            if event.type == pygame.MOUSEBUTTONUP:
                # Triggers the sliders' methods for when a mouse is unclicked
                wv_slider.on_unclick()
                int_slider.on_unclick()
                stop_slider.on_unclick()
                # When unclicked, triggers methods in buttons and menus
                btn.on_unclick()
                save_button.on_unclick()
                load_button.on_unclick()
                cnm_menu.on_unclick()
                settings_btn.on_unclick()
                settings_menu.on_unclick()
                store_menu.on_unclick()

            # Checking for any keyboard key being pressed
            if event.type == pygame.KEYDOWN:
                # If the menu is visible, trigger appropriate method in menu
                if cnm_menu.visible:
                    cnm_menu.on_char_typed(event.key)

            # Checking for key being unpressed
            if event.type == pygame.KEYUP:
                # If the menu is visible, trigger appropriate method in menu
                if cnm_menu.visible:
                    cnm_menu.on_key_up(event.key)
                
            # Checking for exit, in event of exit event, the game closes and the loop stops
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                game_exit = True

        # Checking if each button has been clicked

        # Checks if open menu button has been clicked
        # Opens 'Create new Metal' menu if no other open menus
        if btn.clicked and not settings_menu.visible:
            cnm_menu.visible = True
        # Checks if settings menu button has been clicked
        # Opens Settings menu if no other open menus
        if settings_btn.clicked and not cnm_menu.visible:
            settings_menu.visible = True

        # Checks if add metal menu button is pressed and text boxes are filled in
        if menu_ok_button.clicked and menu_name_txt.text != "" and menu_work_txt != "":
            # Closes 'Create New Metal' menu
            cnm_menu.visible = False
            # Creates a new Metal object and adds to drop-down box
            new_metal = Metal(menu_name_txt.text, get_float_from_string(menu_work_txt.text) * math.pow(10, -19), colour)
            drop = add_new_metal(new_metal, drop)
            # If user chose to save the metal to a file
            if checkbox.on:
                # Opens the file and tells user if it can't
                try:
                    f = open("data/custom_metals.dat", "ab")
                    # Serialises the metal object and writes it to the file
                    pickle.dump(new_metal, f)
                    # Closes the file to prevent unneeded memory use
                    f.close()
                except FileNotFoundError:
                    print("Cannot open data/custom_metals.dat")
            # Resets the text entry boxes to be empty
            menu_name_txt.text = ""
            menu_work_txt.text = ""

        # Checks if close menu button has been pressed, closes menu and resets text fields
        if menu_close_button.clicked:
            cnm_menu.visible = False
            menu_name_txt.text = ""
            menu_work_txt.text = ""

        # Checks if save values button is pressed
        if save_button.clicked:
            # Tries to open the values file, if it can't, tells the user
            try:
                f = open("data/values.dat", "wb")
                pickle.dump(wv_slider.pointer, f)
                pickle.dump(int_slider.pointer, f)
                pickle.dump(drop.current_opt, f)
                f.close()
            except FileNotFoundError:
                print("Cannot open data/value.dat")

        # Checks if load settings button is pressed
        if load_button.clicked:
            # Tries to open values file, tells user if can;t
            try:
                f = open("data/values.dat", "rb")
                try:
                    # Sets slider values to deserialised values from file
                    wv_slider.pointer = pickle.load(f)
                    int_slider.pointer = pickle.load(f)
                    # Tries to set current option of the drop-down box
                    # Will default to first option if fails to load
                    try:
                        drop.current_opt = pickle.load(f)
                        drop.change_text(drop.data[drop.current_opt])
                    except IndexError:
                        drop.current_opt = 0
                        drop.change_text(drop.data[drop.current_opt])
                    # Updates current_metal to the metal loaded from file
                    current_metal = find_metal(drop.data[drop.current_opt])
                except(EOFError, pickle.UnpicklingError):
                    pass
                # Closes file once done to prevent unnecessary memory usage
                f.close()
            except FileNotFoundError:
                print("Cannot open values.dat")

        # Checks if the 'save settings' button (from settings menu) has been pressed
        if save_set_btn.clicked:
            # Try to open settings file, if can't, tell user
            try:
                f = open("data/settings.dat", "wb")
                # Serialises boolean value of whether checkbox is on
                pickle.dump(photon_checkbox.on, f)
                # Closes file to prevent unnecessary memory usage
                f.close()
            except FileNotFoundError:
                print("Cannot load settings.dat")
            # Closes settings menu
            settings_menu.visible = False

        # Checks if 'Open storage menu' button (in settings menu) is clicked
        if store_btn.clicked:
            # Closes settings menu
            settings_menu.visible = False
            # Opens storage menu
            store_menu.visible = True

        # Checks if the button for clearing the 'values.dat' file is clicked
        if clear_v_btn.clicked:
            # Opens the values file
            with open("data/values.dat", "wb") as f:
                # Deletes contents of the file
                delete_file(f)
            # Greys out the button to prevent being used again
            clear_v_btn.grey = True

        # Checks if the button for clearing the 'custom_metals.dat' file is clicked
        if clear_c_btn.clicked:
            # Opens custom metals file
            with open("data/custom_metals.dat", "wb") as f:
                # Deletes the contents of the file
                delete_file(f)
            # Greys out the button prevent being used again
            clear_c_btn.grey = True

        # If the back button (in the storage menu) is clicked
        if back_btn.clicked:
            # Opens the settings menu
            settings_menu.visible = True
            # Closes the storage menu
            store_menu.visible = False
        
        # Updates rgb values for colour patch on cnm Menu if its open
        if cnm_menu.visible:
            colour = (r, g, b)
        # Updates the boolean for whether protons should be drawn if settings menu is open
        elif settings_menu.visible:
            photon_draw = photon_checkbox.on

        # ALL CALCULATIONS BELOW HERE
        # Gets the wavelength from the slider
        wavelength = wv_slider.get_pos()
        # Multiplies it to be the correct order of magnitude (nanometres)
        wavelength = wavelength * math.pow(10, -9)
        # Gets RGB values for light according to wavelength
        r, g, b = set_light_colour(wavelength)

        # Sets the intensity to the 2nd slider's value
        intensity = int_slider.get_pos()

        # Gets stopping voltage
        stop_voltage = stop_slider.get_pos()

        # Emits a photon if needed
        emit_photon(current_metal, intensity, wavelength)

        # Draws white over previous frame
        screen.fill(white)
        # ALL DRAWING BELOW HERE
        # For every photon in the PhotonList
        for photon in Photon.PhotonList:
            # Moves the photon's x and y co-ords
            photon.move()
            # #Draws the photon if the setting for drawing photons is enabled
            if photon_draw:
                photon.draw(screen)
            # Checks if photon has hit left metal plate
            photon.check_collision(left_rect.rect, stop_voltage)

        # Draw Electrons and calculate their average speed using their kinetic energy
        total_ke = 0
        for electron in Electron.ElectronList:
            # Adds each electron's kinetic energy to the total
            total_ke += electron.kinEnergy
            electron.move()
            electron.draw(screen)
            electron.check_pos(right_rect.rect)
        # If the ElectronList is not empty
        if len(Electron.ElectronList) > 0:
            # Calculates average kinetic energy of all electrons
            average_ke = total_ke / len(Electron.ElectronList)
            # Converts kinetic energy to speed
            speed = round(math.sqrt((2*average_ke)/Electron.Mass))
            # Creates a pygame Text object for rendering the speed
            speed_obj = small_font.render(("Average Speed: " + str(speed) + " ms^-1"), 1, black)

        # Draws background for wavelength, intensity and current metal selectors
        pygame.draw.rect(screen, lightGrey, (0, 0, 450, 200))
        # Draws border around bottom and right sides of box
        pygame.draw.lines(screen, black, False, ((0, 200), (450, 200), (450, 0)), 2)
        # Drawing average speed
        screen.blit(speed_obj, (5, 150))
        # Left rectangle
        left_rect.draw(screen, current_metal.colour)
        # Right rectangle
        right_rect.draw(screen, grey)
        # Wavelength slider prompt
        screen.blit(wave_txt, (5, 5))
        # Wavelength slider
        wv_slider.draw(screen)
        # Wavelength slider suffix
        screen.blit(wave_txt2, (400, 5))
        # Intensity slider prompt
        screen.blit(intensity_txt, (5, 40))
        # Intensity slider suffix
        screen.blit(intensity_txt2, (400, 40))
        # Draw intensity slider
        int_slider.draw(screen)
        # Stopping voltage slider
        stop_slider.draw(screen)
        # Stopping voltage slider prompt
        screen.blit(stop_txt, (100, 550))
        # Stopping voltage slider suffix
        screen.blit(stop_txt2, (540, 550))
        # Metal Text
        screen.blit(metal_txt, (5, 90))
        # Drop down box
        drop.draw(screen)
        # Draw button that opens 'Create new metal' menu
        btn.draw(screen)
        # Draws save and load buttons to screen
        save_button.draw(screen)
        load_button.draw(screen)
        # Draw settings button
        settings_btn.draw(screen)

        # Draws light from lamp to screen
        # Gets alpha (transparency) value for light
        alpha = set_light_alpha(wavelength, intensity)
        # Combines colour with alpha in 1 tuple
        light_colour = (r, g, b, alpha)
        # Draws light to transparency enabled surface
        pygame.draw.polygon(surf, light_colour, ((60, 400), (60, 550), (700, 380), (512, 202)))
        # Draws transparent surface to screen
        screen.blit(surf, (0, 0))
        # Draws lamp image
        screen.blit(lamp_img, (500, 150))

        # Draws menus
        cnm_menu.draw(screen)
        settings_menu.draw(screen)
        store_menu.draw(screen)

        # Updates the display
        pygame.display.update()

        # Makes the program wait so that the main loop only runs 30 times a second
        clock.tick(30)


# Calls the main loop subroutine to start
if __name__ == "__main__":
    game_loop()
