# datacite_csv_xml
Convert metadata records in CSV to DataCite XMLs and mint DOIs

* Batch convert metadata information in CSV (one record a row) to DataCite XMLs ([DataCite Metadata Schema 4.1](https://schema.datacite.org/meta/kernel-4.1/))

* Allow batch DOI registrations via DataCite MDS API


### How to use
* Make sure to check documenstions provided by [DataCite](https://schema.datacite.org/meta/kernel-4.1/)
* Construct a CSV template and enter metadata records
    * From the the document "metadata_fields.md" :
        * Select the fields you need and make sure you include all the mandatory fields

        * Use values under "Column ID" as column name in your CSV

        * To faciliate the DOI registrations, you should add an additional columns and name it as "URL". 

          Examples were created in stored in the folder "sample_csvs".
    * Enter the metadata
        * Fill the fileds in the formart specified in "metadata_fields.pdf" 
        * You can skip non-mandatotry by entering a "". Examples:
            * To skip "dateInformation" for "Date|dateType|dateInformation", enter "Date|dateType"
            * To skip "affiliation" from "creatorName|NameType|affiliation|nameIdentifierScheme|nameIdentifier", enter "creatorName|NameType||nameIdentifierScheme|nameIdentifier"
        * Please be aware that some fields should be used togehter though both of them are not mandatory, e.g., "AlternateIdentifier" and "alternateIdentifierType". You can refer to the DataCite documentations.
        * Some fields may accept controlled vocabularies only. Please check out the list in "controlled_values_lists.py". Use either the code or the exact text for data entries. As an example, you can enter 1 to specify the "nameIdentifierScheme" as "ORCID".
        * For fields support multiple entries, simply separate them by a ";".  Example: "Miller, Elizabeth;Foo Data Center".
* Converting records in CSV to DataCite XMLs
```
from parse_csv import *
csv_xml_metadata('sample_records.csv', export = True, folderpath = '')
```
* Registers DOIs via DataCite XMLs with the metadata records in CSV
```
from parse_csv import *
mint_doi('sample_records.csv',username, password, export = False, folderpath = '')
```

### License
[Attribution-NonCommercial 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/legalcode)

### Sources
* [DataCite Metadata Schema 4.1](https://schema.datacite.org/meta/kernel-4.1/)
* [DataCite Metadata Schema 4.1 Documentation](https://schema.datacite.org/meta/kernel-4.1/doc/DataCite-MetadataKernel_v4.1.pdf)
* [DataCite Metadata Schema 4.1 Schema](https://schema.datacite.org/meta/kernel-4.1/metadata.xsd)
* [Full DataCite XML example](https://schema.datacite.org/meta/kernel-4.1/example/datacite-example-full-v4.1.xml)
* [DataCite MDS API Guide](https://support.datacite.org/docs/mds-api-guide)
* [Github - inveniosoftware/datacite - Python API wrapper for the DataCite Metadata Store API](https://github.com/inveniosoftware/datacite)
