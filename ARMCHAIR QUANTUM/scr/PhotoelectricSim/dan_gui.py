# dan_gui.py is a GUI library I have developed for use in the program
import pygame
import math

# RGB colour definitions for referring to later
black = (0, 0, 0)
white = (255, 255, 255)
grey = (100, 100, 100)
darkGrey = (50, 50, 50)
light_grey = (130, 130, 130)


# Base/parent class used for all other classes
# Should be treated as abstract - there should never be an Element object, only objects that are children of Element
class Element:

    # x, y = the x and y position of the top left of the element in pixels
    # width, height = width + height of the element in pixels
    # font = The Pygame Font object used for rendering text
    # bg_colour = The colour of background parts of the element as an RGB tuple
    # text_colour = The colour of text of the element as an RGB tuple
    def __init__(self, x, y, width, height, font, back_colour=grey, text_colour=black):
        # x and y can be a decimal value as these are not the values used in drawing
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # Pygame Rect object that covers the entire object, used for collision detection with mouse
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # x2 and y2 are the co-ords for the bottom right of the element
        self.x2 = self.x + self.width
        self.y2 = self.y + self.height
        self.font = font
        self.bg_colour = back_colour
        self.text_colour = text_colour

    @property
    def bg_colour(self):
        return self._bg_colour

    # Validation check before setting background colour to new value
    # Prevents crash due to invalid colour where one element is greater than 255 or less than 0
    @bg_colour.setter
    def bg_colour(self, new_colour):
        valid = True
        for n in new_colour:
            if n > 255 or n < 0:
                valid = False
        if valid:
            self._bg_colour = new_colour

    # Default methods, child classes override the ones they need
    # Uses 'pass' keyword: method does nothing

    # Default draw method
    # Parameter screen is a Pygame surface object that will be drawn to
    def draw(self, screen):
        pass

    # Method that deals with clicking input, takes in the mouse position as 2 co-ords
    def on_click(self, mouse_x, mouse_y):
        pass

    # Method that deals with mouse button being released
    def on_unclick(self):
        pass

    # Method that deals with a keyboard key being pressed
    # Takes in the pygame key code as a parameter
    def on_char_typed(self, key_pressed):
        pass

    # Method that deals with a keyboard key being released
    # Takes in the pygame key code as a parameter
    def on_key_up(self, key_up):
        pass

    # Method for things that should be run once a frame
    # Takes in the mouse pos as 2 co-ords as parameters
    def update(self, mouse_x, mouse_y):
        pass

    # Method that is called when an Element object is added to a Menu or Group object
    # For explanation, see methods where overriden
    def on_menu_add(self):
        pass


# Class for a drop-down list that displays a list of pre-defined options
# Inherits all methods and attributes from Element
class DropDown(Element):

    # Static constant for how wide the button at the side of the list should be
    buttonWidth = 30

    # data = A list of possible options - strings
    # font = The pygame Font object used to render text
    def __init__(self, x, y, width, height, data, font):
        # Calls its parent's init method to get all parent attributes
        Element.__init__(self, x, y, width, height, font)
        self.bg_colour = light_grey
        self.data = data
        self.current_opt = 0
        self.button_text = self.font.render(self.data[self.current_opt], 1, black)
        # Make text objects for all data objects
        self.options = data
        # Open is a boolean that tracks whether the list should be drawn
        self.open = False
        # Pygame Rect object that covers the button
        self.button_rect = pygame.Rect(self.x2, self.y, DropDown.buttonWidth, self.height)
        # Pygame Rect object that covers the menu
        self.menu_rect = pygame.Rect(self.x, self.y2, self.width, self.height*len(self.data))

    def on_menu_add(self):
        self.button_rect = pygame.Rect(self.x2, self.y, DropDown.buttonWidth, self.height)
        self.menu_rect = pygame.Rect(self.x, self.y2, self.width, self.height*len(self.data))

    def on_click(self, mouse_x, mouse_y):
        # Returns true if an option changed
        changed = False
        # Checks if the menu is open
        if self.open:
            # Checks if clicking button
            if self.button_rect.collidepoint(mouse_x, mouse_y):
                # Closes the drop down menu
                self.open = False
            # If clicking the menu, select the option they clicked on, then close the menu
            if self.menu_rect.collidepoint(mouse_x, mouse_y):
                self.select_option(mouse_y)
                self.open = False
                # Option has been changed
                changed = True
        else:
            # Checks if clicking button
            if self.button_rect.collidepoint(mouse_x, mouse_y):
                # Open the drop down menu
                self.open = True
        return changed

    # Using property modifier for getter and setter
    @property
    def options(self):
        return self.__options

    # Uses setter to make sure when options change, text objects are automatically created
    # Takes in a list of strings as a parameter
    @options.setter
    def options(self, data):
        options = []
        # For each string in data, make a text object from it
        for i in range(len(data)):
            text = self.font.render(data[i], 1, black)
            options.append(text)
        self.__options = options
        # Recreates the collision Rect object to account for longer menu box
        self.menu_rect = pygame.Rect(self.x, self.y2, self.width, self.height * (len(self.data)))

    # Takes in the y co-ord of the mouse
    # Subtracts from the y co-ord so the top of the first option box is at 0
    # Divides by the height of each option box then rounds it down
    def select_option(self, mouse_y):
        self.current_opt = math.floor((mouse_y - self.y - self.height) / self.height)
        # Changes the button text to the currently selected option
        self.change_text(self.data[self.current_opt])

    # Changes the text in the button to string new_text
    def change_text(self, new_text):
        self.button_text = self.font.render(new_text, 1, black)

    # Draws the drop-down box
    def draw(self, screen):
        # Draws the background of the box
        pygame.draw.rect(screen, self.bg_colour, (self.x, self.y, self.width, self.height))
        # Draws the background for the button next to the box
        pygame.draw.rect(screen, darkGrey, ((self.x + self.width), self.y, DropDown.buttonWidth, self.height))
        # Draws the triangle inside the button
        pygame.draw.polygon(screen, black, (((self.x + self.width + (DropDown.buttonWidth / 2)),
                                             (self.y + self.height - 3)), ((self.x + self.width + 3), (self.y + 3)),
                                            ((self.x2 + DropDown.buttonWidth - 3), (self.y + 3))))
        # Draw text in box
        screen.blit(self.button_text, (self.x + 2, self.y + 2))
        # Draw border around box
        pygame.draw.lines(screen, black, True, ((self.x, self.y), (self.x2, self.y), (self.x2, self.y2), (self.x, self.y2)))
        # Displays whole list if open
        if self.open:
            # For each option available, draw a box with text in
            for i in range(len(self.data)):
                current_y = self.y + ((i+1)*self.height)
                # Render a box
                pygame.draw.rect(screen, self.bg_colour, (self.x, current_y, self.width, self.height))
                # Render the text
                screen.blit(self.options[i], (self.x + 2, current_y + 2))


