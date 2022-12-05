# This code was used to add session metadata to data collected during user study sessions before uploading
# Version History
# 1.1
#   Added logic for generating metadata for Hanguk Study
#   Added logic for choosing a study
#   Updated dictionary for Hanguk Study
# 1.1
#   Adds metadata for User Study 2
#   Includes logic for picking a study
#   Includes updated dictionary for User Study 2
# 1.2
#   Added mapping to reverse order dictionary to account for reverse scenarios

import json
import os
from os import path
import pandas as pd
from pprint import pprint

DEFAULT_SESSION_DICT = {
    "device": {
        "model": "iPhone 13 Pro Max",
        "name": "TheEnigma",
    },
    "endDate": "",
    "notes": "",
    "rawDataFileCount": 0,
    "startDate": "",
    "study": {},
    "subject": {
        "gender": "",
        "id": "",
        "nativeLanguageId": ""
    }
}

JSON_MAP_CHINESE = {
    'HaiQ1': 'zh_CN_Study_HaiQ1',
    'HaiQ2': 'zh_CN_Study_HaiQ2',
    'HaiQ3': 'zh_CN_Study_HaiQ3',
    'HaiQ4': 'zh_CN_Study_HaiQ4',
    'NHQ1': 'zh_CN_Study_NHQ1',
    'NHQ2': 'zh_CN_Study_NHQ2',
    'NHQ3': 'zh_CN_Study_NHQ3',
    'NHQ4': 'zh_CN_Study_NHQ4'}

JSON_MAP_KOREAN = {
    1.0: 'Hanguk_scenario-1',
    2.0: 'Hanguk_Scenario-2',
    3.0: 'Hanguk_scenario-3',
}

KEY_MAP = {'faceMask': {'Y': 'on',
                        'N': 'off'},
           'nativeSpeaker': {'Y': 'native',
                             'N': 'non-native'},
           'room': {'korean': {'SLab': 'seoul-lab1',
                               'BLab': 'busan-lab2',
                               'JLab': 'jeju-lab3'},
                    'chinese': {'TaiLab': 'taipei-01',
                                'HKLab': 'hongkong-03'}}
           }

REVERSE_ORDER_DICT = {
    1.0: 'Hanguk_scenario-1_Rev',
    2.0: 'Hanguk_scenario-2',
    3.0: 'Hanguk_scenario-3',
}


def set_subject_id(df_row):
    subject_id = df_row['Subject ID']
    return subject_id


def id_json_file_zh(df_row):
    identifier = df_row['Trigger'] + df_row['Section']
    for key in JSON_MAP_CHINESE:
        if identifier == key:
            json_file = JSON_MAP_CHINESE[identifier]
            return json_file


def id_json_file_kr(df_row):
    identifier = df_row['Scenario']
    for key in JSON_MAP_KOREAN:
        if df_row['Reverse Order'] == "Y":
            json_file = REVERSE_ORDER_DICT[identifier]
            return json_file
        if identifier == key:
            json_file = JSON_MAP_KOREAN[identifier]
            return json_file


def check_session_json(target_dir):
    return path.exists(path.join(target_dir, 'session.json'))


def choose_study(df_row, study_choice):
    while True:

        if study_choice in ("A", "a"):
            study_json_file = path.join(path.expanduser('~'), 'Desktop/Portfolio_copy/Zhongguo_Study_Dependencies'
                                                              '/scripts', id_json_file_zh(df_row) + '.json')
            break
        elif study_choice in ("B", "b"):
            study_json_file = path.join(path.expanduser('~'), 'Desktop/Portfolio_copy/Hanguk_Study_Dependencies'
                                                              '/scripts', id_json_file_kr(df_row) + '.json')
            break
        else:
            print("Invalid entry. Please choose A or B")

    return study_json_file


def generate_session_json(df_row, study_json_file):
    subject_id = set_subject_id(df_row)
    print(subject_id)
    print(study_json_file)
    with open(study_json_file, 'r') as f:
        study_data = json.load(f)
    DEFAULT_SESSION_DICT['study'] = study_data
    if subject_id:
        DEFAULT_SESSION_DICT['subject']['id'] = subject_id
        DEFAULT_SESSION_DICT['recreated_session_json'] = True
    output_path = str(os.path.join(df_row['Path'], 'session.json'))
    print(output_path)
    with open(output_path, 'w') as f:
        json.dump(DEFAULT_SESSION_DICT, f, indent=4)
    return output_path


def set_metainfo(df_row, study_choice):
    language_map = {'A': 'chinese',
                    'B': 'korean'}
    try:
        with open(path.join(df_row['Path'], 'session.json'), 'r') as f:
            session_data = json.load(f)
            metainfo = {'faceMask': KEY_MAP['faceMask'][df_row['Mask']],
                        'native': KEY_MAP['nativeSpeaker'][df_row['Native Speaker']],
                        'room': KEY_MAP['room'][language_map[study_choice.upper()]][df_row['Room']]
                        }
            build = f"1.0 ({df_row['Build']})"
            session_data['metainfo'] = metainfo
            session_data['device']['systemVersion'] = build
            with open(path.join(df_row['Path'], 'session.json'), 'w', encoding="utf-8") as f:
                json.dump(session_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(e)
        print("""
         ⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣠⣤⣶⣶
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢰⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣀⣀⣾⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⡏⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿
        ⣿⣿⣿⣿⣿⣿⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠁⠀⣿
        ⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠙⠿⠿⠿⠻⠿⠿⠟⠿⠛⠉⠀⠀⠀⠀⠀⣸⣿
        ⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣴⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢰⣹⡆⠀⠀⠀⠀⠀⠀⣭⣷⠀⠀⠀⠸⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠈⠉⠀⠀⠤⠄⠀⠀⠀⠉⠁⠀⠀⠀⠀⢿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⢾⣿⣷⠀⠀⠀⠀⡠⠤⢄⠀⠀⠀⠠⣿⣿⣷⠀⢸⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⡀⠉⠀⠀⠀⠀⠀⢄⠀⢀⠀⠀⠀⠀⠉⠉⠁⠀⠀⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿
                """)
        exit()


if __name__ == '__main__':
    # User input for CSV file - enter either the upload
    csv_file = input('Please enter the full path to your csv:\n')

    df = pd.read_csv(f'{csv_file}')
    study = input('Which study are you generating for?\n A: chinese (zh)\n B: korean (kr)\n')
    for idx, row in df.iterrows():
        study_json = choose_study(row, study)
        if not check_session_json(row['Path']):
            print('No json found. Generating session json...')
            generate_session_json(row, study_json)
        set_metainfo(row, study)
