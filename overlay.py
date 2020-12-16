# customized version of https://github.com/ethanedits/overlayGUI/blob/main/src/oGUI.py

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame, win32api, win32gui, win32con, time

version = 0.4

width = win32api.GetSystemMetrics(0)
height = win32api.GetSystemMetrics(1)
screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
fuchsia = (255, 0, 128)
hwnd = pygame.display.get_wm_info()["window"]

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
cyan = (52, 204, 235)
orange = (242, 137, 31)
black = (0, 0, 0)
yellow = (255, 255, 0)
gray = (61, 61, 61)
lightgray = (110, 110, 110)
darkgray = (41, 41, 41)
purple = (133, 55, 250)

def init():
    pygame.init()
    pygame.display.set_caption("Mod menu")
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE)

def startLoop():         
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        exit(0)
    screen.fill(fuchsia)

def endLoop():
    pygame.display.update()

class Checkbox:

    def __init__(self, outsideColor, insideColor, x, y, width, height, enabledByDefault = False):
        self.outsideColor = outsideColor
        self.insideColor = insideColor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.checkBox_enabled = enabledByDefault
        self.is_hoverable = False
        self.hover_color = gray
        self.boolMousePos = False

    def is_hovered(self, hoveredColor):
        self.is_hoverable = True
        self.hover_color = hoveredColor

    def printMousePos(self):
        self.boolMousePos = True

    def is_enabled(self):
        return self.checkBox_enabled

    def draw(self):
        pygame.draw.rect(screen, self.outsideColor, pygame.Rect(self.x - self.width/8, self.y - self.height/8, self.width + self.width/4, self.height + self.height/4))

        mouse = pygame.mouse

        if self.x + self.width > mouse.get_pos()[0] > self.x and self.y + self.height > mouse.get_pos()[1] > self.y:
            #When Hovered Over
            if self.is_hoverable:
                pygame.draw.rect(screen, self.hover_color, pygame.Rect(self.x - self.width/8, self.y - self.height/8, self.width + self.width/4, self.height + self.height/4))

            #When clicked
            if mouse.get_pressed()[0]:
                self.checkBox_enabled = not self.checkBox_enabled
                time.sleep(0.15)

        if self.checkBox_enabled:
            pygame.draw.rect(screen, self.insideColor, pygame.Rect(self.x, self.y, self.width, self.height))

        if self.boolMousePos:
            print(mouse.get_pos())

class Rect:
    
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

class Box:

    def __init__(self, color, x, y, width, height, thickness):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.thickness = thickness
    
    def draw(self):
        pygame.draw.line(screen, self.color, (self.x + self.width, self.y), (self.x, self.y), self.thickness) #Top
        pygame.draw.line(screen, self.color, (self.x, self.y + self.height), (self.x, self.y), self.thickness) #Left
        pygame.draw.line(screen, self.color, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), self.thickness) #Right
        pygame.draw.line(screen, self.color, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), self.thickness) #Bottom

class Text:

    def __init__(self, color, x, y, FontSize, textStr):
        pygame.font.init()
        self.color = color
        self.x = x
        self.y = y
        self.FontSize = FontSize
        self.textStr = textStr
        self.FontString = 'Arial'
        #DropShadow
        self.dropShadowEnabled = False
        self.dropShadowColor = black
        self.dropShadowOffset = 2

    def font(self, fontStr):
        self.FontString = fontStr
    
    def dropShadow(self, color, offset):
        self.dropShadowEnabled = True
        self.dropShadowColor = color
        self.dropShadowOffset = offset

    def draw(self):
        myfont = pygame.font.SysFont(self.FontString, self.FontSize)
        textSurface = myfont.render(self.textStr, True, self.color) #Main Text

        if self.dropShadowEnabled:
            textSurface2 = myfont.render(self.textStr, True, black) #DropShadow
            screen.blit(textSurface2, (self.x + self.dropShadowOffset, self.y)) #DropShadow

        screen.blit(textSurface, (self.x, self.y)) #Main Text

class Button:
        def __init__(self, color, clickedColor, x,y,width,height, text=''):
            self.color = color
            self.clickedColor = clickedColor
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text
            self.is_hoverable = False
            self.hover_color = gray
            self.button_enabled = False

        def is_enabled(self):
            return self.button_enabled

        def is_hovered(self, hoveredColor):
            self.is_hoverable = True
            self.hover_color = hoveredColor

        def draw(self):
            pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

            mouse = pygame.mouse
            
            if self.x + self.width > mouse.get_pos()[0] > self.x and self.y + self.height > mouse.get_pos()[1] > self.y:
                if self.is_hoverable:
                    pygame.draw.rect(screen, self.hover_color, pygame.Rect(self.x, self.y, self.width, self.height))

                if mouse.get_pressed()[0]:
                    self.button_enabled = True
                    pygame.draw.rect(screen, self.clickedColor, pygame.Rect(self.x, self.y, self.width, self.height))
                else:
                    self.button_enabled = False 

class InputBox:
    def __init__(self, inactive_color, active_color, x, y, w, h, size=22, text='', off=None, address=0x00):
        pygame.font.init()              
        font = pygame.font.Font(None, size)
        self.address = address
        self.off = off
        self.font = font
        self.rect = pygame.Rect(x, y, w, h)
        self.color = inactive_color
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False
        self.active_color = active_color
        self.inactive_color = inactive_color

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.active_color if self.active else pygame.Color("dodgerblue2")
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return (self.text, self.off, self.address)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)