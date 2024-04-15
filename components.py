import pygame

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
