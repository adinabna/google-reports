from datetime import (
    datetime,
    timedelta
)

from os.path import (
    join,
    abspath,
    dirname
)

from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery

# If modifying the scope, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SHEET_SCOPE = 'https://www.googleapis.com/auth/spreadsheets'
SHEETS_API = 'sheets'
SHEETS_VERSION = 'v4'

DRIVE_SCOPE = 'https://www.googleapis.com/auth/drive'
DRIVE_API = 'drive'
DRIVE_VERSION = 'v3'

SERVICE_ACCOUNT_SECRET_FILE = join(abspath(dirname(__file__)), 'service_account_secret.json')

FOLDER_MIME = 'application/vnd.google-apps.folder'

SPREADSHEET_NAME = 'My spreadhseet\'s name '

# TODO: change to whatever role you want to grant to the whole domain (https://developers.google.com/drive/v3/reference/permissions)
PERMISSION_ROLE = 'commenter'
PERMISSION_TYPE = 'domain'
# TODO: to change!
DOMAIN = 'YOUR_DOMAIN'

def get_credentials():
    return ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_ACCOUNT_SECRET_FILE, [SHEET_SCOPE, DRIVE_SCOPE])

def _get_service(credentials, api, version):
    return discovery.build(api, version, credentials=credentials)

def get_sheet_service(credentials):
    return _get_service(credentials, SHEETS_API, SHEETS_VERSION)

def get_drive_service(credentials):
    return _get_service(credentials, DRIVE_API, DRIVE_VERSION)

def generate_google_sheet(service, drive_service, spreadsheet_name, sheet_details, folder_name):
    sheet_name = sheet_details['name']
    sheet_range = sheet_details['range']
    values = sheet_details['values']
    columns_count = sheet_details['columns_count']
    final_spreadsheet_name = spreadsheet_name + datetime.now().isoformat()

    spreadsheet_id = _generate_spreadsheet(service, final_spreadsheet_name)

    sheet_id = _update_sheet_details(service, spreadsheet_id, sheet_name)
    body = {'values': values}
    service.spreadsheets().values().update(spreadsheetId=spreadsheet_id,
                                           range=sheet_name+sheet_range,
                                           valueInputOption='RAW',
                                           body=body).execute()
    _format_sheet(service, sheet_id, spreadsheet_id, columns_count, len(values))

    _update_permissions(drive_service, spreadsheet_id)
    folder_id = _identify_folder(drive_service, folder_name)
    _move_to_folder(drive_service, spreadsheet_id, folder_id)
    _update_permissions(drive_service, folder_id)

    return {
        'folder': 'https://drive.google.com/open?id={}'.format(folder_id),
        'file': 'https://docs.google.com/spreadsheets/d/{}'.format(spreadsheet_id)
    }

def _identify_folder(drive_service, folder_name):
    folder_id = _find_folder(drive_service, folder_name)
    if not folder_id:
        folder_id = _create_folder(drive_service, folder_name)

    return folder_id

def _find_folder(drive_service, folder_name):
    query = "name='{}' and mimeType='{}' and trashed=false".format(folder_name, FOLDER_MIME)
    files = find_files(drive_service, query)
    for found_file in files:
        if found_file.get('name') == folder_name:
            return found_file.get('id')
    return None

def find_files(drive_service, query):
    page_token = None
    files = []
    while True:
        if query:
            response = drive_service.files().list(q=query,
                                                  spaces='drive',
                                                  fields='nextPageToken, files(id, name)',
                                                  pageToken=page_token).execute()
        else:
            response = drive_service.files().list(pageToken=page_token).execute()
        files += response.get('files', [])
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files

def find_files_older_than_n_days(drive_service, days):
    n_weeks_ago = datetime.now() - timedelta(days=int(days))
    query = "modifiedTime < '{}' and mimeType!='{}' and name contains '{}'".format(
        n_weeks_ago.isoformat(), FOLDER_MIME, SPREADSHEET_NAME)
    files = find_files(drive_service, query)
    return [found_file.get('id') for found_file in files]

def delete_files(drive_service, file_ids):
    for file_id in file_ids:
        drive_service.files().delete(fileId=file_id).execute()

def _create_folder(drive_service, folder_name):
    file_metadata = {
        'name': folder_name,
        'mimeType': FOLDER_MIME
    }
    drive_file = drive_service.files().create(body=file_metadata,
                                              fields='id').execute()
    return drive_file.get('id')

def _move_to_folder(drive_service, file_id, folder_id):
    # Retrieve the existing parents to remove
    drive_file = drive_service.files().get(fileId=file_id,
                                           fields='parents').execute()
    previous_parents = ",".join(drive_file.get('parents'))
    # Move the file to the new folder
    drive_service.files().update(fileId=file_id,
                                 addParents=folder_id,
                                 removeParents=previous_parents,
                                 fields='id, parents').execute()

def _update_permissions(drive_service, file_id):
    permission_details = {
        'type': PERMISSION_TYPE,
        'role': PERMISSION_ROLE,
        'domain': DOMAIN,
        'allowFileDiscovery': 'true'
    }
    return drive_service.permissions().create(fileId=file_id,
                                              body=permission_details).execute()

def _generate_spreadsheet(service, spreadsheet_name):
    spreadsheet_body = {
        'properties': {
            'title': spreadsheet_name
        }
    }

    result = service.spreadsheets().create(body=spreadsheet_body).execute()
    return result['spreadsheetId']

def _update_sheet_details(service, spreadsheet_id, new_sheet_name):
    sheet_id = 0
    sheet_body = {
        'requests': [
            {
                'updateSheetProperties':{
                    'properties': {
                        'sheetId': sheet_id,
                        'title': new_sheet_name,
                    },
                    'fields': 'title',
                }
            }
        ]
    }

    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                       body=sheet_body).execute()
    return sheet_id

def _format_sheet(service, sheet_id, spreadsheet_id, columns_count, rows_count):
    header_properties = {
        'requests': [
            {
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id,
                        'endRowIndex': 1
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'horizontalAlignment' : 'CENTER',
                            'textFormat': {
                                'fontSize': 10,
                                'bold': 'true'
                            }
                        }
                    },
                    'fields': 'userEnteredFormat(textFormat,horizontalAlignment)'
                }
            },
            {
                'updateSheetProperties': {
                    "properties": {
                        "sheetId": sheet_id,
                        "gridProperties": {
                            "frozenRowCount": 1
                        }
                    },
                    'fields': 'gridProperties.frozenRowCount'
                }
            },
            {
                'autoResizeDimensions': {
                    'dimensions': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': 0,
                        'endIndex': columns_count
                    }
                }
            },
            {
                'autoResizeDimensions': {
                    'dimensions': {
                        'sheetId': sheet_id,
                        'dimension': 'ROWS',
                        'startIndex': 0,
                        'endIndex': rows_count
                    }
                }
            }
        ]}

    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                       body=header_properties).execute()
