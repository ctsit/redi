<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:date="http://exslt.org/dates-and-times"
                extension-element-prefixes="date">
                <xsl:import href="date.month-abbreviation.template.xsl" />
                <xsl:import href="date.year.template.xsl" />
    <xsl:output method="html" version="4.0" encoding="UTF-8" indent="yes" />
    <xsl:template match="/">
        <html>
            <head>
                <style>table,th,td
       {
            border:1px solid black;
            border-collapse:collapse;
        }</style>
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
                </table>
                <br />
                <h3>Summary</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Total Subjects</th>
                            <xsl:for-each select="report/summary/forms/form">
                                <th>
                                    <xsl:value-of select="form_name" />
                                </th>    
                            </xsl:for-each>
                            <th>Total Unique Dates</th>
                            <th>Earliest date</th>
                            <th>Latest date</th>
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
                            <td>
                                <xsl:value-of select="report/summary/total_unique_dates" />
                            </td>
                            <td>
                                <xsl:variable name="month">
                                <xsl:call-template name="date:month-abbreviation">
                                    <xsl:with-param name="date-time" select="report/summary/dates/earliestDate" />?
                                </xsl:call-template>
                                </xsl:variable>
                                <xsl:variable name="yr">
                                <xsl:call-template name="date:year">
                                    <xsl:with-param name="date-time" select="report/summary/dates/earliestDate" />?
                                </xsl:call-template>
                                </xsl:variable>
                                <xsl:value-of select="concat($month, ' ', $yr)" />
                            </td>
                            <td>
                                <xsl:variable name="month">
                                <xsl:call-template name="date:month-abbreviation">
                                    <xsl:with-param name="date-time" select="report/summary/dates/latestDate" />?
                                </xsl:call-template>
                                </xsl:variable>
                                <xsl:variable name="yr">
                                <xsl:call-template name="date:year">
                                    <xsl:with-param name="date-time" select="report/summary/dates/latestDate" />?
                                </xsl:call-template>
                                </xsl:variable>
                                <xsl:value-of select="concat($month, ' ', $yr)" />
                            </td>
                        </tr>
                    </tbody>
                </table>
                <br />
                <!-- Alerts start here -->
                <!-- <h3>Import Alerts</h3> -->
                <!-- check for not null -->
                <!-- Commented out as the output is not fully de-identified-->
                <!-- <xsl:if test="report/alerts/tooManyForms/eventAlert">
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
                </xsl:if> -->
                <!-- check for not null -->
                <!-- Commented out as the output is not fully de-identified-->
                <!-- <xsl:if test="report/alerts/tooManyValues/valuesAlert">
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
                </xsl:if>  -->
                <br />
                <h3>Subject Details</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Subject</th>
                            <xsl:for-each select="report/summary/forms/form">
                                <th>
                                    <xsl:value-of select="form_name" />
                                </th>    
                            </xsl:for-each>
                            <th>Earliest date</th>
                            <th>Latest date</th>
                            <th>Study Period (Days)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <xsl:for-each select="report/subjectsDetails/Subject">
                            <tr>
                                <td>
                                    <xsl:value-of select="ID" />
                                </td>
                                <xsl:for-each select="forms/form">
                                <td>
                                    <xsl:value-of select="form_count"/>
                                </td>    
                                </xsl:for-each>
                                <td>
                                    <xsl:variable name="month">
                                <xsl:call-template name="date:month-abbreviation">
                                    <xsl:with-param name="date-time" select="earliestdate" />?
                                </xsl:call-template>
                                </xsl:variable>
                                <xsl:variable name="yr">
                                <xsl:call-template name="date:year">
                                    <xsl:with-param name="date-time" select="earliestdate" />?
                                </xsl:call-template>
                                </xsl:variable>
                                <xsl:value-of select="concat($month, ' ', $yr)" />
                                    <!-- <xsl:value-of select="earliestdate" /> -->
                                </td>
                                <td>
                                    <xsl:variable name="month">
                                <xsl:call-template name="date:month-abbreviation">
                                    <xsl:with-param name="date-time" select="latestdate" />?
                                </xsl:call-template>
                                </xsl:variable>
                                <xsl:variable name="yr">
                                <xsl:call-template name="date:year">
                                    <xsl:with-param name="date-time" select="latestdate" />?
                                </xsl:call-template>
                                </xsl:variable>
                                <xsl:value-of select="concat($month, ' ', $yr)" />
                                    <!-- <xsl:value-of select="latestdate" /> -->
                                </td>
                                <td>
                                    <xsl:value-of select="StudyPeriod" />
                                </td>
                            </tr>
                        </xsl:for-each>
                    </tbody>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>