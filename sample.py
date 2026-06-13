import os
from pathlib import Path
import argparse
import sys
from file_size import get_file_size_str,get_file_size
from mkdir_datetime import mkdir_dt,get_today_date,get_now_time

# 標準出力をUTF-8に再設定（Windows環境での文字化け対策）
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# stdout をファイルと元のストリームに同時に書き出すラッパー
class _Tee:
    def __init__(self, stream, filepath: str):
        # 元ストリームを行バッファリングに設定してからラップ
        if hasattr(stream, 'reconfigure'):
            # バイナリモード（rb/wb/ab）でなければ行バッファリングを設定
            mode = getattr(stream, 'mode', 'w')
            if mode not in ('rb', 'wb', 'ab'):
                try:
                    stream.reconfigure(line_buffering=True)
                except Exception:
                    pass
        self._stream = stream
        self._file = open(filepath, "w", encoding="utf-8", buffering=1)

    def write(self, data):
        self._stream.write(data)
        self._file.write(data)

    def flush(self):
        self._stream.flush()
        self._file.flush()

    def close(self):
        self._file.close()

    # sys.stdout が持つ属性に委譲（subprocess等の互換性のため）
    def __getattr__(self, name):
        return getattr(self._stream, name)
    
# ──────────────────────────────────────────
# 実行
# ──────────────────────────────────────────
def main():
    args = do_arg_parse()
    dbg_dir_path = None
    
    # デバッグモードの場合、標準出力をファイルにも保存するためのクラス
    if args['debug']:
        import sys
        dbg_dir_path = Path(mkdir_dt())  # デバッグ用にフォルダ作成
        log_path = dbg_dir_path / (Path(args['output']).stem + "_debug.log")
        _tee = _Tee(sys.stdout, log_path)  # reconfigure もここで完結
        sys.stdout = _tee
        print(f'デバッグモードが有効です。 {dbg_dir_path} に保存されます。', flush=True)

    print(f'====== {PROGRAM_TITLE} ======', flush=True)
    print('                  v.0.0.1', flush=True)
    print(f'指定された引数: {args}', flush=True)
    print('実行日時: ' + get_today_date() + ' ' + get_now_time(), flush=True)
    print('ファイル存在チェック:', flush=True)
    for key, value in args.items():
        if isinstance(value, str) and value.endswith(('.csv', '.CSV')):
            if not os.path.exists(value):
                print(f'  - {key}: {value} が存在しません', flush=True)
            else:
                print(f'  - {key}: {value} が存在します', flush=True)
                print(f'    ファイルサイズ(KB): {get_file_size(value)}', flush=True)
                print(f'    ファイルサイズ(文字列): {get_file_size_str(value)}', flush=True)

    if args['debug']:
        print('--- デバッグモード', flush=True)
        save_ini(dbg_dir_path / 'config.ini', args)  # デバッグ用に現在の設定値をiniとして保存
        for key, value in args.items():
            if isinstance(value, str) and value.endswith(('.csv', '.CSV')):
                if os.path.exists(value):
                    # デバッグ用にファイルをコピー
                    import shutil
                    dest_path = dbg_dir_path / os.path.basename(value)
                    shutil.copy2(value, dest_path)
                    print(f'  - {key}: {value} を {dest_path} にコピーしました。', flush=True)

# 相対パス取得
def get_relative_path(filePath):
    from pathlib import Path
    if(Path(filePath).is_absolute()):
        return Path(filePath).relative_to(Path.cwd())
    else:
        return filePath

# 絶対パス取得
def get_absolute_path(filePath):
    from pathlib import Path
    if(Path(filePath).is_absolute()):
        return filePath
    else:
        return Path(filePath).resolve()

# 引数解析
def do_arg_parse() -> dict:
    parser = build_parser(ARG_DESCRIPTION)
    args = parser.parse_args()
    arg_dict = vars(args)
    config_path = arg_dict.pop('config')
    ini_dict = load_ini(config_path)

    # 優先順位: 引数 > ini > デフォルト
    merged = {}
    for opt in OPTION_DEFS:
        key = opt['name']
        if arg_dict.get(key) is not None:
            merged[key] = arg_dict[key]
        elif key in ini_dict:
            merged[key] = ini_dict[key]
        else:
            merged[key] = opt['default']

    # 必須チェック
    for opt in OPTION_DEFS:
        if opt['required'] and not merged.get(opt['name']):
            parser.error(f'--{opt["name"]} が指定されていません（引数またはiniファイルで設定してください）')

    # iniファイルが存在しない場合は現在の設定値で生成する
    if Path(config_path).exists()==False:
        save_ini(config_path, merged)

    return merged


# ──────────────
# オプション定義
# ──────────────
from external_define import OPTION_DEFS, ARG_DESCRIPTION, CONFIG_DEFAULT, PROGRAM_TITLE

# ──────────────
# INIファイルの読み書き関数
# ──────────────
from external_define import load_ini, save_ini

# OPTION_DEFSからargparseを生成
def build_parser(desc=ARG_DESCRIPTION) -> argparse.ArgumentParser:
    import argparse
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--config', default=CONFIG_DEFAULT, help='設定ファイルパス')

    for opt in OPTION_DEFS:
        if opt['store_true']:
            parser.add_argument(f'--{opt["name"]}', action=argparse.BooleanOptionalAction, default=None, help=opt['help'])
        else:
            parser.add_argument(f'--{opt["name"]}', type=opt['type'], default=None, help=opt['help'])

    return parser


if __name__ == '__main__':
    main()