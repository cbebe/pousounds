#!/usr/bin/env python

import time
from datetime import datetime

import pyautogui

import config as c


def click(coords):
    pyautogui.click(x=coords[0], y=coords[1])


def px_match(a, b, tolerance=10):
    for i in range(0, 3):
        if abs(a[i] - b[i]) > tolerance:
            return False

    return True


def is_pou(im, colour):
    return px_match(im.getpixel(c.COORDS[colour]), c.POUS[colour])


def get_last_pou():
    done_flag = 0
    last_pou = None
    while True:
        time.sleep(0.5)
        im = pyautogui.screenshot()
        pous = {key: is_pou(im, key) for key in c.POUS.keys()}
        has_open = False
        for key, value in pous.items():
            if not value:
                last_pou = key
                has_open = True
        if not has_open and last_pou is not None:
            done_flag += 1
        if done_flag == 3:
            print(last_pou)
            return last_pou


def get_screenshot_with_name(name=None):
    if name is None:
        name = f"{datetime.now().isoformat()}.png"
    pyautogui.screenshot(name)


def click_list(pou_list):
    for colour in pou_list:
        print(f"Clicking {colour}")
        click(c.COORDS[colour])
        time.sleep(0.1)


def countdown(count):
    while count > 0:
        print(f"{count}\r", end="")
        time.sleep(1)
        count -= 1
    print("Start")


def restart_game():
    click(c.PAUSE)
    click(c.RESTART)
    time.sleep(1)


def main():
    # pyautogui.mouseInfo()
    # return
    countdown(5)
    restart_game()
    pou_list = []
    while True:
        pou_list.append(get_last_pou())
        print(" ".join(pou[0] for pou in pou_list))
        click_list(pou_list)
        time.sleep(1.5)


if __name__ == "__main__":
    main()
