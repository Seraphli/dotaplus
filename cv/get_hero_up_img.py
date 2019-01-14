import pyautogui
import time
from data.cfg import Interface, HeroImage
from dpapi.util.util import get_path
from data.hero_index import HERO_INDEX
import cv2


def get_one_hero_up_image(c, row, col):
    hero_name = HERO_INDEX[str((c, row, col))]
    # Start AI game
    pyautogui.click(1700, 1035, clicks=2, interval=1, button='left')
    time.sleep(2)
    x, y, w, h = Interface.X, Interface.Y, Interface.W, Interface.H
    x += col * Interface.D_COL + w / 2
    y += row * Interface.D_ROW + c * Interface.D_CLASS + h / 2
    pyautogui.click(x, y, button='left')
    pyautogui.click(1470, 795, button='left')
    pyautogui.screenshot('temp_ss.png')
    img = cv2.imread('temp_ss.png')
    crop_img = img[HeroImage.T_0_Y:HeroImage.T_0_Y + HeroImage.UP_H,
               HeroImage.T_0_X:HeroImage.T_0_X + HeroImage.UP_W]
    cv2.imwrite(get_path('res/hero_up_img') +
                '/{}.png'.format(hero_name), crop_img)
    pyautogui.click(30, 30, button='left')
    pyautogui.click(1700, 1035, button='left')


def get_hero_up_images():
    hero_num = Interface.HERO_NUM
    for c, rows in enumerate(hero_num):
        for row, col_n in enumerate(rows):
            for col in range(col_n):
                get_one_hero_up_image(c, row, col)
                time.sleep(1)


def main():
    pyautogui.PAUSE = 2
    time.sleep(2)
    get_hero_up_images()


if __name__ == '__main__':
    main()