# Class for a button with a text label
# Inherits all methods and attributes from Element
class Button(Element):

    # text = The text rendered as the button's label
    def __init__(self, x, y, font, text):
        self.text = text
        # Width and Height are generated based on the width and height of the text
        self.width = font.size(text)[0] + 5
        self.height = font.size(text)[1] + 5
        Element.__init__(self, x, y, self.width, self.height, font)
        self.bg_colour = light_grey
        # Makes a text object of the label text
        self.txt_obj = self.font.render(self.text, 1, self.text_colour)
        # Clicked is a boolean value which is true when the user has clicked on the button
        self.clicked = False
        # The number of frames since the button was last clicked
        self.last_click = 0
        # The width of the black border around the button in pixels
        self.border = 1
        # When this is true, the button appears greyed out and cannot be clicked
        self.grey = False

    # Using getters and setters for attribute 'grey'
    @property
    def grey(self):
        return self._grey

    # Sets grey_change to true when grey has been changed
    # The part of update that deals with colour should only be run once, not on every update
    @grey.setter
    def grey(self, new_grey):
        self._grey = new_grey
        self.update_grey()

    # When mouse button released, clicked = false
    def on_unclick(self):
        self.clicked = False

    # When mouse clicked, checks if mouse is inside button
    # Checks if button has not been pressed in last 20 frames
    # Checks if button is not greyed out
    # If all True, button is clicked and last_click set to 20
    def on_click(self, mouse_x, mouse_y):
        if self.rect.collidepoint(mouse_x, mouse_y)and self.last_click == 0 and not self.grey:
            self.clicked = True
            self.last_click = 20

    # Called every frame, checks if mouse is inside button but doesn't need to be clicked
    def on_hover(self, mouse_x, mouse_y):
        # If in button, make border thicker and make background slightly lighter
        if self.rect.collidepoint(mouse_x, mouse_y) and not self.grey:
            self.border = 2
            self.bg_colour = (100, 100, 100)
        # If not in button, set border and colour back to normal
        else:
            self.border = 1
            self.bg_colour = light_grey

    # Called every second
    def update(self, mouse_x, mouse_y):
        # Runs method to check if mouse is inside button
        self.on_hover(mouse_x, mouse_y)
        # If button has not been clicked in that frame, decrement button counter and set clicked to false
        if self.last_click != 0:
            self.last_click -= 1
            self.clicked = False

    def update_grey(self):
        # If the button is greyed out, make background colour darker
        if self.grey:
            self.bg_colour = (150, 150, 150)
            # Try to make text colour darker
            # Uses try statement because Button is parent class of ImageButton
            # ImageButton has no text attribute
            try:
                self.text_colour = darkGrey
                self.txt_obj = self.font.render(self.text, 1, self.text_colour)
            except AttributeError:
                pass
        # If not grey, set background colour and text colour to normal
        else:
            self.bg_colour = light_grey
            try:
                self.text_colour = black
                self.txt_obj = self.font.render(self.text, 1, self.text_colour)
            except AttributeError:
                pass
        
    def draw(self, screen):
        # Draws the background rectangle of the button
        pygame.draw.rect(screen, self.bg_colour, (self.x, self.y, self.width, self.height))
        # Draws the button text
        screen.blit(self.txt_obj, (self.x + 3, self.y + 3))
        # Draws the border
        pygame.draw.lines(screen, black, True, ((self.x, self.y), (self.x, self.y2), (self.x2, self.y2),
                                                    (self.x2, self.y)), self.border)


# Child of the button class but displays an image instead of a text label
# Inherits all methods and attributes from Button which also inherits from Element
class ImageButton(Button):

    # Takes in a filepath to an image instead of text label
    def __init__(self, x, y, font, filepath):
        # Tries to open the image specified by 'filepath' in the /img folder
        # The root of the /img folder is the folder where this .py file is
        try:
            self.image = pygame.image.load("img/" + filepath + ".png")
        # Validation: Tell user if image cannot be found
        except FileNotFoundError:
            print("Could not find file at img/" + filepath + ".png")
        # Get width and height of image
        size = self.image.get_rect().size
        # Dimensions of button is dimensions of image with 10 pixels of padding in each direction
        self.width = size[0] + 10
        self.height = size[1] + 10
        Element.__init__(self, x, y, self.width, self.height, font)
        self.border = 1
        self.clicked = False
        self.last_click = 0
        self.grey = False

    def draw(self, screen):
        # Draw the background
        pygame.draw.rect(screen, self.bg_colour, (self.x, self.y, self.width, self.height))
        # Draw the image
        screen.blit(self.image, (self.x + 5, self.y + 5))
        # Draw the borders
        pygame.draw.lines(screen, black, True, ((self.x, self.y), (self.x, self.y2), (self.x2, self.y2),
                                                    (self.x2, self.y)), self.border)


