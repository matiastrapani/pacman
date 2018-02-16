import pygame
class Txt(pygame.surface.Surface):
    def __init__(self, general_sprites):
        self.sheet = general_sprites
        self.sheet.set_clip(pygame.Rect(1699, 535, 30, 30))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.digit  = { 0: (1699, 535, 30, 30), 1: (1729, 535, 30, 30), 2: (1759, 535, 30, 30), 3: (1789, 535, 30, 30), 4: (1819, 535, 30, 30), 5: (1849, 535, 30, 30), 6: (1879, 535, 30, 30), 7: (1909, 535, 30, 30), 8: (1939, 535, 30, 30), 9: (1969, 535, 30, 30)}
   
    def handle_event(self, event, num, position):
        if event.type == pygame.QUIT:
            game_over = True
        num_str = str(num)
        if num == 0: num_str = "00"
        num_list = list(map(int, num_str))
        surf = pygame.Surface (((len(num_list))*24+3, 30), pygame.SRCALPHA, 32)
        for n in range(0, len(num_list)):
            surf.blit (self.sheet.subsurface(self.digit[num_list[n]]),(n*24,0))
        
        self.image = surf
        self.rect = self.image.get_rect()
        self.rect.center = position
