# Generates Filtered CSV for upload_to_kennel script and session_json script or
# Kennel Upload Log for the Table of Contents in Kennel bucket

# ****** Version History *******
#   1.1 
#   Added logic for Hanguk Study
#   1.2 
#   Added user input error handling

import pandas as pd
from pprint import pprint
import numpy as np
from os import path

pd.set_option('display.max_columns', None)


def delete_blank_rows(df):
    df['Path'].replace('', np.nan, inplace=True)
    df.dropna(subset=['Path'], inplace=True)
    # pprint(df.head())


def fill_x_rows(df):
    df['Date'].replace('', np.nan, inplace=True, limit=6)
    df['Room'].replace('', np.nan, inplace=True, limit=6)
    df['Build'].replace('', np.nan, inplace=True, limit=6)
    df['Subject ID'].replace('', np.nan, inplace=True, limit=6)
    df['Mask'].replace('', np.nan, inplace=True, limit=6)
    df['Native Speaker'].replace('', np.nan, inplace=True, limit=6)

    df[['Date', 'Room', 'Build', 'Subject ID', 'Mask', 'Native Speaker']] = df[
        ['Date', 'Room', 'Build', 'Subject ID', 'Mask', 'Native Speaker']].fillna(
        method='ffill', limit=6)


def fill_in_info(df):
    df.fillna(method='ffill', inplace=True)


def generate_filtered_csv(df):
    df.drop(columns=['Date', 'Timestamps', 'Time', 'Stage', 'Moderator(s)', 'Session', 'Utterances Recorded',
                     'Target', 'Still Needed Per Use Case', 'Starting From', 'Issue Tags', 'Notes', 'Kennel Link',
                     'Redo'], inplace=True)
    df.to_csv(path.join(path.expanduser('~'), 'Downloads', 'zhongguo_session_sheets_filtered.csv'), index=False)


def generate_upload_csv(df):
    df.drop(columns=['Date', 'Timestamps', 'Time', 'Stage', 'Moderator(s)', 'Session', 'Utterances Recorded',
                     'Target', 'Still Needed Per Use Case', 'Starting From', 'Issue Tags', 'Notes', 'Path',
                     'Redo'], inplace=True)
    df.to_csv(path.join(path.expanduser('~'), 'Downloads', 'zhongguo_upload_log.csv'), index=False)


def generate_filtered_csv_hanguk(df):
    df.drop(columns=['Date', 'Participant #', 'ICF', 'Moderator(s)', 'Timestamps', 'Time', 'Stage',
                     'Timeout', 'Last Prompt Recorded', 'Total Prompts Recorded',
                     'Total Time (per session)', 'Issue Tags', 'Issue Description/Notes', 'Post Study Survey Completed',
                     'Kennel Link'], inplace=True)
    df.to_csv(path.join(path.expanduser('~'), 'Downloads', 'hanguk_session_sheets_filtered.csv'), index=False)


def generate_upload_csv_hanguk(df):
    df.drop(columns=['Date', 'Participant #', 'ICF', 'Moderator(s)', 'Timestamps', 'Time', 'Stage',
                     'Scenario', 'Timeout', 'Last Prompt Recorded', 'Reverse Order', 'Total Prompts Recorded',
                     'Total Time (per session)', 'Issue Tags', 'Issue Description/Notes', 'Path',
                     'Post Study Survey Completed'], inplace=True)
    df.to_csv(path.join(path.expanduser('~'), 'Downloads', 'hanguk_upload_log.csv'), index=False)


def choose_study():
    study = input('Which study CSV would you like?\n 1: Zhongguo Study\n 2: Hanguk Study\n')
    return study


def choose_csv():
    for i in range(5):
        study = choose_study()
        if study not in ("1", "2"):
            print('Invalid answer. Please choose 1 or 2.')
        else:
            while True:
                answer = input('Which CSV would you like to generate?\n A: Filtered CSV\n B: Upload Log\n')
                if answer in ('A', 'a') and study == "1":
                    generate_filtered_csv(df_yeet)
                    pprint(df_yeet.head())
                    print('CSV generated.')
                    exit()
                elif answer in ('B', 'b') and study == "1":
                    generate_upload_csv(df_yeet)
                    pprint(df_yeet.head())
                    print('CSV generated.')
                    exit()
                elif answer in ('A', 'a') and study == "2":
                    generate_filtered_csv_hanguk(df_yeet)
                    pprint(df_yeet.head())
                    print('CSV generated.')
                    exit()
                elif answer in ('B', 'b') and study == "2":
                    generate_upload_csv_hanguk(df_yeet)
                    pprint(df_yeet.head())
                    print('CSV generated.')
                    exit()
                else:
                    print('Invalid entry. Please choose A or B.')
                    i += 1
                    if i > 5:
                        result = input('You seem confused. Do you want to exit? (y/n)')
                        if result not in ('Y', 'y'):
                            continue
                        else:
                            exit()


if __name__ == '__main__':

    # User input for session log
    session_log = input('Please paste the full path to your session log below:\n')

    df_yeet = pd.DataFrame(pd.read_excel(f'{session_log}',
                                         sheet_name="Session Log", skiprows=1))

    # Perform initial formatting
    print('Processing spreadsheet...')

    # Applies to Hanguk study only
    if df_yeet['Stage'].eq('Session Start').any():
        fill_x_rows(df_yeet)

    # **** Code Check ****
    # print('After fill_x_rows:')
    # print(df_yeet[['Date', 'Room', 'Subject ID', 'Mask', 'Native Speaker', 'Stage', 'Path']].head(12))

    delete_blank_rows(df_yeet)
    fill_in_info(df_yeet)

    # **** Code Check ****
    # print('After delete & fill:')
    # print(df_yeet[['Date', 'Room', 'Subject ID', 'Mask', 'Native Speaker','Stage', 'Path']].head(12))

    # Choose which study you want and which CSV you want to generate
    choose_csv()
