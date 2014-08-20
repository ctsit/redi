# Describing a REDCap Form to RED-I

RED-I needs to know certain information about REDCap forms and events so that it can correctly translate and insert clinical data into them.

The two relevant files are called the **[Form Events](#form-events)** and **[Translation Table](#translation-table)** files. Their locations are specified in the ```settings.ini``` configuration file. Both of them are XML files.

***See:*** [How to Add a Simple REDCap Form to RED-I](#howto)


## [Form Events](id:form-events)

- Format: **XML**
- Configuration:
  - Key: **form_events_file**
  - Default: **formEvents.xml**

### Sample

```
<?xml version="1.0" encoding="UTF-8"?>
<redcapProject>
    <name>Project</name>
    <form>
        <name>cbc</name>

        <formDateField>cbc_date</formDateField>

        <formCompletedFieldName>cbc_done</formCompletedFieldName>
        <formCompletedFieldValue>2</formCompletedFieldValue>

        <formImportedFieldName>cbc_imported</formImportedFieldName>
        <formImportedFieldValue>Y</formImportedFieldValue>

        <event>
            <name>1_arm_1</name>
        </event>
        <event>
            <name>2_arm_1</name>
        </event>
    </form>
</redcapProject>

```

### Root Element

Required? | Name or Path | Description | Max
-|-
Required | ```redcapProject``` | Root node. | 1
Optional | ```redcapProject/name``` | Name of the REDCap Project being described. *(Currently unused)* | 1
Optional | ```redcapProject/form``` | One or many ```<form>``` elements to describe **REDCap Forms**

### Form Elements
The follow are children elements of each ```redcap/form``` element.

Required? | Name or Path | Description | Max | Notes
-|-
Required | ```name``` | Name of the **REDCap Form**. | 1
Required | ```formDateField``` | ID for the date field on the **REDCap Form**. | 1
Required | ```formCompletedFieldName``` | ID for the completion status field on the **REDCap Form**. | 1
Required | ```formCompletedFieldValue``` | Value written to the completion status field to designated a form as "completed". | 1 | Usually for a **Select**.
Optional | ```formImportedFieldName``` | ID for the imported status field on the **REDCap Form**. | 1
Optional | ```formImportedFieldValue``` | Value written to the imported status field to designate a form as imported versus manually entered. | 1 | Usually for a **Checkbox**, so *Y* or *N*.
Optional | ```event``` | One or many ```<event>``` elements to describe **REDCap Events** | |

### Event Elements
The following are children elements of each ```redcap/form/event``` element.

Required? | Name or Path | Description | Max
-|-
Required | ```name``` | Name of the **REDCap Event** | 1


## [Translation Table](id:translation-table)

- Format: **XML**
- Configuration:
  - Key: **translation_table_file**
  - Default: **translationTable.xml**

### Sample

```
<rediFieldMap>

    <clinicalComponent>
        <loinc_code>34714-6</loinc_code>
        <clinicalComponentName>INR</clinicalComponentName>

        <redcapFormName>inr</redcapFormName>

        <redcapFieldNameValue>inr_lab_result</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>INR</redcapFieldNameValueDescriptiveText>

        <redcapStatusFieldName>inr_lab_status</redcapStatusFieldName>
        <redcapStatusFieldValue>NOT_DONE</redcapStatusFieldValue>
    </clinicalComponent>

    <clinicalComponent>
        <loinc_code>11011-4</loinc_code>
        <clinicalComponentName>Hepatitis C virus RNA</clinicalComponentName>

        <redcapFormName>hcv_rna</redcapFormName>

        <redcapFieldNameValue>hcv_lab_result</redcapFieldNameValue>
        <redcapFieldNameUnits>hcv_lab_result_units</redcapFieldNameUnits>
        <redcapFieldNameValueDescriptiveText>HCV RNA results</redcapFieldNameValueDescriptiveText>
    </clinicalComponent>

</rediFieldMap>
```

### Clinical Components
**Clinical Component** is a generic term for test, measurement, or observation. Each Clinical Component is represented by a ```clinicalComponent``` XML element whose children elements are as follows:

Required? | Name | Description | Max | Notes
-|-
Required | ```loinc_code``` | [LOINC Code](http://loinc.org/) | 1
Required | ```clinicalComponentName``` | Name | 1
Required | ```redcapFormName``` | Name of the REDCap Form to write to. | 1
Required | ```redcapFieldNameValue``` | ID of the REDCap Field that has the value for this Clinical Component. | 1
Required | ```redcapFieldNameUnits``` | ID of the REDCap Field that has the units of measurement. | 1
Optional | ```redcapFieldNameValueDescriptiveText``` | Textual description of the REDCap Field | 1
Optional | ```redcapStatusFieldName``` | ID of the REDCap Field that holds the optional Status information | 1 | The Field with the given ID will be updated with the Value specified by ```redcapStatusFieldValue```.
Optional | ```redcapStatusFieldValue``` | Value of the REDCap Field that represents the default Status | 1

## [How to Add a Simple REDCap Form to RED-I](id:howto)
Remember, when "adding a form" you are describing it to RED-I. So, you can open your browser and use the actual REDCap Form to guide you.

1. Edit ```formEvents.xml```
   1. Copy the contents of the sample data for a ```form``` element.
   1. Replace the text of all XML Elements using the descriptions above.
1. Edit ```translationTable.xml```
   1. Copy the contents of the sample data for a ```clinicalComponent``` element
   1. Replace the text of all XML Elements using the descriptions above.
   1. Repeat for as many clinical components as needed.

### Note
You can lookup a field's ID using REDCap's **Data Collection Instruments** editor.

1. Click _Project Setup_
1. Under _Design your data collection instruments_, click  _Online Designer_.
1. Find the name of your form (called an Instrument), such as "Demographics".
1. Find the field you are looking for and copy it's _Variable_ name.
![image](screenshot-field-name-lookup.png "Screenshot showing the location of the "Subject Number" field's ID")