# Class for a slider that has a small triangle that moves along a bar when clicked and dragged
# The output is always between 2 limits, given by parameter limits, a tuple of length 2
# Lower limit is limit[0], upper limit is limit[1]
# starting_pos determines how far along the line the pointer starts where 0 is fully left
# 1 is fully right and 0.5 is halfway. Defaults to 0.5
# dec_points - how many decimal points the text should render, defaults to 0 (integers only)
# Inherits all methods and attributes from Element
class Slider(Element):

    # Limits = the lowest and highest points given as a tuple
    # StartingPos = how far along the bar the pointer is at when program starts
    def __init__(self, x, y, width, height, font, limits, starting_pos=.5, dec_points = 0):
        Element.__init__(self, x, y, width, height, font)
        self.limits = limits
        # line_y = The y value at which the line starts
        self.line_y = self.y + (self.height * 0.8)
        self.starting_pos = starting_pos
        self.dec_points = dec_points
        # 'pointer' is the raw pixel position of the x co-ord of the middle of the triangular pointer
        self.pointer = self.x + (self.width * self.starting_pos)
        # Value is the output of the slider
        self.value = self.get_pos()
        # txt is the text object that renders the value of the slider
        self.txt = self.update_txt()
        # true when the slider itself is clicked
        self.clicked = False
        # true when the pointer is clicked
        self.tri_clicked = False
        # Pygame Rect object for the triangle pointer
        self.tri_rect = pygame.Rect(self.pointer - 10, self.y + 2, 20, (self.line_y - 2) - (self.y + 2))

    # Called when a slider object is added to a Menu object
    # Updates all x and y positions of the triangle and text
    def on_menu_add(self):
        self.line_y = self.y + (self.height * 0.8)
        self.pointer = self.x + (self.width * self.starting_pos)
        self.value = self.get_pos()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.tri_rect = pygame.Rect(self.pointer - 10, self.y + 2, 20, (self.line_y - 2) - (self.y + 2))
        self.update_txt()

    # Given the raw pointer position relative to the top left corner of the screen
    # Gets the value from the slider and returns it
    def get_pos(self):
        # Gets the proportion of slider to left of pointer
        # Eg. if 10% of slider to left of pointer, result is 0.1
        pos = (self.pointer - self.x) / self.width
        # Multiplies proportion by the difference between the limits
        # This gives a proportional value of how far the pointer is from the left limit
        pos = pos * (self.limits[1] - self.limits[0])
        # Adds the lower limit
        pos += self.limits[0]
        return pos

    # Updates the text object of the value above the pointer
    def update_txt(self):
        if self.dec_points == 0:
            txt = self.font.render(str(round(self.value)), 1, black)
        else:
            txt = self.font.render(str(round(self.value, self.dec_points)), 1, black)
        return txt

    def draw(self, screen):
        # Draws bottom line
        pygame.draw.rect(screen, black, (self.x, self.line_y, self.width, self.y2 - self.line_y))
        # Draws triangular pointer 2 pixels above the line
        pygame.draw.polygon(screen, black, ((self.pointer, self.line_y - 2), (self.pointer - 10, self.y + 2),
                                                (self.pointer + 10, self.y + 2)))
        # Draws value above pointer
        self.value = self.get_pos()
        self.txt = self.update_txt()
        screen.blit(self.txt, (self.pointer + 12, self.y))

    # If clicked and is in bounds of the triangle, clicked = True
    def on_click(self, mouse_x, mouse_y):
        if self.tri_rect.collidepoint(mouse_x, mouse_y):
            self.tri_clicked = True
        elif self.rect.collidepoint(mouse_x, mouse_y):
            self.clicked = True

    # sets clicked booleans to false when mouse button released
    def on_unclick(self):
        self.tri_clicked = False
        self.clicked = False

    # Run every frame. Only needs x co-ord of mouse
    # Requires both co-ords but sets y to None as default to allow overriding of method of same name in Element
    def update(self, mouse_x, mouse_y=None):
        if self.tri_clicked or self.clicked:
            # If mouse x co-ord further than upper boundary
            if mouse_x > self.x2:
                # Pointer = upper boundary
                self.pointer = self.x2
            # If mouse x co-ord further than lower boundary
            elif mouse_x < self.x:
                # Pointer = lower boundary
                self.pointer = self.x
            # Otherwise, mouse x co-ord is between the 2 boundaries
            # pointer = mouse x co-ord
            else:
                self.pointer = mouse_x
            self.tri_rect = pygame.Rect(self.pointer - 10, self.y + 2, 20, (self.line_y - 2) - (self.y + 2))


