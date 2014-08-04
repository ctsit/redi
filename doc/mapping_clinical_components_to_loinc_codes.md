# Mapping Clinical Components to LOINC Codes

This document explains how to lookup [LOINC] Codes and map them to a site's local clinical components for RED-I to use.

## Lookup LOINC Codes
1. Download the [LOINC Table File] and open it in your preferred [Spreadsheet Viewer].
2. Find the columns **LONG_COMMON_NAME** and **COMMON_TEST_RANK**.
3. Filter the **LONG_COMMON_NAME** by the name of your clinical component.
4. Sort **COMMON_TEST_RANK** descendingly. This column ranks the top 2000 components from most common (ranked 1) to least common (ranked 2000), as described on the [LOINC usage site](http://loinc.org/usage). Unless you are mapping specialized data, it is more likely that the component of interest is ranked more highly, i.e., it is more common.
5. Starting with the highest rank, use [LOINC Search] to investigate each Component until you've found the one you're looking for.

[LOINC]: http://loinc.org
[LOINC Search]: http://search.loinc.org
[LOINC Table File]: http://loinc.org/downloads/loinc
[Spreadsheet Viewer]: http://www.libreoffice.org/discover/calc/

## Map Local ID to LOINC Code

Mapping is done in an XML document; a sample of a mapping file and an explaination of the format is as follows.

- Format: **XML**
- settings.ini configuration:
  - Key: **component_to_loinc_code_xml**
  - Default: **clinical-component-to-loinc.xml**

### Sample

```
<?xml version='1.0' encoding='US-ASCII'?>
<clinical_datum>
    <version>0.1.0</version>
    <Description>
      Mapping of the University Hospital's Lab Component Identifiers to corresponding LOINC codes
    </Description>
    <components>
        <component>
          <description>Leukocytes [#/​volume] in Blood</description>
          <source>
            <name>COMPONENT_ID</name>
            <value>8675309</value>
          </source>
          <target>
            <name>loinc_code</name>
            <value>26464-8</value>
          </target>
        </component>
        <component>
          <description>Hepatitis C virus RNA [#/​volume]</description>
          <source>
            <name>COMPONENT_ID</name>
            <value>42</value>
          </source>
          <target>
            <name>loinc_code</name>
            <value>26464-8</value>
          </target>
        </component>
    </components>
</clinical_datum>
```

### Clinical Datum

The root element **MUST** be ```clinical_datum```.

Required? | Name or Path | Description | Max | Notes
-|-
Optional | ```version``` | Version number of the Clinical Datum XML format. | 1 | 0.1.0 is currently the only version
Optional | ```Description``` | Description of the XML document | 1 | Potentially helpful to readers
Required | ```components``` | The parent element for [Clinical Components Mappings](#mapping) | 1

### [Clinical Component Mapping](id:mapping)

Represented as ```component``` elements under ```clinical_datum/components```. Each component represents a mapping from a (clinical component) Source to a Target (LOINC code). Source comprises an XML Element name and value; likewise, Target comprises the name and values to use as a replacement. 

For every incoming clinical component that will be mapped to a LOINC value, create a new <component> block and complete it according to the below table.

Required? | Name or Path | Description | Max | Notes
-|-
Optional | ```Description``` | Description of the Component | 1 | Potentially helpful to readers
Required | ```source``` | Parent element for the Source information | 1
Required | ```source/name``` | Name of the XML Element | 1
Required | ```source/value``` | Value of the XML Element | 1
Required | ```target``` | Parent element for the Target information | 1
Required | ```source/name``` | Name of the XML Element | 1
Required | ```source/value``` | Value of the XML Element | 1

### Example

Given the sample above, the following input:

```<COMPONENT_ID>8675309</COMPONENT_ID>```

would be mapped to:

```<loinc_code>26464-8</loinc_code>```
