import time
from data.cfg import MainHeroInterface
from data.hero_index import HERO_INDEX
from dataproc.get_data import insert_role_into_data
import json


def get_one_hero_role(c, row, col):
    import pyautogui
    import cv2
    # Click on hero interface
    pyautogui.click(465, 30, button='left')
    pyautogui.click(450, 90, button='left')
    x, y, w, h = MainHeroInterface.X, MainHeroInterface.Y, \
                 MainHeroInterface.W, MainHeroInterface.H
    x += col * MainHeroInterface.D_COL + w / 2
    y += row * MainHeroInterface.D_ROW + c * MainHeroInterface.D_CLASS + h / 2
    pyautogui.click(x, y, button='left')
    pyautogui.click(1435, 305, button='left')
    pyautogui.screenshot('temp_ss.png')
    img = cv2.imread('temp_ss.png')
    crop_img = img[400:600, 1070:1200]
    template = cv2.imread('res/role_pos_template.png')
    res = cv2.matchTemplate(crop_img, template, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    assert (min_val < 0.01)
    loc = (min_loc[0] + 1112, min_loc[1] + 400)
    role = {}
    for c, col_row in enumerate(MainHeroInterface.I_NUM):
        cols, rows = col_row
        for row in range(rows):
            attr = 0
            for col in range(cols):
                x = loc[0] + col * MainHeroInterface.I_D_COL + \
                    c * MainHeroInterface.I_D_CLASS
                y = loc[1] + row * MainHeroInterface.I_D_ROW
                crop_img = img[y:y + MainHeroInterface.I_H,
                           x:x + MainHeroInterface.I_W]
                mean = crop_img.mean()
                if mean > 50:
                    attr += 1
            role[MainHeroInterface.ROLE_NAME[str((c, row))]] = attr
    return role


def get_hero_role():
    roles = {}
    for c, rows in enumerate(MainHeroInterface.HERO_NUM):
        for row, col_n in enumerate(rows):
            for col in range(col_n):
                index = row * 22 + col
                _row = index // 21
                _col = index % 21
                hero_name = HERO_INDEX[str((c, _row, _col))]
                role = get_one_hero_role(c, row, col)
                roles[hero_name] = role
    with open('role.json', 'w') as f:
        json.dump(roles, f)


def main():
    import pyautogui
    pyautogui.PAUSE = 1
    time.sleep(3)
    get_hero_role()
    insert_role_into_data()


if __name__ == '__main__':
    main()
