# frontend.py
import pygame
from utils import (BLUE, RED, GREEN, BLACK, BUTTON_COLOR, BUTTON_ACTIVE_COLOR,
                   DARK_GREY, SLIDER_BG_COLOR, SLIDER_HANDLE_COLOR)

pygame.font.init()
FONT = pygame.font.SysFont("Arial", 18)
STATUS_FONT = pygame.font.SysFont("Arial", 22)


def draw_array(win, arr, bar_width, height, highlight=None, sort_finished=False, offset_y=0):
    """Draws the bars representing the array."""
    for i, val in enumerate(arr):
        x = i * bar_width
        y = offset_y + (height - val)

        color = BLUE
        if sort_finished:
            color = GREEN
        elif highlight and i in highlight:
            color = RED

        pygame.draw.rect(win, color, (x, y, bar_width, val))
        pygame.draw.rect(win, DARK_GREY, (x, y, bar_width, val), 1)


def draw_ui(win, buttons, active_algo, status, slider):
    """Draws all UI elements like buttons, status text, and the slider."""
    for btn in buttons:
        is_active = (btn.text == active_algo)
        btn.draw(win, is_active)

    status_label = STATUS_FONT.render(f"Algorithm: {active_algo} | Status: {status}", True, DARK_GREY)
    win.blit(status_label, (10, 60))

    slider.draw(win)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = BUTTON_COLOR
        self.text_color = BLACK

    def draw(self, win, is_active=False):
        draw_color = BUTTON_ACTIVE_COLOR if is_active else self.color
        pygame.draw.rect(win, draw_color, self.rect, border_radius=5)
        pygame.draw.rect(win, DARK_GREY, self.rect, width=2, border_radius=5)

        label = FONT.render(self.text, True, self.text_color)
        label_rect = label.get_rect(center=self.rect.center)
        win.blit(label, label_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.handle_radius = h
        self.handle_x = x + (w * (initial_val - min_val) / (max_val - min_val))
        self.dragging = False

    def draw(self, win):
        pygame.draw.rect(win, SLIDER_BG_COLOR, self.rect, border_radius=5)
        pygame.draw.rect(win, DARK_GREY, self.rect, width=2, border_radius=5)
        pygame.draw.circle(win, SLIDER_HANDLE_COLOR, (self.handle_x, self.rect.centery), self.handle_radius)
        label = FONT.render(f"Speed: {self.get_value()}", True, DARK_GREY)
        win.blit(label, (self.rect.x, self.rect.y - 25))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) or \
                    pygame.math.Vector2(event.pos).distance_to((self.handle_x, self.rect.centery)) < self.handle_radius:
                self.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        if event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle_x = max(self.rect.x, min(event.pos[0], self.rect.right))
            self.val = self.min_val + ((self.handle_x - self.rect.x) / self.rect.w) * (self.max_val - self.min_val)

    def get_value(self):
        return int(self.val)