from pygame import gfxdraw
import pygame
import math

class Button:
   
    def __init__(self,x,y,width,height,radius,button_color,hover_color,text,text_color,action,target):
        '''
        Initializes a Button object with specified attributes.
        '''
        self.rect = pygame.Rect(x,y,width,height)
        self.text = text
        self.action = action
        self.text_color = text_color
        self.color = button_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.radius = radius
        self.target = target
        
    def draw(self,surface):
        '''
        Draws the button on the specified surface.

        Args:
            surface (pygame.Surface): The surface on which to draw the button.
        '''
         
        pygame.draw.rect(surface,self.color,self.rect,border_radius=self.radius)
        text_surface = pygame.font.Font(None,30).render(self.text,True,self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        '''
          Handles mouse click event on the button.

        Args:
            event (pygame.Event): The event to be handled.
        '''
        if self.target and event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action(self.target.text)
                self.target.text = ""
                
    def hover(self):
        '''
            Changes button color when hovered over.
        '''
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = self.hover_color
        else:
            self.color = self.button_color

class Input:
    def __init__(self,x,y,width,height,radius,inactive_color,active_color,text,text_color):
        '''
        Initializes an Input object with specified attributes.
        '''
        self.rect = pygame.Rect(x,y,width,height)
        self.text = text
        self.color = inactive_color
        self.radius = radius
        self.text_color = text_color
        self.inactive_color = inactive_color
        self.active_color = active_color
    
    def draw(self,surface):
        '''
        Draws the input field on the specified surface.

        Args:
            surface (pygame.Surface): The surface on which to draw the input field.
        '''
        pygame.draw.rect(surface,self.color,self.rect, 2,border_radius=self.radius)
        text_surface = pygame.font.Font(None,24).render(self.text,True,self.text_color)
        text_rect = text_surface.get_rect(left=self.rect.left + 10, centery=self.rect.centery)
        surface.blit(text_surface, text_rect)
                
    def read(self,event,button):
        '''
         Reads user input from the input field.

        Args:
            event (pygame.Event): The event to be handled.
            button (Button): The button associated with the input field.
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.color = self.active_color
            else:
                self.color = self.inactive_color
                
        if event.type == pygame.KEYDOWN:
            if self.color == self.active_color:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    button.action(self.text)
                    self.text = ""
                else:
                    self.text += event.unicode

class Circle:
    def __init__(self,x,y,radius,inactive_color,active_color,text,text_color):
        '''
         Initializes a Circle object with specified attributes.
        '''
        self.circle = pygame.Surface((radius*2,radius*2),pygame.SRCALPHA)
        self.x = x
        self.y = y
        self.text = text
        self.color = inactive_color
        self.radius = radius
        self.text_color = text_color
        self.active_color = active_color
        self.inactive_color = inactive_color
    
    def draw(self, surface):
        '''
        Draws the circle on the specified surface.
        '''
        text_surface = pygame.font.Font(None, 32).render(self.text, True, self.text_color)
        pygame.draw.circle(surface, self.color, (self.x + self.radius, self.y + self.radius), self.radius)
        pygame.gfxdraw.aacircle(surface, self.x + self.radius, self.y + self.radius, self.radius, self.color)
        pygame.gfxdraw.filled_circle(surface, self.x + self.radius, self.y + self.radius, self.radius, self.color)
        text_rect = text_surface.get_rect(left=self.x + 9, top=self.y + 6)
        surface.blit(text_surface, text_rect)

    def click(self, event, selectedHrtf):
        '''
        Handles mouse click event on the circle.

        Args:
            event (pygame.Event): The event to be handled.
            selectedHrtf (str): The currently selected HRTF.

        Returns:
            str: The newly selected HRTF
        '''
        if selectedHrtf==self.text:
            self.color = self.active_color
            return selectedHrtf
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos  # Use event.pos to get the mouse position
            distance = math.sqrt((mouse_x - (self.x + self.radius)) ** 2 + (mouse_y - (self.y + self.radius)) ** 2)
            if distance <= self.radius:
                self.color = self.active_color
                return self.text
            else:
                self.color = self.inactive_color

        return selectedHrtf
    
class Plot:
    def __init__(self,x,y,width,height,color):
        '''
        Initializes a Plot object with specified attributes.
        '''
        self.plot = self.rect = pygame.Rect(x,y,width,height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self,surface):
        '''
        Draws the texts on the specified surface.
        '''
        pygame.draw.rect(surface,self.color,self.rect)

class Text:
    def __init__(self, texts, positions, font_sizes, colors):
        '''
        Initializes a Text object with specified attributes.
        '''
        self.texts = texts
        self.positions = positions
        self.font_sizes = font_sizes
        self.colors = colors
        self.fonts = [pygame.font.Font(None, size) for size in font_sizes]

    def draw(self, surface):
         
        for text, pos, font, color in zip(self.texts, self.positions, self.fonts, self.colors):
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(left=pos[0], top=pos[1])
            surface.blit(text_surface, text_rect)