# main.py
import pygame
import sys
import random
from backend import bubble_sort, insertion_sort, quick_sort
from frontend import draw_array, draw_ui, Button, Slider
from utils import WHITE

# --- Setup ---
pygame.init()
WIDTH, HEIGHT = 1100, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algorithm Visualizer")

# --- Constants & State ---
UI_AREA_HEIGHT = 100
ARRAY_AREA_HEIGHT = HEIGHT - UI_AREA_HEIGHT
NUM_BARS = 100
MIN_VAL, MAX_VAL = 10, ARRAY_AREA_HEIGHT - 20
bar_width = WIDTH / NUM_BARS

array = []
sorter = None
algorithm_name = "None"
status = "Idle"
highlight = None
sort_finished = False

# --- UI Elements ---
buttons = [
    Button(10, 10, 120, 40, "Bubble Sort"),
    Button(140, 10, 130, 40, "Insertion Sort"),
    Button(280, 10, 120, 40, "Quick Sort"),
    Button(430, 10, 100, 40, "Start"),
    Button(540, 10, 100, 40, "Pause"),
    Button(670, 10, 120, 40, "Randomize"),
]
speed_slider = Slider(x=820, y=25, w=250, h=10, min_val=1, max_val=500, initial_val=100)


def generate_array():
    """Generates a new random array and resets the application state."""
    global array, sorter, algorithm_name, status, highlight, sort_finished
    array = [random.randint(MIN_VAL, MAX_VAL) for _ in range(NUM_BARS)]
    sorter = None
    algorithm_name = "None"
    status = "Idle"
    highlight = None
    sort_finished = False


def choose_sort(name):
    """Selects a sorting algorithm and prepares its generator."""
    global array, sorter, algorithm_name, status, sort_finished
    # Make a fresh copy of the array for the new sort
    current_array_state = array[:]
    generate_array()  # Reset state
    array = current_array_state  # Restore the array state

    algorithm_name = name
    if name == "Bubble Sort":
        sorter = bubble_sort(array)
    elif name == "Insertion Sort":
        sorter = insertion_sort(array)
    elif name == "Quick Sort":
        sorter = quick_sort(array)

    status = "Ready"
    sort_finished = False


def handle_button_click(text):
    """Handles logic for button presses."""
    global status
    if text in ["Bubble Sort", "Insertion Sort", "Quick Sort"]:
        choose_sort(text)
    elif text == "Start":
        if sorter is not None and status != "Sorting":
            status = "Sorting"
    elif text == "Pause":
        if status == "Sorting":
            status = "Paused"
    elif text == "Randomize":
        generate_array()


def main():
    """The main application loop."""
    global array, sorter, status, highlight, sort_finished

    clock = pygame.time.Clock()
    running = True
    generate_array()

    while running:
        clock.tick(speed_slider.get_value())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            speed_slider.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not speed_slider.dragging:  # Prevent button clicks when dragging slider
                    pos = pygame.mouse.get_pos()
                    for btn in buttons:
                        if btn.is_clicked(pos):
                            handle_button_click(btn.text)

        if status == "Sorting" and sorter is not None:
            try:
                array, highlight, step_status = next(sorter)
                if step_status == "Finished":
                    status = "Finished"
                    sort_finished = True
                    highlight = None
            except StopIteration:
                status = "Finished"
                sort_finished = True
                sorter = None
                highlight = None

        win.fill(WHITE)
        draw_ui(win, buttons, algorithm_name, status, speed_slider)
        draw_array(win, array, bar_width, ARRAY_AREA_HEIGHT, highlight, sort_finished, offset_y=UI_AREA_HEIGHT)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()