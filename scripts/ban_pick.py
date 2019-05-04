from dpapi.custom_lib.cn_heroes import Heroes
from dpapi.algo.core import Core
from tabulate import tabulate


def main():
    core = Core()
    core.load_data()
    cfg = {
        # Refer to dpapi/data/custom/custom_config.json
        'config_str': 'cn_h_y',
        # Refer to dpapi/data/generated/role_type.json
        'roles': ['Carry', 'Support']
    }
    match_ups = [Heroes.none, Heroes.none, Heroes.none,
                 Heroes.none, Heroes.none]
    teammates = [Heroes.none, Heroes.none, Heroes.none,
                 Heroes.none, Heroes.none]
    match_ups, teammates = core.remove_none(match_ups, teammates)
    r = core.calculate(cfg, match_ups, teammates, list(core.name_dict.keys()))
    print(r)
    print(tabulate(r['table']))
    print(r['output'])


if __name__ == '__main__':
    main()
