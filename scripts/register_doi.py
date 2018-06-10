import requests, sys

def register_doi(entry, username, password):
    """
    args: (list) entry: output from the funciton csv_xml_metadata
          [DOI,URL,metadata]
    """
    doi = entry[0]
    url = entry[1]
    endpoint_metadata = 'https://mds.datacite.org/metadata'
    try:
        metadata_response = requests.post(endpoint_metadata,
          auth = (username, password),
          data = entry[2].encode('utf-8'),
          headers = {'Content-Type':'application/xml;charset=UTF-8'})
    except:
        msg = 'Please verify the metadata of {}'.format(url)
        print(msg)
        return msg
    endpoint_doi = 'https://mds.datacite.org/doi'
    file = 'doi={}\nurl={}'.format(entry[0], entry[1])
    doi_response = requests.put(endpoint_doi + "/" + doi,
      auth = (username, password),
      data = file.encode('utf-8'),
      headers = {'Content-Type':'text/plain;charset=UTF-8'})
    if doi_response.status_code == 201:
        msg = 'DOI of {} is successfull registered: {}.'.format(url, doi)
    else:
        msg = str(doi_response.status_code) + " " + doi_response.text
    print(msg)
    return msg
