# coding=cp949

import os
import csv


def get_main_csv() -> dict:
    csv_data = dict()

    def is_main_app() -> str:
        if os.path.basename(os.path.abspath("./")) != "py":
            base_dir = os.path.abspath(f"./resource/voca")
        else:
            base_dir = os.path.abspath(f"../voca")

        return base_dir

    def get_unique_group_name(dict_values, key_name):
        return list(set(dict_values[key_name]))

    base_path = is_main_app()
    csv_file = os.path.join(base_path, 'WordList.csv')

    dataframe = dict()
    keys = list()

    for encoding in ['cp949', 'utf-8', 'EUC-KR']:
        try:
            with open(csv_file, 'r', encoding=encoding) as file:
                lines = csv.reader(file)
                for idx, line in enumerate(lines):
                    if idx == 0:
                        column_count = len(line)
                        keys = line
                        for key in keys:
                            dataframe[key] = list()
                    else:
                        if len(line) < column_count:
                            add_none = [None] * (column_count - len(line))
                            line.extend(add_none)

                        for idx_item in range(column_count):
                            key = keys[idx_item]
                            value = line[idx_item]
                            if key == "en" and value == '':
                                # index 명으로 한 줄을 날렸으므로 -1 해줘야 함.
                                dataframe[keys[0]].pop(idx - 1)
                                break
                            dataframe[key].append(value)

                print(dataframe)
            break
        except UnicodeDecodeError as e:
            print("  [Error] Enconding problem occurred.. ")

    print(dataframe)

    unique_name = get_unique_group_name(dataframe, keys[0])
    unique_name.sort()

    csv_data["dataframe"] = dataframe
    csv_data["unique_name"] = unique_name

    return csv_data