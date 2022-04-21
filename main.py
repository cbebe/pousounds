#!/usr/bin/env python

import time
from datetime import datetime

import pyautogui
from attr import has

X = (617, 796)
Y = (381, 548)

POUS = {
    "RED": (248, 64, 61),
    "GREEN": (61, 251, 69),
    "BLUE": (62, 169, 248),
    "YELLOW": (249, 241, 60)
}

COORDS = {
    "RED": (X[0], Y[0]),
    "GREEN": (X[1], Y[0]),
    "BLUE": (X[0], Y[1]),
    "YELLOW": (X[1], Y[1]),
}


def is_mouth(im, colour):
    px = im.getpixel(colour)
    red_match = (110 < px[0] < 130)
    grn_match = (30 < px[1] < 45)
    blu_match = (20 < px[2] < 45)
    one_match = red_match or grn_match or blu_match
    all_match = red_match and grn_match and blu_match
    if one_match and not all_match:
        print(f"One does not match: {px}")

    return all_match


def px_match(a, b, tolerance=10):
    for i in range(0, 3):
        if abs(a[i] - b[i]) > tolerance:
            return False

    return True


def is_pou(im, colour):
    return px_match(im.getpixel(COORDS[colour]), POUS[colour])


def check_mouths():
    done_flag = 0
    last_open = None
    while True:
        time.sleep(0.5)
        im = pyautogui.screenshot()
        pous = {key: is_pou(im, key) for key in POUS.keys()}
        has_open = False
        for key, value in pous.items():
            if not value:
                last_open = key
                has_open = True
        if not has_open and last_open is not None:
            done_flag += 1
        if done_flag == 3:
            print(last_open)
            return last_open


def get_screenshot_with_name(name=None):
    if name is None:
        name = f"{datetime.now().isoformat()}.png"
    pyautogui.screenshot(name)


def click_list(pou_list):
    for colour in pou_list:
        coords = COORDS[colour]
        print(f"Clicking {colour}")
        pyautogui.click(x=coords[0], y=coords[1])
        time.sleep(0.1)


def main():
    # pyautogui.mouseInfo()
    # return
    pou_list = []
    count = 5
    while count > 0:
        print(count)
        time.sleep(1)
        count -= 1
    while True:
        pou_list.append(check_mouths())
        click_list(pou_list)
        time.sleep(1.5)


if __name__ == "__main__":
    main()
