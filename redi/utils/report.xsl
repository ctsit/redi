<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="html" version="4.0" encoding="UTF-8" indent="yes" />

<xsl:variable name="sort_column" select="/report/sort_details_by" />

<xsl:template match="/">
<html>
<head>
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}

table#redi_summary thead,
table#subject_details thead {
    color: #fff;
    background: #11772D;
}

table#subject_details tr:nth-child(odd) {
    backround: #ccc;
}

table#errors thead {
    color: #fff;
    background: #D37C90;
}
</style>

<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<link rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/themes/smoothness/jquery-ui.css" />
<script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/jquery-ui.min.js"></script>
<script src="http://tablesorter.com/__jquery.tablesorter.min.js"></script>
<script>
$(document).ready(function() {
    $("#subject_details").tablesorter();
    }
);
</script>
    <title>Summary Report</title>
</head>
<body>
               <h1>Data Import Report</h1>
                <table>
                    <tr>
                        <td>
                            <b>Project</b>
                        </td>
                        <td>
                            <xsl:value-of select="report/header/project" />
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <b>Date</b>
                        </td>
                        <td>
                            <xsl:value-of select="report/header/date" />
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <b>RedCapServerAddress</b>
                        </td>
                        <td>
                            <xsl:value-of select="report/header/redcapServerAddress" />
                        </td>
                    </tr>
                    <tr>
                        <td> Start/End Times </td>
                        <td>
                            From <xsl:value-of select="report/time_all_start" /> to
                            <xsl:value-of select="report/time_all_end" />
                        </td>
                    </tr>
                    <tr>
                        <td> Duration </td>
                        <td> <xsl:value-of select="report/time_all_diff" /> </td>
                    </tr>
                </table>
                <br />
                <h3>Summary</h3>
                <table id="redi_summary">
                    <thead>
                        <tr>
                            <th>Total Subjects</th>
                            <xsl:for-each select="report/summary/forms/form">
                                <th>
                                    <xsl:value-of select="form_name" />
                                </th>
                            </xsl:for-each>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <xsl:value-of select="report/summary/subjectCount" />
                            </td>
                            <xsl:for-each select="report/summary/forms/form">
                                <td>
                                    <xsl:value-of select="form_count"/>
                                </td>
                            </xsl:for-each>
                        </tr>
                    </tbody>
                </table>
                <br />

            <!-- Alerts start here -->
            <xsl:if test="count(report/alerts/tooManyForms/eventAlert) > 0 or count(report/alerts/tooManyValues/valuesAlert) > 0">
                <h3>Import Alerts</h3>
                <!-- check for not null -->
                <!-- Commented out as the output is not fully de-identified-->
                <xsl:if test="report/alerts/tooManyForms/eventAlert">
                    <table>
                        <thead>
                            <tr>
                                <th>Too many forms</th>
                            </tr>
                        </thead>
                        <tbody>
                            <xsl:for-each select="report/alerts/tooManyForms/eventAlert">
                                <tr>
                                    <td>
                                        <xsl:value-of select="message" />
                                    </td>
                                </tr>
                            </xsl:for-each>
                        </tbody>
                    </table>
                    <br />
                </xsl:if>
                <!-- check for not null -->
                <!-- Commented out as the output is not fully de-identified-->
                <xsl:if test="report/alerts/tooManyValues/valuesAlert">
                    <table>
                        <thead>
                            <tr>
                                <th>Too many values</th>
                            </tr>
                        </thead>
                        <tbody>
                            <xsl:for-each select="report/alerts/tooManyValues/valuesAlert">
                                <tr>
                                    <td>
                                        <xsl:value-of select="message" />
                                    </td>
                                </tr>
                            </xsl:for-each>
                        </tbody>
                    </table>
                </xsl:if>
            </xsl:if>
                <br />
                <h3>Subject Details</h3>
                <table id="subject_details" class="tablesorter">
                    <caption>
                        <xsl:value-of select="
                                concat(
                                    'Number of forms for each of the ',
                                    count(report/subjectsDetails/subject),
                                    ' subject(s)') " />
                    </caption>
                    <thead>
                        <tr>
                            <th>Subject ID</th>
                            <th>Subject Number</th>
                            <xsl:for-each select="report/summary/forms/form">
                                <th>
                                    <xsl:value-of select="form_name" />
                                </th>
                            </xsl:for-each>
                        </tr>
                    </thead>
                    <tbody>
                        <xsl:for-each select="report/subjectsDetails/subject">
                            <xsl:sort select="*[name() = $sort_column]" order="ascending" />

                            <tr>
                                <td>
                                    <xsl:value-of select="lab_id" />
                                </td>
                                <td>
                                    <xsl:value-of select="redcap_id" />
                                </td>
                                <xsl:for-each select="forms/form">
                                <td>
                                    <xsl:value-of select="form_count"/>
                                </td>
                                </xsl:for-each>
                            </tr>
                        </xsl:for-each>
                    </tbody>
                </table>
                <br />
                <h3>Errors</h3>
                <table id="errors">
                    <xsl:for-each select="report/errors/error">
                    <tr>
                        <td>
                                    <xsl:value-of select='.' />
                        </td>
                    </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
