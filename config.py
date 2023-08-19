from pathlib import Path

from environs import Env

path_root = Path(__file__).resolve().parent

env = Env()
env.read_env()

token = env.str('token')
path_posters = env.str('path_posters')
path_base_y_disc = '/Компьютер HOME-PC/Ready pdf compress'