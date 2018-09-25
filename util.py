def get_path(name='log', abspath=None, relative_path=None, _file=None):
    """Create path if path don't exist
    Args:
        name: folder name
        abspath: absolute path to be prefix
        relative_path: relative path that can be convert into absolute path
        _file: use directory based on _file
    Returns: Path of the folder
    """
    import os
    if abspath:
        directory = os.path.abspath(os.path.join(abspath, name))
    elif relative_path:
        directory = os.path.abspath(os.path.join(
            os.path.abspath(relative_path), name))
    else:
        if _file:
            directory = os.path.abspath(
                os.path.join(os.path.dirname(_file), name))
        else:
            directory = os.path.abspath(
                os.path.join(os.path.dirname(__file__), name))
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def generate_hero_json():
    import json

    with open('data.json') as f:
        data = json.load(f)
    print(data.keys())


def main():
    generate_hero_json()


if __name__ == '__main__':
    main()
