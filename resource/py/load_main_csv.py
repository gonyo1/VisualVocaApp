import os
import csv
import pandas as pd


def get_main_csv() -> dict:
    csv_data = dict()

    def is_main_app() -> str:
        if os.path.basename(os.path.abspath("./")) != "py":
            base_dir = os.path.abspath(f"./resource/voca")
        else:
            base_dir = os.path.abspath(f"../voca")

        return base_dir

    def get_unique_group_name(dataframe):
        return dataframe["그룹"].unique()

    base_path = is_main_app()
    csv_file = f'{base_path}\\Word_List.csv'
    dataframe = pd.read_csv(csv_file, encoding='cp949')
    unique_name = get_unique_group_name(dataframe)

    csv_data["dataframe"] = dataframe
    csv_data["unique_name"] = unique_name

    return csv_data