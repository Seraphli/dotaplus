import time
from data import CUSTOM_DATA
import json
from dpapi.util.util import get_path


def get_one_hero_role(c, row, col):
    import pyautogui
    import cv2
    # Click on hero interface
    pyautogui.click(465, 30, button='left')
    pyautogui.click(450, 90, button='left')
    x, y = CUSTOM_DATA['main_interface_hero']['x, y']
    w, h = CUSTOM_DATA['main_interface_hero']['w, h']
    d = CUSTOM_DATA['main_interface_hero']['d_col, d_row, d_class']
    x += col * d[0] + w / 2
    y += row * d[1] + c * d[2] + h / 2
    pyautogui.click(x, y, button='left')
    pyautogui.click(1435, 305, button='left')
    pyautogui.screenshot('temp_ss.png')
    img = cv2.imread('temp_ss.png')
    crop_img = img[400:600, 1070:1200]
    template = cv2.imread(get_path('res', parent=True) +
                          '/role_pos_template.png')
    res = cv2.matchTemplate(crop_img, template, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    assert (min_val < 0.01)
    loc = (min_loc[0] + 1112, min_loc[1] + 400)
    role = {}
    w, h = CUSTOM_DATA['role']['w, h']
    d = CUSTOM_DATA['role']['d_col, d_row, d_class']
    for c, col_row in enumerate(CUSTOM_DATA['role']['num']):
        cols, rows = col_row
        for row in range(rows):
            attr = 0
            for col in range(cols):
                x = loc[0] + col * d[0] + c * d[2]
                y = loc[1] + row * d[1]
                crop_img = img[y:y + h, x:x + w]
                mean = crop_img.mean()
                if mean > 50:
                    attr += 1
            role[CUSTOM_DATA['role']['role_pos'][str((c, row))]] = attr
    print(role)
    return role


def get_hero_role():
    roles = {}
    index = 0
    for c, rows in enumerate(CUSTOM_DATA['main_interface_hero']['num']):
        for row, col_n in enumerate(rows):
            for col in range(col_n):
                hero_name = CUSTOM_DATA['cn_layout'][index]
                print(hero_name)
                role = get_one_hero_role(c, row, col)
                roles[hero_name] = role
                index += 1
    with open(get_path('data', parent=True) + '/role.json', 'w') as f:
        json.dump(roles, f)


def main():
    import pyautogui
    pyautogui.PAUSE = 1
    time.sleep(3)
    get_hero_role()


if __name__ == '__main__':
    main()
