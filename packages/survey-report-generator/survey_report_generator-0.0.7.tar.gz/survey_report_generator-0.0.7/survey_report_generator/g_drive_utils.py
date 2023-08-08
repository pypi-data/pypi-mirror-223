import io
import os
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools
from http.client import IncompleteRead


def generate_credentials():
    '''Handles login, and then passes on credentials for the connection to be started'''
    SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
    if not os.path.exists('survey_report_generator/storage.json') and os.path.exists('~/storage.json'):
        store = file.Storage('~/storage.json')
    else:
        store = file.Storage('survey_report_generator/storage.json')
    creds = store.get()
    # Get credentials according to either https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev
    # or https://codelabs.developers.google.com/codelabs/gsuite-apis-intro/#6
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return creds


def get_gdrive_connection():
    '''actually provides the connection to the API for use elsewhere'''
    creds = generate_credentials()
    DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))
    return DRIVE


def download_file(DRIVE, file_id):
    """Downloads a file
    Args:
        file_id: ID of the file to download
    Returns : IO object with location.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    # creds, _ = google.auth.default()

    try:
        # create drive api client
        # service = build('drive', 'v3', credentials=creds)

        # file_id = file_id

        # pylint: disable=maybe-no-member
        request = DRIVE.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')

    except HttpError as error:
        print(f'HTTP error occurred: {error}, with file {file_id}')
        file = None
    except IncompleteRead as error:
        print(f'IncompleteRead error occurred: {error}, with file {file_id}')
        file = None

    return file


def get_drive_file_list(connection, query, fields, drive_id):
    files = []
    page_token = None
    while True:
        # pylint: disable=maybe-no-member
        response = connection.files().list(q=query,
                                           spaces='drive',
                                           fields=f'nextPageToken, {fields}',
                                           pageToken=page_token,
                                           pageSize=1000,
                                           supportsAllDrives=True,
                                           includeItemsFromAllDrives=True,
                                           corpora='drive',
                                           driveId=drive_id).execute()
        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files
