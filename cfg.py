class Language(object):
    EN = 'en'
    CN = 'cn'


class Interface(object):
    X, Y, W, H = 169, 189, 46, 72
    D_COL, D_ROW, D_CLASS = 52, 80, 184
    HERO_NUM = [[21, 16], [21, 16], [21, 20]]


class MainHeroInterface(object):
    X, Y, W, H = 347, 155, 46, 92
    D_COL, D_ROW, D_CLASS = 56, 100, 224
    HERO_NUM = [[22, 15], [22, 15], [22, 19]]
    I_X, I_Y, I_W, I_H = 1142, 422, 28, 9
    I_D_COL, I_D_ROW, I_D_CLASS = 33, 20, 298
    I_NUM = [[3, 5], [3, 4]]
    ROLE_NAME = {
        '(0, 0)': 'Carry',
        '(0, 1)': 'Support',
        '(0, 2)': 'Nuker',
        '(0, 3)': 'Disabler',
        '(0, 4)': 'Jungler',
        '(1, 0)': 'Durable',
        '(1, 1)': 'Escape',
        '(1, 2)': 'Pusher',
        '(1, 3)': 'Initiator'
    }


class HeroImage(object):
    I_W, I_H = 205, 115
    I_UP_W, I_UP_H = 118, 66
    UP_W, UP_H = 97, 66
    T_0_X, T_0_Y = 176, 6
    T_1_X, T_1_Y = 1151, 6
    D_HERO = 124
