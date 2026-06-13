
from pathlib import Path
import configparser

# ──────────────
# オプション定義
# ──────────────
# タイトル
PROGRAM_TITLE = 'python sample'

# 実行ファイル名
PROGRAM_FILE_NAME = 'sample'

# 説明文
ARG_DESCRIPTION = 'CSVファイルを処理する'

# ファイル参照が必要なキーワード
FILE_KEYWORDS = ("file", "img", "image", "path", "output")

# 引数定義
OPTION_DEFS = [
    #    name           type       default                required        store_true        frame(GUI用)          width(GUI)  help, choices
    dict(name='file',   type=str,  default='input.csv',   required=True,  store_true=False, frame='ファイル設定', width=None, help='入力CSVファイルパス'),
    dict(name='output', type=str,  default='output.csv',  required=True,  store_true=False, frame='ファイル設定', width=None, help='出力CSVファイルパス'),
    dict(name='enc',    type=str,  default='CP932',       required=False, store_true=False, frame='文字コード',   width=None, help='文字エンコーディング（例: CP932, utf-8）'),
    dict(name='token',  type=str,  default='XXXXXX...',   required=True,  store_true=False, frame='API',          width=50,   help='APIトークン'),
    dict(name='method', type=str,  default='GET',         required=True,  store_true=False, frame='API',          width=None, help='HTTPメソッド', choices=['GET','POST','PUT','DELETE']),
    dict(name='column', type=int,  default=3,             required=False, store_true=False, frame='指定カラム',   width=None, help='処理するカラム番号'),
    dict(name='debug',  type=bool, default=False,         required=False, store_true=True,  frame='その他',       width=None, help='デバッグモード'),
]
CONFIG_DEFAULT = "config.ini"

# ──────────────
# iniファイルの読み書き関数
# ──────────────
# OPTION_DEFSの型定義に従ってiniファイルを読み込む
def load_ini(config_path: str) -> dict:
    config = configparser.ConfigParser()
    if not Path(config_path).exists():
        return {}

    config.read(config_path, encoding='utf-8')
    section = 'settings'
    if section not in config:
        return {}

    ini = config[section]
    result = {}

    for opt in OPTION_DEFS:
        key = opt['name']
        if key not in ini:
            continue
        if opt['type'] == int:
            result[key] = ini.getint(key)
        elif opt['type'] == bool or opt['store_true']:
            result[key] = ini.getboolean(key)
        else:
            result[key] = ini[key]

    return result

# 現在の設定値をiniとして書き出す
def save_ini(config_path: str, merged: dict) -> None:
    config = configparser.ConfigParser()
    config['settings'] = {}

    for opt in OPTION_DEFS:
        key = opt['name']
        value = merged.get(key)
        if value is None:
            config['settings'][key] = ''
        else:
            config['settings'][key] = str(value).lower() if isinstance(value, bool) else str(value)

    with open(config_path, 'w', encoding='utf-8') as f:
        config.write(f)
