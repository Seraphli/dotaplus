from dpapi.util.util import get_path
import codecs
import glob
import os
from collections import defaultdict
import json
import vdf
import copy
import subprocess
import shlex
import shutil


def extract_hero_name():
    dota2_data = get_path('data/dota2', parent=True)
    generated_data = get_path('data/generated', parent=True)

    hero_name_dict = defaultdict(dict)
    for file in glob.glob(dota2_data + '/dota_*.txt'):
        language = os.path.splitext(os.path.basename(
            file))[0].replace('dota_', '')
        with codecs.open(file, encoding='utf-16') as f:
            d = vdf.parse(f)
            for k, real_name in d['lang']['Tokens'].items():
                if 'npc_dota_hero_' in k and 'hype' not in k and \
                        'creep' not in k and 'none' not in k and \
                        'dummy' not in k:
                    hero_name = k.replace('npc_dota_hero_', '')
                    hero_name_dict[hero_name][language] = real_name
                    hero_name_dict[hero_name]['raw_hero_name'] = k
    with codecs.open(generated_data + '/name_dict.json', 'w',
                     encoding='utf8') as f:
        json.dump(hero_name_dict, f)


def extract_hero_roles():
    dota2_data = get_path('data/dota2', parent=True)
    generated_data = get_path('data/generated', parent=True)

    # Extract role type
    role_type = {}
    with codecs.open(dota2_data + '/dota_english.txt', encoding='utf-16') as f:
        d = vdf.parse(f)
        for k, v in d['lang']['Tokens'].items():
            if 'DOTA_HeroRole_' in k and 'Lane' not in k and \
                    'Description' not in k:
                role_type[k] = v

    with codecs.open(generated_data + '/role_type.json', 'w',
                     encoding='utf8') as f:
        json.dump(role_type, f)

    types = role_type.values()
    role_type_dict = dict(zip(types, [0 for _ in range(len(types))]))

    def init_roles_dict():
        return copy.copy(role_type_dict)

    # Extract hero roles
    hero_info_dict = defaultdict(init_roles_dict)
    npc_heroes = vdf.parse(open(dota2_data + '/npc_heroes.txt'))['DOTAHeroes']
    for hero, info in npc_heroes.items():
        if hero.find('npc_dota_hero') < 0 or hero.find('base') >= 0:
            continue
        hero = hero.replace('npc_dota_hero_', '')
        roles = dict(zip(info['Role'].split(','),
                         [int(i) for i in info['Rolelevels'].split(',')]))
        hero_info_dict[hero].update(roles)

    with codecs.open(generated_data + '/hero_info.json', 'w',
                     encoding='utf8') as f:
        json.dump(hero_info_dict, f)


def decompile_dota2_package(dota2_path, f_path):
    dll_path = get_path('tools/Decompiler', parent=True)
    dll_path = dll_path.replace('\\', '/')
    dll_path = f'"{dll_path}/Decompiler.dll"'
    vpk_path = f'"{dota2_path}/game/dota/pak01_dir.vpk"'
    tmp_path = get_path('data/tmp', parent=True)
    cmd = f'dotnet {dll_path} -i {vpk_path} ' \
        f'-o "{tmp_path}" -d -f "{f_path}"'
    args = shlex.split(cmd)
    process = subprocess.Popen(args, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output, error = process.communicate()
    print(output.decode())
    print(error.decode())


def prepare_dota2_resource(dota2_path):
    dota2_data = get_path('data/dota2', parent=True)
    tmp_path = get_path('data/tmp', parent=True)

    # npc_heroes.txt
    npc_hero_file = dota2_path + '/game/dota/scripts/npc/npc_heroes.txt'
    shutil.copy2(npc_hero_file, dota2_data)

    # dota_english.txt
    f_path = 'resource/localization/dota_english.txt'
    decompile_dota2_package(dota2_path, f_path)
    shutil.copy2(f'{tmp_path}/{f_path}', dota2_data)

    # dota_schinese.txt
    f_path = 'resource/localization/dota_schinese.txt'
    decompile_dota2_package(dota2_path, f_path)
    shutil.copy2(f'{tmp_path}/{f_path}', dota2_data)


def process_dota2_content(dota2_path):
    prepare_dota2_resource(dota2_path)
    extract_hero_name()
    extract_hero_roles()


if __name__ == '__main__':
    DOTA2_PATH = r'C:\Software\Steam\steamapps\common\dota 2 beta'
    process_dota2_content(DOTA2_PATH)
