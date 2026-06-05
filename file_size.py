import os
import sys

def formatting_input(prefix,digit):
    # 指定の接頭語を大文字に変換（小文字での指定対応）
    prefix = prefix.upper()
    # 接頭語をbyte/*Bに統一
    if(prefix.endswith(('B','byte')) != True):
        prefix = prefix+'B'

    # 四捨五入桁を整数に変更
    digit = int(digit)
    return prefix,digit

def get_file_size_str(file_path, prefix='K', digit=2):
    prefix,digit = formatting_input(prefix,digit)
    return str(get_file_size(file_path, prefix, digit))+' '+prefix

def get_file_size(file_path, prefix='KB', digit=0):
    # ファイルサイズを取得
    file_size = os.path.getsize(file_path)

    prefix,digit = formatting_input(prefix,digit)

    if(prefix == 'K' or prefix == 'KB'):
        # KB
        file_size = round(file_size/1024, digit)
    elif(prefix == 'M' or prefix == 'MB'):
        # MB
        file_size = round(file_size/1024**2, digit)
    elif(prefix == 'G' or prefix == 'GB'):
        # GB
        file_size = round(file_size/1024**3, digit)
    elif(prefix == 'T' or prefix == 'TB'):
        # GB
        file_size = round(file_size/1024**4, digit)
    else:
        # byte
        file_size = round(file_size)

    if(digit == 0):
        return round(file_size)
    else:
        return file_size

def main(input):
    print(input)
    if(2 <= len(input) & len(input) <= 4):
        if(len(input) == 2):
            file = input[1]
            print(get_file_size_str(file))
            print(get_file_size(file))
        elif(len(input) == 3):
            file = input[1]
            prefix = input[2]
            print(get_file_size_str(file,prefix))
            print(get_file_size(file,prefix))
        elif(len(input) == 4):
            file = input[1]
            prefix = input[2]
            digit = input[3]
            print(get_file_size_str(file,prefix,digit))
            print(get_file_size(file,prefix,digit))
    else:
        print('fileSize.py "file/to/path" "KB/MB/GB/TB/null" "digit number"')

if __name__ == '__main__':
    args = sys.argv
    main(args)
