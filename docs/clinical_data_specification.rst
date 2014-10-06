Clinical Data Specification
===========================

Clinical data from an Epic Clarity system should conform to this
specification. The specification was designed to adhere to default Epic
Clarity field names and data formats wherever possible.

-  All data will be returned in the UTF8 Character set
-  The first row of the file will be a header row showing the name of
   each column, enclosed in double quotes and separated by commas.
-  The field names in the header row will be those shown below. The case
   of each column name should be that shown below.
-  Subsequent rows will show lab result values. All values will be
   enclosed in double quotes and separated by commas.
-  Each row will show one lab result value.

These fields may be specified in the data file:

::

    Field Name      Field Required?  Field Description
    STUDY_ID            yes          Identifier of a person within a study
    NAME                yes          Name of lab component
    COMPONENT_ID        yes          Numeric identifier of lab component
    ORD_VALUE           yes          Result value for lab component
    REFERENCE_LOW       no           Lowest expected value for ORD_VALUE
    REFERENCE_HIGH      no           Highest expected value for ORD_VALUE
    REFERENCE_UNIT      yes          Units for ORD_VALUE
    SPECIMN_TAKEN_TIME  yes          Date and time specimen was taken from the patient/study subject. Date must be formatted as "YYYY-MM-DD HH:MM:SS".

