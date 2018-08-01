from output import CNOutput
from cfg import Language
from ban_pick import BanPick
from img_proc import HeroMatchCV


def main():
    team_no = 0
    lang = Language.CN
    cv = HeroMatchCV()
    o = CNOutput()
    bp = BanPick()
    available, teams = cv.find_heroes()
    teammates = teams[team_no]
    match_ups = teams[1 - team_no]
    match_ups, teammates = bp.remove_none(match_ups, teammates)
    r = bp.recommend(match_ups, teammates, available)
    if r is not None:
        _, _, _, t_1, t_2 = r
        t_1 = bp.convert_table_lang(t_1, lang)
        t_2 = bp.convert_table_lang(t_2, lang)
        bp.print_recommend(t_1, t_2)
        o.recommend(match_ups, teammates, available)
    r = bp.win_rate(match_ups, teammates, lang=lang)
    if r is not None:
        _, _, _, table = r
        table = bp.convert_table_lang(table, lang)
        bp.print_table(table, headers=['Name', 'Value', 'Reason'])
        o.win_rate(match_ups, teammates)


if __name__ == '__main__':
    main()
