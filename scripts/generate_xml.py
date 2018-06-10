from itertools import chain
from common_functions import *

class genXML:
    def tag_xml(ele_v, ele, attr = '',attr_v = ''):
        """
        generate XML tags
        args:
        (str) ele: element name; (str) ele_v: value of the element
        (str/list) attr: attribute name, attr_v: attribute values
        returns: (str) XML tags
        """
        if ele_v == '':
            return ''
        if not ele or type(ele) != str:
            return False
        if all([attr == '',attr_v == '']):
            xml = """<%(s)s>{}</%(s)s>""" % {'s': ele}
            return xml.format(ele_v)
        if all([type(attr) == str, type(attr_v) == str]):
            attr = [attr]
            attr_v = [attr_v]
        rg = list(range(len(attr)))
        attrs = [' {}="{}"'.format(*[attr[i], attr_v[i]]) for i in rg if attr_v[i] != '']
        attrs = ''.join(attrs)
        return """<%s%s>%s</%s>""" % (ele, attrs, ele_v, ele)

    def attr_xml(entry, ref):
    #sample entry[value(ele), value(attr1), value(attr2), ...]
        if entry[0] == '':
            return ''
        attrs = ref['attr']
        attr_values = entry[1:]
        if type(attr_values) != list:
            attr_values = [attr_values]
        if type(attrs) != list:
            attrs = [attrs]
        attrs_values = []
        for i in list(range(len(attrs))):
            if attrs[i]['con'] != '':
                attr_value = val_con(attr_values[i], attrs[i]['con'])
                if attr_value == False:
                    return False
            else:
                attr_value = str(attr_values[i])
            attrs_values.append(attr_value)
        attrs = [x['ele'] for x in attrs]
        return genXML.tag_xml(entry[0],ref['ele'],attrs,attrs_values)

    def repeatFunction(entry, ref, function_name):
        xmls = []
        for i in entry:
            xml = getattr(genXML, function_name)(i, ref)
            xmls.append(xml)
        return '\n'.join(xmls)

    def per_org(entry, field_id):
        ref = fieldIndex[field_id]['child']
        entry_new = []
        entry[1] = val_con(entry[1], ref['child'][0]['attr']['con'])
        if entry[1] == False:
            return False
        entry_new = entry_new + [genXML.attr_xml(entry[:2], ref['child'][0])]
        if entry[1] == "Personal":
            name = [x.strip() for x in entry[0].split(',')]
            if len(name) > 1:
                first_name = genXML.tag_xml(', '.join(name[1:]), 'givenName')
                last_name = genXML.tag_xml(name[0], 'familyName')
                entry_new = entry_new + [first_name] + [last_name]
            else:
                entry_new = entry_new + [''] * 2
        else:
            entry_new = entry_new + [''] * 2
        if entry[3] != '':
            identifiers = entry[3:]
            i = 0
            identifiersInfo = []
            while i + 1 <= len(identifiers):
                idscheme = val_con(identifiers[i + 1], ref['child'][3]['attr'][0]['con'])
                if identifiers[i + 1] == False:
                    return False
                scheme_uri = ref['child'][3]['attr'][1]['con'][idscheme]
                idInfo = [identifiers[i], idscheme, scheme_uri]
                idInfo = genXML.attr_xml(idInfo, ref['child'][3])
                identifiersInfo.append(idInfo)
                i += 2
            identifiersInfo = '\n'.join(identifiersInfo)
        else:
            identifiersInfo = ''
        entry_new = entry_new + [identifiersInfo] + [genXML.tag_xml(entry[2], 'affiliation')]
        identifiersInfo_xml = '\n'.join([x for x in entry_new if x != ''])
        return identifiersInfo_xml

    def identifier(entry):
    #sample entry:'10.5072','10.5072/1234-5667'
        xml_t = '<identifier identifierType="DOI">{}</identifier>'
        entry = split_str(entry, '/')
        if len(entry) == 1:
            return xml_t.format(gen_doi(entry[0]))
        else:
            return xml_t.format('/'.join(entry))

    def publicationYear(entry):
        try:
            entry = int(entry)
        except:
            return False
        return genXML.tag_xml(str(entry), fieldIndex[5]['ele'])

    def resourceType(entry):
        entry[1] = val_con(entry[1], resourceTypeGeneral)
        if not entry[1]:
            return False
        else:
            entry[0] = '/'.join([entry[1], entry[0]])
        return genXML.attr_xml(entry, fieldIndex[10])

    def fundingReference(entry, ref = fieldIndex[19]):
        entry = [entry[0], entry[1:3]] + entry[3:]
        funderName = genXML.tag_xml(entry[0], 'funderName')
        funderIdentifierType = genXML.attr_xml(entry[1], fieldIndex[19]['child']['child'][1])
        awardNumber = genXML.tag_xml(entry[2], 'awardNumber')
        awardURI = genXML.tag_xml(entry[3], 'awardURI')
        awardTitle = genXML.tag_xml(entry[4], 'awardTitle')
        xmls = [funderName, funderIdentifierType, awardNumber, awardURI , awardTitle]
        xmls = '\n'.join(x for x in xmls if x!= '')
        return genXML.tag_xml(xmls, 'fundingReference')

    def creator(entry, ref = fieldIndex[2]):
        creatorInfo = genXML.per_org(entry, 2)
        return genXML.tag_xml(creatorInfo, 'creator')

    def contributor(entry, ref = fieldIndex[7]):
        contributor_type = val_con(entry[0], contributorType)
        if contributor_type == False:
            return False
        contributorInfo = genXML.per_org(entry[1:], 7)
        xml = genXML.tag_xml(contributorInfo, 'contributor','contributorType', contributor_type)
        return xml

    def geoLocation(entry, ref = fieldIndex[18]['child']):
        if type(entry) == str:
            geoLocationPlace = genXML.tag_xml(entry, 'geoLocationPlace')
            return genXML.tag_xml(geoLocationPlace, 'geoLocation')
        geoLocationPlace = genXML.tag_xml(entry[0], 'geoLocationPlace')
        coordinates = entry[1:]
        coordinates_xml = []
        for item in coordinates:
            item = split_str(item, ',')
            geoLocationType = val_con(item[0], geoLocationType_list)
            if geoLocationType == False:
                return False
            if geoLocationType == 'geoLocationPoint':
                ref_p = ref['child'][1]
                coords = item[1:]
                coords = [genXML.tag_xml(coords[i], ref_p['child'][i]['ele']) for i in [0, 1]]
                coords = genXML.tag_xml('\n'.join(coords), ref_p['ele'])
            if geoLocationType == 'geoLocationBox':
                ref_p = ref['child'][2]
                coords = item[1:]
                coords = [genXML.tag_xml(coords[i], ref_p['child'][i]['ele']) for i in list(range(4))]
                coords = genXML.tag_xml('\n'.join(coords), ref_p['ele'])
            if geoLocationType == 'geoLocationPolygon':
                ref_p = ref['child'][3]
                i = 1
                coords = []
                while i + 1 <= len(item):
                    coords += [[item[i], item[i + 1]]]
                    i += 2
                polygonPoints = []
                for ele in coords:
                    ele = [genXML.tag_xml(ele[i], ref_p['child']['child'][i]['ele']) for i in [0, 1]]
                    ele = genXML.tag_xml('\n'.join(ele), ref_p['child']['ele'])
                    polygonPoints.append(ele)
                polygonPoints = '\n'.join(polygonPoints)
                coords = genXML.tag_xml(polygonPoints, ref_p['ele'])
            coordinates_xml.append(coords)
        coordinates_xml = '\n'.join([x for x in coordinates_xml if x != ''])
        geoInfo = [geoLocationPlace, coordinates_xml]
        geoInfo = '\n'.join([x for x in geoInfo if x != ''])
        return genXML.tag_xml(geoInfo, 'geoLocation')

