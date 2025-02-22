# ZenClock.py
import pygame
import sys
import math
from pygame.locals import *

# تنظیمات پنجره
WIDTH, HEIGHT = 85, 85
SUN_RADIUS = 10
ORBIT_RADIUS = 30
TRANSPARENT_COLOR = (0, 0, 0, 0)

class ZenClock:
    def __init__(self):
        pygame.init()
        self.angle = 0
        self.dragging = False
        self.offset = (0, 0)
        
        # ایجاد پنجره شفاف
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME | pygame.SRCALPHA)
        pygame.display.set_caption("Zen Clock")
        self.set_window_icon()
        
        # ماسک دایره‌ای
        self.mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(self.mask, (255,255,255,255), (WIDTH//2, HEIGHT//2), WIDTH//2)
        
        # موقعیت اولیه پنجره
        self.window_pos = [100, 100]
        self.update_window_position()

    def set_window_icon(self):
        icon = pygame.Surface((32,32), pygame.SRCALPHA)
        pygame.draw.circle(icon, (255,215,0), (16,16), 12)
        pygame.draw.line(icon, (255,255,0,150), (16,16), (28,16), 3)
        pygame.display.set_icon(icon)

    def update_window_position(self):
        try:
            import ctypes
            hwnd = pygame.display.get_wm_info()['window']
            ctypes.windll.user32.SetWindowPos(hwnd, -1, 
                self.window_pos[0], self.window_pos[1], 0, 0, 0x0001)
        except:
            pass

    def hsl_to_rgb(self, h, s, l):
        h /= 360.0
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        
        rgb = []
        for c in (h + 1/3, h, h - 1/3):
            if c < 0: c += 1
            if c > 1: c -= 1
            
            if c < 1/6:
                temp = p + (q - p) * 6 * c
            elif c < 0.5:
                temp = q
            elif c < 2/3:
                temp = p + (q - p) * (2/3 - c) * 6
            else:
                temp = p
            
            rgb.append(int(temp * 255))
        
        return tuple(rgb)

    def get_sky_color(self):
        progress = self.angle / 360
        hue = 40 - (progress * 40)
        return self.hsl_to_rgb(hue, 0.7, 0.5)

    def draw_sun(self):
        rad = math.radians(self.angle - 90)
        x = WIDTH//2 + ORBIT_RADIUS * math.cos(rad)
        y = HEIGHT//2 + ORBIT_RADIUS * math.sin(rad) * 1.2
        
        pygame.draw.circle(self.screen, (255,215,0), (int(x), int(y)), SUN_RADIUS)
        
        for i in range(8):
            angle = self.angle + i*45
            rad = math.radians(angle)
            start = (x + math.cos(rad)*10, y + math.sin(rad)*10)
            end = (x + math.cos(rad)*18, y + math.sin(rad)*18)
            alpha = 100 + (i % 2)*50
            pygame.draw.line(self.screen, (255,255,0,alpha), start, end, 2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
                self.angle = (self.angle + 2) % 360
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if math.hypot(mouse_pos[0]-WIDTH//2, mouse_pos[1]-HEIGHT//2) <= WIDTH//2:
                        self.dragging = True
                        self.offset = (event.pos[0], event.pos[1])
                self.angle = (self.angle + 1) % 360
            
            if event.type == MOUSEBUTTONUP:
                self.dragging = False
            
            if event.type == MOUSEMOTION and self.dragging:
                self.window_pos[0] += event.rel[0]
                self.window_pos[1] += event.rel[1]
                self.update_window_position()

    def run(self):
        while True:
            self.handle_events()
            
            self.screen.fill(TRANSPARENT_COLOR)
            self.screen.blit(self.mask, (0,0), special_flags=BLEND_RGBA_MULT)
            
            pygame.draw.circle(self.screen, self.get_sky_color(), (WIDTH//2, HEIGHT//2), WIDTH//2)
            
            self.draw_sun()
            pygame.display.update()
            pygame.time.Clock().tick(60)

    def quit(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    ZenClock().run()
