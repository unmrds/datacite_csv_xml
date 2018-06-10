from controlled_values_lists import *
from fields_dicts import *
from generate_xml import *
from common_functions import *
from pandas import DataFrame, read_csv
import codecs

def split_col(colname, df):
    """
    args: (dataframe) df: a pandas DataFrame; (str) colname: column name
    returns: (column) a column stored split values
    """
    #look up repeat and mandate requirements
    col = df[colname]
    m = fieldIndex[int(colname)]['mandate']
    r = fieldIndex[int(colname)]['repeat']
    if m:
        col = col.apply(lambda x: x if x else False)
    if r:
        col = col.apply(lambda x: split_str(x))
    return col

def split_cell(entry):
    """
    split mutiple entries in the cells by "|", if the field is repeatable
    """
    if entry == False:
        return False
    try:
        return split_str(entry, '|')
    except:
        return [split_str(i, '|') for i in entry]

def read_records(filename):
    df = read_csv(filename)
    df = df.fillna('')
    columnlist = [x for x in list(df.columns) if x in list(map(str, range(1, 20)))]
    for i in columnlist:
        df[i] = split_col(i, df)
        if i in ['2', '3', '6', '7', '8', '11', '12', '16', '17', '18', '19']:
            df[i] = df[i].apply(lambda x: split_cell(x))
    df['10'] = df['10'].apply(lambda x: split_cell(x))
    return df

def generate_xml(df, export = True, folderpath = ''):
    columnlist = [x for x in list(df.columns) if x in list(map(str, range(1, 20)))]
    for i in columnlist:
        df[i] = df[i].apply(lambda x: gen_xml(x, i))
    xml_order_1 = list(map(str, range(1,6))) + ['10']
    xml_order = xml_order_1 + [x for x in columnlist if x not in xml_order_1]
    xml_outputs = []
    for i in list(range(len(df.index))):
        xml = df.iloc[[i]][xml_order].values[0]
        if False not in xml:
            xmls = '\n'.join([x for x in xml if x != ''])
            xml_output = genXML.tag_xml(xmls,'resource',
            ['xmlns:xsi', 'xmlns', 'xsi:schemaLocation'],
            ['http://www.w3.org/2001/XMLSchema-instance',
            'http://datacite.org/schema/kernel-4',
            'http://datacite.org/schema/kernel-4 http://schema.datacite.org/meta/kernel-4.1/metadata.xsd'])
            #add the location of the resource (the URL)
            try:
                doi = df['1'][i][len('<identifier identifierType="DOI">'):-len('</identifier>')]
                xml_output = [doi, df['URL'][i],xml_output]
            except:
                xml_output = ['','',xml_output]
            if export == True:
                filename = folderpath + '/' + '{}.xml'.format(df['recordID'][i])
                with codecs.open(filename,'w',encoding='utf8') as xmlfile:
                    xmlfile.write(xml_output[2])
        else:
            error_fields = [j for j in list(range(len(xml))) if xml[j] == False]
            error_fields = ', '.join([xml_order[k] for k in error_fields])
            xml_output = ''
            print('Please check field {} in row {}.'.format(error_fields, str(i)))
        xml_outputs.append(xml_output)
    xml_outputs = [x for x in xml_outputs if x!= '']
    return xml_outputs