# Class for a text entry box
# Inherits all methods and attributes from Element
class Textbox(Element):

    # Static tuple of pygame character codes that have a different key_name than a letter
    # Eg. key_name of the g key is g, therefore not included in tuple
    special_chars = ("space", "escape", "left ctrl", "right ctrl", "return", "left alt", "right alt", "caps lock",
                     "numlock", "scroll lock", "tab", "left super", "right super", "menu", "f1", "f2", "f3", "f4", "f5",
                     "f6", "f7", "f8", "f9", "f10", "f11", "f12", "insert", "home", "delete", "end", "page up",
                     "page down", "pause")
    # Dictionary of the keys that have different characters when shift is pressed with them
    # and the corresponding characters
    shifts = {"1": "!", "2": "\"", "3": "£", "4": "$", "5": "%", "6": "^", "7": "&", "8": "*", "9": "(", "0": ")",
              "-": "_", "=": "+", "#": "~", "[": "{", "]": "}", ";": ":", "'": "@", ",": "<", ".": ">", "/": "?",
              "\\": "|"}
    # Just gets the keys from the shifts dictionary
    # tuple of numbers 0 - 9
    shift_keys = shifts.keys()
    # Static variable that holds the total number of text boxes in the program
    # Used in checking which text box is in focus
    # A text box must be in focus in order to register keyboard input
    TextBoxes = 0
    
    # blocked_chars = the characters the box will not accept
    # char_limit = the maximum number of characters allowed in the textbox
    def __init__(self, x, y, width, height, font, blocked_chars, char_limit = None):
        Element.__init__(self, x, y, width, height, font)
        self.blocked_chars = blocked_chars
        self.charLimit = char_limit
        # text is a string that holds the characters input to the text box
        self.text = ""
        # txt_obj is a text object used for rendering the input
        self.txt_obj = font.render(self.text, 1, black)
        self.update_text()
        # Adds one to the count of text boxes
        Textbox.TextBoxes += 1
        # By default is not in focus
        self.is_focused = False
        # If it is the only text box, automatically in focus
        if Textbox.TextBoxes < 2:
            self.is_focused = True
        # Boolean value of whether the shift key is held down
        self.shift_pressed = False

    # If the user clicks on the text box, it is in focus
    # If the user hasn't clicked on the text box, defocuses it to prevent multiple text boxes in focus at one time
    def on_click(self, mouse_x, mouse_y):
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.is_focused = True
        else:
            self.is_focused = False

    # Called every time a key is pressed
    def on_char_typed(self, key_pressed):
        # Only runs the code if the textbox is in focus
        if self.is_focused:
            # Special case for backspace, removes the last letter of the string
            if key_pressed == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            # Checks if shift key is pressed
            elif key_pressed == pygame.K_LSHIFT or key_pressed == pygame.K_RSHIFT:
                self.shift_pressed = True
            # Checks the character limit has not been reached
            elif len(self.text) < self.charLimit:
                # is_allowed is True by default, if the key input is a blocked char, it become false
                is_allowed = True
                # is_special is False by default
                # If key input is a special character (from special_chars list) then it is True
                is_special = False
                # key_name gets the name of the corresponding pygame key code
                # for alphanumeric characters, is the same as the character itself
                key_name = pygame.key.name(key_pressed)
                # Checking if character is blocked
                for c in self.blocked_chars:
                    if key_name == c:
                        is_allowed = False
                        break
                # Checking if character is special
                for s in Textbox.special_chars:
                    if key_name == s:
                        is_special = True
                        break
                # If the character is allowed and isn't a special character, it can be added normally
                if is_allowed and not is_special:
                    # If the shift key is being held down
                    if self.shift_pressed:
                        # is_shift_key is False by default but becomes true if
                        # the key being pressed is the shift_keys list
                        is_shift_key = False
                        # Checks through the shift_keys list for the key being pressed
                        for k in Textbox.shift_keys:
                            if key_name == k:
                                is_shift_key = True
                        # If the key is in shift_key, use that key's shift equivalent
                        # Add it to the text string
                        if is_shift_key:
                            self.text = self.text + Textbox.shifts[key_name]
                        # If not in shift_keys, just add the uppercase equivalent of the letter typed
                        else:
                            self.text = self.text + key_name.upper()
                    # If shift key not pressed, just add the character typed to text
                    else:
                        self.text = self.text + key_name
                # If it's an allowed character and is a special character
                # Special cases are dealt with here
                elif is_allowed and is_special:
                    # Key name of the space bar is not ' ', must be manually checked for
                    if key_pressed == pygame.K_SPACE:
                        self.text = self.text + " "
            # Updates the text object being drawn to the screen
            self.update_text()

    # Called every time a key is released
    def on_key_up(self, key_up):
        # Checks if shift is unpressed
        if key_up == pygame.K_RSHIFT or key_up == pygame.K_LSHIFT:
            self.shift_pressed = False

    def draw(self, screen):
        # Draws white background box
        pygame.draw.rect(screen, white, (self.x, self.y, self.width, self.height))
        # Draws outline if focused
        if self.is_focused:
            pygame.draw.lines(screen, black, True, ((self.x, self.y), (self.x + self.width, self.y),
                                                        (self.x + self.width, self.y + self.height),
                                                        (self.x, self.y + self.height)), 2)
        # Draws text if not empty
        if self.text != "":
            screen.blit(self.txt_obj, (self.x + 2, self.y + 2))

    # Called when the text in the text box is updated, recreates the text object
    def update_text(self):
            self.txt_obj = self.font.render(self.text, 1, black)

    @property
    def text(self):
        return self._text

    # Method for externally setting the text in the text box
    # changes text to the parameter new_text then updates the text object
    @text.setter
    def text(self, new_text):
        self._text = new_text
        self.update_text()


