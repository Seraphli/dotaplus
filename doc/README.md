# DotaPlus Document

## Prepare

1. Install Python 3(3.6.5), and create a virtual environment.
2. (Suggested) Install Pycharm and open project folder.
If you don't want to install Pycharm,
you have to remember to add `PYTHONPATH=.` before you run any script.
And of course, you have to activate your virtual environment before running any script.
For example, if you want to run `script.py`, please use `PYTHONPATH=. python script.py`.

## How to use

### Only update web data

1. Run `scripts/update_web_data.py` to crawl web data.

### Update with a new hero

When a new hero releases, you have to update the hero list before updating the web data.
If I have time, I will update the base data, including image templates and the hero list.
But you also can update these data by yourself.

#### Update necessary data from Dota 2 package

1. Install .Net Core Runtime from [here](https://dotnet.microsoft.com/download).
2. Download `Decompiler.zip` from [here](https://opensource.steamdb.info/ValveResourceFormat/).
3. Extract `Decompiler.zip` into `tools` folder. Make sure `tools/Decompliler/Decompiler.dll` exists.
4. Set `DOTA2_PATH` in `scripts/update_all_hero.py`.
5. Run `scripts/update_all_hero.py`.
6. Run `scripts/update_web_data.py`.

### Usage

After update necessary data from website and Dota 2, the dota plus can provide suggestions for ban pick. 

#### Basic usage

Check out [ban_pick.py](scripts/ban_pick.py).
