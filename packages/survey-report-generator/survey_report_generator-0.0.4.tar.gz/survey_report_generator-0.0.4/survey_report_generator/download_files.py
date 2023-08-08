import os
from collections import defaultdict

from .g_drive_utils import get_gdrive_connection, get_drive_file_list, download_file


def download_file_from_filepath(filepath):
    """
    This method takes a filepath and downloads the file using its id

    Args:
        filepath (str): path to the file including the file name
    """
    drive_service = get_gdrive_connection()

    # Get the file name
    file_name = os.path.basename(filepath)

    # Get the parent folder
    parent_folder = os.path.basename(os.path.dirname(filepath))

    file_query = f"mimeType != 'application/vnd.google-apps.folder' and name = '{file_name}'"
    folder_query = f"name='{parent_folder}' and mimeType='application/vnd.google-apps.folder'"
    fields = "files(id, name, parents)"
    drive_id = '0AN3GmaVXlFK-Uk9PVA'

    files = get_drive_file_list(drive_service, file_query, fields, drive_id)
    folders = get_drive_file_list(drive_service, folder_query, fields, drive_id)

    # We now have two lists of potential files and folders. We just have to match the folder/file combination with the
    # original file path to make sure we download the correct file.
    flag = False
    for file1 in files:
        parent_folder_id = file1['parents'][0]
        for folder in folders:
            if folder['id'] == parent_folder_id:
                do_download(drive_service, f'kmls/{file_name}', file1['id'])
                flag = True
                break
        if flag:
            break
    if not flag:
        raise FileNotFoundError(f'The file {filepath} could not be found.')


def download_databases(database_location):
    if not os.path.exists(database_location):
        # Create a new directory because it does not exist
        os.makedirs(database_location)
        os.makedirs(os.path.join(database_location, 'original'))

    drive_service = get_gdrive_connection()

    # location_dataframe
    destination_path = os.path.join(database_location, 'original', 'location_dataframe.csv')
    file_id = '1PTw7C8o-uFq-edJM0URTsSpvQ-BVW6w7'
    print('Downloading location_dataframe.csv ...')
    do_download(drive_service, destination_path, file_id)

    # survey_match
    destination_path = os.path.join(database_location, 'original', 'survey_match.csv')
    file_id = '10ZDOIF2bnIJ-cRJFCNQ3Jzg08rP1lxYa'
    print('Downloading survey_match.csv ...')
    do_download(drive_service, destination_path, file_id)

    # det_match
    destination_path = os.path.join(database_location, 'original', 'det_match.csv')
    file_id = '17MX-QbCDyP8UBAQCAtJv5pv0Dg0I74lQ'
    print('Downloading det_match.csv ...')
    do_download(drive_service, destination_path, file_id)

    # airdata
    destination_path = os.path.join(database_location, 'original', 'airdata_matches.csv')
    file_id = '1hjYBPm6wNBgdgHEgFVMDS_zfrQ0CXf5z'
    print('Downloading airdata_matches.csv ...')
    do_download(drive_service, destination_path, file_id)

    # kml_gdf
    # https://drive.google.com/file/d/1-07FdpPFkNKqFmnmE9p9RQ8EvTuH2W_f/view?usp=drive_link
    destination_path = os.path.join(database_location, 'original', 'kml_gdf.csv')
    file_id = '1-07FdpPFkNKqFmnmE9p9RQ8EvTuH2W_f'
    print('Downloading kml_gdf.csv ...')
    do_download(drive_service, destination_path, file_id)


def do_download(drive_service, destination_path, file_id, file_sha1=None, hash_store=defaultdict(str),
                hash_store_file='', test=False):
    '''
    Download the file
    '''
    folder_path = os.path.dirname(destination_path)
    os.makedirs(folder_path, exist_ok=True)
    file_contents = download_file(drive_service, file_id)
    if file_contents is not None:
        with open(destination_path, 'wb') as write:
            write.write(file_contents.getvalue())
        if hash_store_file != '':
            add_hash(destination_path, hash_store_file, file_sha1)
    else:
        print(f'skipping non-binary doc {destination_path}')
    return True


def add_hash(destination_path, hash_store_file, file_sha1):
    with open(hash_store_file, 'a') as hash_write:
        hash_write.writelines(
            f'{file_sha1}  {destination_path}\n')


if __name__ == '__main__':
    download_databases('databases')
    # filepath = 'drive/Shareddrives/Thermal File Archive/Flight Planning/.UGCS/Koala Strategy Baseline 2022/Koala Strategy_20221024-28/SYB04_Mel_406869_UGCS_AGL_256m.kml'
    # download_file_from_filepath(filepath)
    # download_file_from_filepath('drive/Shareddrives/Thermal File Archive/Flight Planning/.UGCS/Meryla/Meryla FR5-7_UGCS_W_672m.kml')