# Colour patch draws a rectangle of a specific colour on the screen
# Useful for showing output of RGB selectors
# Inherits all methods and attributes from Element
class ColourPatch(Element):

    # rgb - A tuple of 3 integers between 0 and 255 to represent a 24 bit colour
    def __init__(self, x, y, width, height, font, rgb):
        Element.__init__(self, x, y, width, height, font)
        self.rgb = rgb

    @property
    def rgb(self):
        return self._rgb

    # Setter method acts as validation to make sure an RGB colour does not contain numbers outside of 0-255
    @rgb.setter
    def rgb(self, new_rgb):
        valid = True
        for num in new_rgb:
            if num > 255 or num < 0:
                valid = False
        if valid:
            self._rgb = new_rgb
        else:
            print("RGB colour must be between 0 and 255")
    
    def draw(self, screen):
        # Draws the colour
        pygame.draw.rect(screen, self.rgb, (self.x, self.y, self.width, self.height))
        # Draws a border
        pygame.draw.lines(screen, black, True, ((self.x, self.y), (self.x2, self.y), (self.x2, self.y2),
                                                    (self.x, self.y2)))


# A Group is a list of Elements that can be addressed all at once
# Inherits all methods and attributes from Element
# Uses a list to contain all elements contained within it
# Rather than calling the update method of every element in the list,
# you can just call the update method of the group, which calls them all
# as all Element objects have an update method
class Group(Element):

    def __init__(self, x, y, width, height, font):
        Element.__init__(self, x, y, width, height, font)
        # visible - whether to draw the elements or not
        self.visible = False
        # The list of elements
        # Any object that inherits from the Element class can be added
        # The elements in the list are associated with the Menu object but are not deleted if the menu is deleted
        self.elements = []
        # texts is a two-dimensional list that stores pygame text objects
        # and the co-ords where each object should be drawn
        self.texts = [[], []]

    # Adds an element (any object that inherits the Element class) to the group
    def add(self, element):
        try:
            # Adds the x and y co-ords of the group to the element's co-ord
            element.x += self.x
            element.y += self.y
            element.x2 += self.x
            element.y2 += self.y
            element.rect.move_ip(self.x, self.y)
            # Run method that allows objects to do things specific to them when added
            element.on_menu_add()
            # Add object to elements list
            self.elements.append(element)
        except AttributeError:
            print("Error: Tried adding a non-element object to a group")

    # Adds text to render in the group, takes 2 parameters
    # text - the text to be added, in string form
    def add_text(self, text, coords):
        self.texts[0].append(self.font.render(text, 1, (255, 0, 0)))
        self.texts[1].append((coords[0] + self.x, coords[1] + self.y))

    def draw(self, screen):
        if self.visible:
            # Draws each element in the group by calling its draw method
            for element in self.elements:
                element.draw(screen)
            # Draws each text object in the group to the screen
            for i in range(len(self.texts[0])):
                screen.blit(self.texts[0][i], self.texts[1][i])

    def on_click(self, mouse_x, mouse_y):
        # Runs each element's on_click method
        for element in self.elements:
            element.on_click(mouse_x, mouse_y)

    def on_unclick(self):
        # Runs each element's on_unclick method
        for element in self.elements:
            element.on_unclick()

    def on_char_typed(self, key_pressed):
        # Runs each element's on_char_typed method
        for element in self.elements:
            element.on_char_typed(key_pressed)

    def on_key_up(self, key_up):
        for element in self.elements:
            element.on_key_up(key_up)

    def update(self, mouse_x, mouse_y):
        for element in self.elements:
            element.update(mouse_x, mouse_y)


