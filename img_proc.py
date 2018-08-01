import cv2
from util import get_path
from PIL import ImageGrab
from cfg import Interface, HeroImage
from hero_index import HERO_INDEX
import json


def crop_hero_img():
    x, y, w, h = Interface.X, Interface.Y, Interface.W, Interface.H
    d_col, d_row, d_class = Interface.D_COL, Interface.D_ROW, Interface.D_CLASS
    hero_num = Interface.HERO_NUM
    img = cv2.imread('interface.png')
    for c, rows in enumerate(hero_num):
        for row, col_n in enumerate(rows):
            for col in range(col_n):
                hero_name = HERO_INDEX[str((c, row, col))]
                _x = x + col * d_col
                _y = y + row * d_row + c * d_class
                crop_img = img[_y:_y + h, _x:_x + w]
                cv2.imwrite(get_path('res/origin') +
                            '/{}.png'.format(hero_name), crop_img)


def crop_hero_template_img():
    w, h = Interface.W, Interface.H
    for c, rows in enumerate(Interface.HERO_NUM):
        for row, col_n in enumerate(rows):
            for col in range(col_n):
                hero_name = HERO_INDEX[str((c, row, col))]
                img = cv2.imread('res/origin/{}.png'.format(hero_name))
                crop_img = img[h - 20:h,
                           int(w / 2 - 10):int(w / 2 + 10)]
                cv2.imwrite(get_path('res/crop') +
                            '/{}.png'.format(hero_name), crop_img)


def crop_hero_up_template_image():
    up_w, up_h = HeroImage.I_UP_W, HeroImage.I_UP_H
    with open('data.json', 'r') as f:
        data = json.load(f)
    for h in data:
        path = get_path('res/heroes') + '/{}.png'.format(h)
        img = cv2.imread(path)
        res = cv2.resize(img, (up_w, up_h), interpolation=cv2.INTER_AREA)
        res = res[int(up_h / 2 - 10):int(up_h / 2 + 10),
              int(up_w / 2 - 10):int(up_w / 2 + 10)]
        cv2.imwrite(get_path('res/hero_up') + '/{}.png'.format(h), res)


class HeroMatchCV(object):
    def __init__(self):
        with open('data.json', 'r') as f:
            self.data = json.load(f)
        self.select_templates = {}
        for h in self.data:
            self.select_templates[h] = cv2.imread('res/crop/{}.png'.format(h))
        self.up_templates = {}
        for h in self.data:
            self.up_templates[h] = cv2.imread('res/hero_up/{}.png'.format(h))

    def find_index(self, img, c, row, col):
        hero_name = HERO_INDEX[str((c, row, col))]
        x, y, w, h = Interface.X, Interface.Y, Interface.W, Interface.H
        x = Interface.X + col * Interface.D_COL
        y = Interface.Y + row * Interface.D_ROW + c * Interface.D_CLASS
        template = self.select_templates[hero_name]
        crop_img = img[y:y + h, x:x + w]
        res = cv2.matchTemplate(crop_img, template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if min_val < 0.01:
            return True
        else:
            return False

    def find_up_hero(self, img, team, num):
        if team == 0:
            x = HeroImage.T_0_X + num * HeroImage.D_HERO
            y = HeroImage.T_0_Y
        else:
            x = HeroImage.T_1_X + num * HeroImage.D_HERO
            y = HeroImage.T_1_Y
        crop_img = img[y:y + HeroImage.UP_H, x:x + HeroImage.UP_W]
        for h, template in self.up_templates.items():
            res = cv2.matchTemplate(crop_img, template, cv2.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if min_val < 0.05:
                return h

    def find_heroes(self):
        available = []
        im = ImageGrab.grabclipboard()
        im.save('screenshot.png', 'PNG')
        img = cv2.imread('screenshot.png')
        hero_num = Interface.HERO_NUM
        for c, rows in enumerate(hero_num):
            for row, col_n in enumerate(rows):
                for col in range(col_n):
                    if self.find_index(img, c, row, col):
                        hero_name = HERO_INDEX[str((c, row, col))]
                        available.append(hero_name)

        teams = [[], []]
        for i in range(2):
            for j in range(5):
                res = self.find_up_hero(img, i, j)
                if res:
                    teams[i].append(res)
                else:
                    teams[i].append('none')
        return available, teams


def main():
    cv = HeroMatchCV()
    available, teams = cv.find_heroes()
    print(len(available), teams)


if __name__ == '__main__':
    main()