def gen_xml(entry, colname):
    try:
        if entry == False:
            return False
        if entry == '':
            return ''
        if colname == '1':
            return genXML.identifier(entry)
        if colname == '5':
            return genXML.publicationYear(entry)
        if colname == '10':
            return genXML.resourceType(entry)
        if colname in ['4', '9', '15']:
            return genXML.tag_xml(entry, fieldIndex[int(colname)]['ele'])
        if colname in ['13', '14']:
            ref = fieldIndex[int(colname)]['child']['ele']
            xmls = genXML.repeatFunction(entry, ref, 'tag_xml')
            return genXML.tag_xml(xmls, fieldIndex[int(colname)]['ele'])
        if colname in ['3', '6', '8', '11', '12', '16','17']:
            entry = [ext_len(i, values_num[int(colname)]) for i in entry]
            ref = fieldIndex[int(colname)]['child']
            xmls = genXML.repeatFunction(entry, ref, 'attr_xml')
            return genXML.tag_xml(xmls, fieldIndex[int(colname)]['ele'])
        if colname == '19':
            entry = [ext_len(i, values_num[int(colname)]) for i in entry]
            ref = fieldIndex[int(colname)]
            xmls = genXML.repeatFunction(entry, ref, 'fundingReference')
            return genXML.tag_xml(xmls, ref['ele'])
        if colname == '2':
            entry = [ext_len(i, values_num[int(colname)]) for i in entry]
            ref = fieldIndex[int(colname)]
            xmls = genXML.repeatFunction(entry, ref, 'creator')
            return genXML.tag_xml(xmls, ref['ele'])
        if colname == '7':
            entry = [ext_len(i, values_num[int(colname)]) for i in entry]
            ref = fieldIndex[int(colname)]
            xmls = genXML.repeatFunction(entry, ref, 'contributor')
            return genXML.tag_xml(xmls, ref['ele'])
        if colname == '18':
            ref = fieldIndex[int(colname)]
            xmls = genXML.repeatFunction(entry, ref['child'], 'geoLocation')
            return genXML.tag_xml(xmls, ref['ele'])
    except:
        return False
