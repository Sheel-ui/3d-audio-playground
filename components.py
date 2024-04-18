import pygame
import math

class Button:
    def __init__(self,x,y,width,height,radius,button_color,hover_color,text,text_color,action,target):
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
        pygame.draw.rect(surface,self.color,self.rect,border_radius=self.radius)
        text_surface = pygame.font.Font(None,32).render(self.text,True,self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if self.target and event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action(self.target.text)
                self.target.text = ""
                
    def hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = self.hover_color
        else:
            self.color = self.button_color

class Input:
    def __init__(self,x,y,width,height,radius,inactive_color,active_color,text,text_color):
        self.rect = pygame.Rect(x,y,width,height)
        self.text = text
        self.color = inactive_color
        self.radius = radius
        self.text_color = text_color
        self.inactive_color = inactive_color
        self.active_color = active_color
    
    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect, 2,border_radius=self.radius)
        text_surface = pygame.font.Font(None,32).render(self.text,True,self.text_color)
        text_rect = text_surface.get_rect(left=self.rect.left + 10, centery=self.rect.centery)
        surface.blit(text_surface, text_rect)
                
    def read(self,event,button):
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
        self.circle = pygame.Surface((radius*2,radius*2),pygame.SRCALPHA)
        self.x = x
        self.y = y
        self.text = text
        self.color = inactive_color
        self.radius = radius
        self.text_color = text_color
        self.active_color = active_color
        self.inactive_color = inactive_color
    
    def draw(self,surface):
        text_surface = pygame.font.Font(None,32).render(self.text,True,self.text_color)
        pygame.draw.circle(self.circle,self.color,(self.radius,self.radius),self.radius)
        text_rect = text_surface.get_rect(left=self.x + 3)
        surface.blit(self.circle,(self.x,self.y))
        text_rect.top = self.y + 6  # Align the top of the text_rect with the top of the circle
        text_rect.left = self.x + 8  # Offset the text to the right slightly from the circle
        surface.blit(text_surface, text_rect)

    def click(self, event, selectedHrtf):
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
        self.plot = self.rect = pygame.Rect(x,y,width,height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect)