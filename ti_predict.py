from output import CNOutput
from cfg import Language
from ban_pick import BanPick
from cn_heroes import CNAbbrevHeroes


def main():
    team_no = 0
    teams = [[CNAbbrevHeroes.none, CNAbbrevHeroes.none,
              CNAbbrevHeroes.none, CNAbbrevHeroes.none,
              CNAbbrevHeroes.none],
             [CNAbbrevHeroes.none, CNAbbrevHeroes.none,
              CNAbbrevHeroes.none, CNAbbrevHeroes.none,
              CNAbbrevHeroes.none]]
    bans = []
    lang = Language.CN
    o = CNOutput()
    bp = BanPick()
    available = list(bp.data.keys())
    for ban in bans:
        available.remove(ban)
    for team in teams:
        for h in team:
            if h in available:
                available.remove(h)
    print('Available: {}'.format(len(available)))
    print('Teams: {}'.format(teams))
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
