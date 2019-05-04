from dpapi.dataproc.dota2trans import process_dota2_content
from dpapi.dataproc.custom_data import process_custom_data

DOTA2_PATH = r'C:\Software\Steam\steamapps\common\dota 2 beta'


def main():
    process_dota2_content(DOTA2_PATH)
    process_custom_data()


if __name__ == '__main__':
    main()
