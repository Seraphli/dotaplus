class CVGen(object):
    @staticmethod
    def crop_hero_template_img():
        from data import CUSTOM_DATA
        interface = CUSTOM_DATA['hero_choose_interface']
        w, h = interface['w, h']
        for c, rows in enumerate(interface['num']):
            for row, col_n in enumerate(rows):
                for col in range(col_n):
                    # if not (c == 0 and row == 0 and col == 11):
                    #     continue
                    hero_name = HERO_INDEX[str((c, row, col))]
                    img = cv2.imread('res/origin/{}.png'.format(hero_name))
                    crop_img = img[h - 20:h,
                               int(w / 2 - 10):int(w / 2 + 10)]
                    cv2.imwrite(get_path('res/crop') +
                                '/{}.png'.format(hero_name), crop_img)