# Child of the Group class
# Inherits all methods and attributes from Group and therefore from Element
# Use of polymorphism: uses same methods as parent Group
# Functions exactly like a group but looks like a menu
# Has background and a top bar similar to a normal window
class Menu(Group):

    # title is a string that is drawn on the top bar
    # optional parameter bar_height sets the height of the top bar
    def __init__(self, x, y, width, height, font, title, bar_height=25):
        Group.__init__(self, x, y, width, height, font)
        self.title = title
        self.bar_height = bar_height
        self.total_height = self.height + self.bar_height
        # y3 is the y co-ord where the main part of the menu starts and the top bar ends
        self.y3 = self.y + self.bar_height
        # Creates a pygame text object for the title
        self.txt = self.font.render(title, 1, black)

    # Adds an element (any object that inherits the Element class) to the menu
    # Overrides Group add method to factor in height of menu bar
    def add(self, element):
        try:
            # Adds the x and y co-ords to the element's co-ord so it appears on the menu
            element.x += self.x
            element.y += (self.y + self.bar_height)
            element.x2 += self.x
            element.y2 += (self.y + self.bar_height)
            element.rect.move_ip(self.x, self.y + self.bar_height)
            # Run method that allows objects to do things when added to a Group or menu
            element.on_menu_add()
            # Add to the elements list
            self.elements.append(element)
        except AttributeError:
            print("Error: Adding a non-element object")

    # Adds text to render in the menu
    # Overrides Group addText method to factor in height of menu bar
    def add_text(self, text, coords):
        self.texts[0].append(self.font.render(text, 1, black))
        self.texts[1].append((coords[0] + self.x, coords[1] + self.y + self.bar_height))

    def draw(self, screen):
        if self.visible:
            # Draw top bar of menu
            pygame.draw.rect(screen, (80, 80, 80), (self.x, self.y, self.width, self.bar_height))
            # Draw title on top bar
            screen.blit(self.txt, (self.x+2, self.y+2))
            # Draw bg of menu
            pygame.draw.rect(screen, (120, 120, 120), (self.x, self.y3, self.width, self.height))
            # Draw border of menu
            pygame.draw.lines(screen, black, True, ((self.x, self.y), (self.x, self.y2 + self.bar_height),
                                                        (self.x2, self.y2 + self.bar_height), (self.x2, self.y)))
            pygame.draw.line(screen, black, (self.x, self.y3), (self.x2, self.y3))
            # Draws each element in the group by calling its draw method
            for element in self.elements:
                element.draw(screen)
            # Draws each text object in the group to the screen
            for i in range(len(self.texts[0])):
                screen.blit(self.texts[0][i], self.texts[1][i])


# Checkbox is a small box which when clicked will toggle between an 'on' and 'off' state
# Inherits all methods and attributes from Element
class Checkbox(Element):

    # Width and height are both set to 22 by default though can be changed
    # off_img and on_img are the images used for the off state and on state respectively
    def __init__(self, x, y, font, width=22, height=22, off_img="dan_gui/checkboxOff", on_img="dan_gui/checkboxOn"):
        Element.__init__(self, x, y, width, height, font)
        self.offImg = pygame.image.load("img/" + off_img + ".png")
        self.onImg = pygame.image.load("img/" + on_img + ".png")
        # Checkbox is off by default
        self.on = False

    def draw(self, screen):
        # Draw background rectangle
        pygame.draw.rect(screen, self.bg_colour, (self.x, self.y, self.width, self.height))
        # Draw border
        pygame.draw.lines(screen, black, True, ((self.x, self.y), (self.x, self.y2), (self.x2, self.y2),
                                                    (self.x2, self.y)), 2)
        # If on, draw the 'on' image
        if self.on:
            screen.blit(self.onImg, (self.x + 2, self.y + 2))
        # If off, draw the 'off' image
        else:
            screen.blit(self.offImg, (self.x + 2, self.y + 2))

    # If clicked on, toggle between on and off state
    def on_click(self, mouse_x, mouse_y):
        if self.rect.collidepoint(mouse_x, mouse_y):
            if self.on:
                self.on = False
            else:
                self.on = True
