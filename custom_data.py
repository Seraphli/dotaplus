import codecs

CN_ABBREV_DICT = {
    'antimage': ['DF', 'AM', '敌法', '敌法师'],
    'axe': ['FW', 'AXE', '斧王'],
    'bane': ['痛苦之源', '祸乱之源'],
    'bloodseeker': ['BS', '血魔', '嗜血狂魔'],
    'crystal_maiden': ['CM', '冰女', '水晶室女'],
    'drow_ranger': ['DR', '小黑', '黑弓', '卓尔游侠'],
    'earthshaker': ['ES', '神牛', '小牛', '撼地神牛', '撼地者'],
    'juggernaut': ['JUGG', '剑圣', '主宰'],
    'mirana': ['POM', 'POTM', '白虎', '月之女祭司', '米拉娜'],
    'morphling': ['MOR', 'MORPH', '水人', '变体精灵'],
    'nevermore': ['SF', '沙发', '影魔'],
    'phantom_lancer': ['PL', '猴子', '幻影长矛手'],
    'puck': ['仙女龙', '帕克'],
    'pudge': ['TF', '胖子', '屠夫'],
    'razor': ['电魂', '闪电幽魂', '剃刀'],
    'sand_king': ['SK', '沙王'],
    'storm_spirit': ['蓝猫', '风暴之灵'],
    'sven': ['SV', 'SW', '流浪剑客', '斯温'],
    'tiny': ['山岭巨人', '小小'],
    'vengefulspirit': ['VS', '复仇之魂'],
    'windrunner': ['WR', '风行', '风行者'],
    'zuus': ['ZS', '众神之王', '宙斯'],
    'kunkka': ['船长', '海军上将', '昆卡'],
    'lina': ['火女', '秀逗魔导士', '莉娜'],
    'lion': ['恶魔巫师', '莱恩'],
    'shadow_shaman': ['XY', '小Y', '萨满', '暗影萨满'],
    'slardar': ['大鱼', '大鱼人', '斯拉达'],
    'tidehunter': ['TH', '潮汐', '潮汐猎人'],
    'witch_doctor': ['WD', '巫医'],
    'lich': ['巫妖'],
    'riki': ['SA', '隐刺', '隐形刺客', '力丸'],
    'enigma': ['谜团'],
    'tinker': ['TK', '地精修补匠', '修补匠'],
    'sniper': ['矮子', '火枪', '火枪手', '矮人火枪手', '狙击手'],
    'necrolyte': ['NEC', '死灵法', '死灵法师', '瘟疫法师'],
    'warlock': ['WL', 'WLK', '术士'],
    'beastmaster': ['BM', '兽王'],
    'queenofpain': ['QOP', '女王', '痛苦女王'],
    'venomancer': ['剧毒', '剧毒术士'],
    'faceless_void': ['FV', '虚空', '虚空假面'],
    'skeleton_king': ['SNK', '骷髅王', '冥魂大帝'],
    'death_prophet': ['DP', '死亡先知'],
    'phantom_assassin': ['PA', '幻刺', '幻影刺客'],
    'pugna': ['PUG', '骨法', '遗忘法师', '帕格纳'],
    'templar_assassin': ['TA', '圣堂', '圣堂刺客'],
    'viper': ['VIP', 'VIPER', 'VP', '蝮蛇', '毒龙', '冥界亚龙'],
    'luna': ['月骑', '月之女骑士', '露娜'],
    'dragon_knight': ['DK', '龙骑', '龙骑士'],
    'dazzle': ['暗牧', '暗影牧师', '戴泽'],
    'rattletrap': ['CW', '发条', '发条技师'],
    'leshrac': ['老鹿', '受折磨的灵魂', '拉席克'],
    'furion': ['FUR', 'NP', '先知'],
    'life_stealer': ['LS', '小狗', '食尸鬼', '噬魂鬼'],
    'dark_seer': ['DS', '黑贤', '兔子', '黑暗贤者'],
    'clinkz': ['小骷髅', '骨弓', '骷髅射手', '克林克兹'],
    'omniknight': ['OK', '全能', '全能骑士'],
    'enchantress': ['ENT', '小鹿', '魅惑魔女'],
    'huskar': ['HUS', '神灵', '神灵武士', '哈斯卡'],
    'night_stalker': ['NS', '夜魔', '暗夜魔王'],
    'broodmother': ['ZZ', '蜘蛛', '育母蜘蛛'],
    'bounty_hunter': ['BH', '赏金', '赏金猎人'],
    'weaver': ['蚂蚁', '地穴编制者', '编制者'],
    'jakiro': ['双头龙', '杰齐洛'],
    'batrider': ['BAT', '蝙蝠', '蝙蝠骑士'],
    'chen': ['老陈', '圣骑士', '陈'],
    'spectre': ['UG', 'SPE', '幽鬼'],
    'ancient_apparition': ['AA', '冰魂', '极寒幽魂', '远古冰魄'],
    'doom_bringer': ['DOOM', '末日', '末日使者'],
    'ursa': ['拍拍', '拍拍熊', '熊战士'],
    'spirit_breaker': ['SB', '白牛', '裂魂人'],
    'gyrocopter': ['GYRO', '飞机', '矮人直升机'],
    'alchemist': ['GA', '炼金', '炼金术士'],
    'invoker': ['卡尔', '召唤师', '祈求者'],
    'silencer': ['SIL', '沉默', '沉默术士'],
    'obsidian_destroyer': ['OD', '黑鸟', '殁境神蚀者'],
    'lycan': ['狼人'],
    'brewmaster': ['BREW', '熊猫', '大熊猫', '熊猫酒仙', '酒仙'],
    'shadow_demon': ['SD', '毒狗', '艾瑞达', '暗影恶魔'],
    'lone_druid': ['LD', '小德', '德鲁伊'],
    'chaos_knight': ['CK', '混沌', '混沌骑士'],
    'meepo': ['狗头', '狗头人', '地卜师', '米波'],
    'treant': ['TREE', '大树', '树精卫士'],
    'ogre_magi': ['蓝胖', '食人魔魔法师'],
    'undying': ['UD', '尸王', '不朽尸王'],
    'rubick': ['大魔导师', '拉比克'],
    'disruptor': ['萨尔', '干扰者'],
    'nyx_assassin': ['NYX', '小强', '地穴刺客', '司夜刺客'],
    'naga_siren': ['NAGA', '小娜迦', '娜迦女妖'],
    'keeper_of_the_light': ['KOTL', '光法', '光之守卫'],
    'wisp': ['IO', '小精灵', '艾欧'],
    'visage': ['VIS', '死灵龙', '死灵飞龙', '维萨吉'],
    'slark': ['小鱼', '小鱼人', '鱼人夜行者', '斯拉克'],
    'medusa': ['MED', '大娜迦', '美杜莎'],
    'troll_warlord': ['TROLL', '巨魔', '巨魔战将'],
    'centaur': ['人马', '半人马', '半人马战行者'],
    'magnataur': ['MAG', '猛犸', '半人猛犸', '马格纳斯'],
    'shredder': ['TIMBER', '伐木机'],
    'bristleback': ['BB', '刚背', '钢背', '刚背兽', '钢背兽'],
    'tusk': ['海民', '巨牙海民'],
    'skywrath_mage': ['SM', '天怒', '天怒法师'],
    'abaddon': ['地狱领主', '死骑', '死亡骑士', '魔霭领主', '亚巴顿'],
    'elder_titan': ['ET', '大牛', '牛头人酋长', '上古巨神'],
    'legion_commander': ['LC', '军团', '军团指挥官'],
    'techies': ['炸弹人', '哥布林工程师', '工程师'],
    'ember_spirit': ['EMBER', '火猫', '灰烬之灵'],
    'earth_spirit': ['土猫', '大地之灵'],
    'abyssal_underlord': ['大屁股', '深渊领主', '孽主'],
    'terrorblade': ['TB', '魂守', '灵魂守卫', '恐怖利刃'],
    'phoenix': ['菲尼克斯', '凤凰'],
    'oracle': ['神谕', '神谕者'],
    'winter_wyvern': ['冰龙', '寒冬飞龙'],
    'arc_warden': ['ARC', '电狗', '弧光', '弧光守卫者', '天穹守望者'],
    'monkey_king': ['MK', '大圣', '齐天大圣'],
    'dark_willow': ['小仙女', '花仙子', '邪影芳灵'],
    'pangolier': ['穿山甲', '滚滚', '石鳞剑士']
}


def get_hero(name):
    for k, v in CN_ABBREV_DICT.items():
        if name.upper() == k.upper() or name.upper() in v:
            return k

    raise ValueError('Cannot find hero: {}'.format(name))


def to_key_name(heroes):
    heroes = [get_hero(name) for name in heroes]
    return heroes


def generate_abbrev_name_py():
    lines = ['class CNAbbrevHeroes(object):\n    none = "none"\n']
    for h in CN_ABBREV_DICT:
        lines.append('    {} = "{}"\n'.format(h, h))
        for abbrev in CN_ABBREV_DICT[h]:
            if ord(abbrev[0]) < 255:
                lines.append('    {} = "{}"\n'.format(abbrev.upper(), h))
                lines.append('    {} = "{}"\n'.format(abbrev.lower(), h))
            else:
                lines.append('    {} = "{}"\n'.format(abbrev, h))
    with codecs.open('cn_heroes.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)


def main():
    generate_abbrev_name_py()


if __name__ == '__main__':
    main()
