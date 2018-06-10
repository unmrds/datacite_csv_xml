from parse_csv import *
from register_doi import *
import os.path

def csv_xml_metadata(filename, export = True, folderpath = ''):
    """
    read records in CSV and export converted XMLs
    args:
    (str) filename: the filename
    (bool) export: whether to export the XMLs (yes: True, no: False)
    (str) folderpath: specify a folder to store the XMLs (if applicable)
    """
    try:
        df = read_records(filename)
        return generate_xml(df, export, folderpath)
    except:
        if not os.path.exists(filename):
            print('File not exists. Please choose another file.')
        if not os.path.exists(folderpath) and folderpath != '':
            print('Folder not exists. Please choose another folder.')

def mint_doi(filename, username, password, export = False, folderpath = ''):
    """
    read records in CSV and register DOIs
    args:
    (str) filename: the filename
    (str) username: DataCite MDS Username
    (str) password: DataCite MDS password
    (bool) export: whether to export the XMLs (yes: True, no: False)
    (str) folderpath: specify a folder to store the XMLs (if applicable)
    """
    records = csv_xml_metadata(filename, export, folderpath)
    if records:
        output_msgs = []
        for record in records:
            doi_reg = register_doi(record, username, password)
            output_msgs.append(doi_reg)
        return output_msgs

if __name__ == "__main__":
    csv_xml_metadata(filename)
    csv_xml_metadata(filename, export = False)
    mint_doi(filename, username, password)
