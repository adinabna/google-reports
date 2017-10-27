#!/usr/bin/env python

import string
import argparse
import traceback

from os.path import (
    join,
    abspath,
    dirname
)

from google import (
    get_credentials,
    get_sheet_service,
    get_drive_service,
    generate_google_sheet,
    SPREADSHEET_NAME
)

COLUMN_RANGES = string.ascii_uppercase
# TODO: this number will represent the number of column for your input data
COLUMNS_COUNT = 9
SHEET_NAME = "My first sheet"

def main():
    credentials = get_credentials()
    service = get_sheet_service(credentials)
    drive_service = get_drive_service(credentials)

    args = _get_args()
    settings = _make_settings(args)

    _generate_report(settings, service, drive_service)

def _print_data(data):
    folder_link = data['folder']
    file_link = data['file']
    print('Folder link: {}'.format(folder_link))
    print('File link: {}'.format(file_link))

def _generate_report(settings, service, drive_service, folder_name):
    spreadsheet_details = {
        'sheet_name': SHEET_NAME,
        'name': SPREADSHEET_NAME,
        'sheet_values': report_data,
        'columns_count': COLUMNS_COUNT
    }
    return _build_sheet(service, drive_service, spreadsheet_details, folder_name)

def _build_sheet(service, drive_service, spreadsheet_details, folder_name):
    report_data = spreadsheet_details['sheet_values']
    row_number = len(report_data)
    columns_count = spreadsheet_details['columns_count']
    sheet_range = '!A1:{}{}'.format(COLUMN_RANGES[columns_count], row_number)

    sheet_details = {
        'name': spreadsheet_details['sheet_name'],
        'range': sheet_range,
        'values': report_data,
        'columns_count': columns_count
    }

    return generate_google_sheet(service,
                                 drive_service,
                                 spreadsheet_details['name'],
                                 sheet_details,
                                 folder_name)

if  __name__ == '__main__':
    main()
