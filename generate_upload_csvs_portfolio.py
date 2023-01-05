# Generates Filtered CSV for upload script and session_json script or
# Upload Log for the Table of Contents in upload bucket

# ****** Version History *******
#   1.1 
#   Added logic for Hanguk Study
#   1.2 
#   Added user input error handling
#   1.3
#   Modified error handling
#   Added MismatchError
#   Simplified logic for calling functions

import pandas as pd
from pprint import pprint
import numpy as np
from os import path

pd.set_option('display.max_columns', None)

zh_columns = ['Date', 'Room', 'Build', 'Timestamps', 'Time', 'Stage', 'Subject ID', 'Moderator(s)', 'Native Speaker',
              'Mask', 'Session', 'Trigger', 'Background Noise', 'Imposter', 'Section', 'Utterances Recorded', 'Target',
              'Still Needed Per Use Case', 'Starting From', 'Issue Tags', 'Notes', 'Path', 'Kennel Link', 'Redo']

hg_columns = ['Date', 'Room', 'Build', 'Subject ID', 'Participant #', 'ICF', 'Moderator(s)', 'Mask', 'Native Speaker',
              'Timestamps', 'Stage', 'Time', 'Scenario', 'Timeout', 'Last Prompt Recorded', 'Reverse Order',
              'Total Prompts Recorded',
              'Total Time (per session)', 'Issue Tags', 'Issue Description/Notes', 'Post Study Survey Completed',
              'Path', 'Kennel Link']

class MismatchError(Exception):
    """Raises error when user calls the incorrect function for the input Excel sheet. For example,
    generate_filtered_csv can only be used with the Zhongguo Study Excel file, while generate_filtered_csv_hanguk must
    be used with the Hanguk Study Excel file.
    """
    pass


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
    headers = list(df.columns)
    if headers not in zh_columns:
        raise MismatchError
        
    df.drop(columns=['Date', 'Timestamps', 'Time', 'Stage', 'Moderator(s)', 'Session', 'Utterances Recorded',
                     'Target', 'Still Needed Per Use Case', 'Starting From', 'Issue Tags', 'Notes', 'Kennel Link',
                     'Redo'], inplace=True)
    df.to_csv(path.join(path.expanduser('~'), 'Downloads', 'zhongguo_session_sheets_filtered.csv'), index=False)


def generate_upload_csv(df):
    headers = list(df.columns)
    if headers not in zh_columns:
        raise MismatchError
        
    df.drop(columns=['Date', 'Timestamps', 'Time', 'Stage', 'Moderator(s)', 'Session', 'Utterances Recorded',
                     'Target', 'Still Needed Per Use Case', 'Starting From', 'Issue Tags', 'Notes', 'Path',
                     'Redo'], inplace=True)
    df.to_csv(path.join(path.expanduser('~'), 'Downloads', 'zhongguo_upload_log.csv'), index=False)


def generate_filtered_csv_hanguk(df):
    headers = list(df.columns)
    if headers not in hg_columns:
        raise MismatchError
        
    df.drop(columns=['Date', 'Participant #', 'ICF', 'Moderator(s)', 'Timestamps', 'Time', 'Stage',
                     'Timeout', 'Last Prompt Recorded', 'Total Prompts Recorded',
                     'Total Time (per session)', 'Issue Tags', 'Issue Description/Notes', 'Post Study Survey Completed',
                     'Kennel Link'], inplace=True)
    df.to_csv(path.join(path.expanduser('~'), 'Downloads', 'hanguk_session_sheets_filtered.csv'), index=False)


def generate_upload_csv_hanguk(df):
    headers = list(df.columns)
    if headers not in hg_columns:
        raise MismatchError
        
    df.drop(columns=['Date', 'Participant #', 'ICF', 'Moderator(s)', 'Timestamps', 'Time', 'Stage',
                     'Scenario', 'Timeout', 'Last Prompt Recorded', 'Reverse Order', 'Total Prompts Recorded',
                     'Total Time (per session)', 'Issue Tags', 'Issue Description/Notes', 'Path',
                     'Post Study Survey Completed'], inplace=True)
    df.to_csv(path.join(path.expanduser('~'), 'Downloads', 'hanguk_upload_log.csv'), index=False)
   

key_map = {'1': {'A': generate_filtered_csv,
                 'B': generate_upload_csv
                 },
           '2': {'A': generate_filtered_csv_hanguk,
                 'B': generate_upload_csv_hanguk
                 }
           }


def make_selections():
    study = input('Which study CSV would you like?\n 1: Zhongguo Study\n 2: Hanguk Study\n')
    doc = input('Which CSV would you like to generate?\n A: Filtered CSV\n B: Upload Log\n')
    return study, doc


def choose_csv():
    study_choice, doc_choice = make_selections()
    while True:
        try:
            key_map[study_choice][doc_choice.upper()](df_yeet)
            print('CSV generated.')
            break
        except KeyError:
            print('Invalid entry. Please choose 1 or 2 to choose study and A or B to choose document.')
            choose_csv()
            break
        except MismatchError:
            print('Study chosen does not match Excel sheet.')
            break
            

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
