makefakedata <- function(input,
    output,
    min_panel=1,
    max_panel=1,
    incomplete_panels=FALSE,
    start_date="2112-01-01",
    end_date="2112-12-31",
    subject_count=1) {
    # input is a csv file with these columns:
    #   loinc_component - a name that describe a lab component
    #   loinc_code - the code for that lab component
    #   low - a normal low value for that component (required)
    #   high - a normal high value for that component (required)
    #   units - typical units for the component, compatible with low and high
    #   panel - a lab panel on which these tests are likely to appear
    #   loinc_long_common_name - a more descriptive name from LOINC

    # output is a csv filename to which the fake data will be written

    # min_panel - the minimum number of panels to create for each subject

    # max_panel - the maximum number of panels to create for each subject

    # incomplete_panels - should we create panels with random missing values?

    # start_date - the first date for which labs should be generated

    # end_date - the last date for which labs should be generated

    # subject_count - the number of research subjects for which we should make data

    input_dataframe <- read.csv(input)
    minimal_input_dataframe <- input_dataframe[ c("loinc_component","loinc_code","low","high","units") ]

    data <- makeasetofsubjects(minimal_input_dataframe,
            min_panel,
            max_panel,
            incomplete_panels,
            start_date,
            end_date,
            subject_count)

    write.csv(data, file=output, quote=TRUE, row.names=FALSE)

    return(data)
}

makeasetofsubjects <- function (
    input_df,
    min_panel=1,
    max_panel=1,
    incomplete_panels=FALSE,
    start_date,
    end_date,
    subject_count=1) {

    # input_df - a dataframe from which other functions will make a panel

    # min_panel - the minimum number of panels to create for each subject

    # max_panel - the maximum number of panels to create for each subject

    # incomplete_panels - should we create panels with random missing values?

    # start_date - the first date for which labs should be generated

    # end_date - the last date for which labs should be generated

    # subject_count - the number of research subjects for which we should make data

    data <- data.frame()

    for (subject_id in (1:subject_count)) {
        set_of_panels <- makeasetofpanels(input_df,
            min_panel,
            max_panel,
            incomplete_panels,
            start_date,
            end_date)
        study_id <- rep(subject_id, nrow(set_of_panels))
        set_of_panels <- cbind(set_of_panels, study_id)
        data <- rbind(data, set_of_panels)
    }

    return(data)

}

makeasetofpanels <- function (
    input_df,
    min_panel,
    max_panel,
    incomplete_panels,
    start_date,
    end_date) {

    # input_df - a dataframe from which other functions will make a panel

    # min_panel - the minimum number of panels to create for each subject

    # max_panel - the maximum number of panels to create for each subject

    # incomplete_panels - should we create panels with random missing values?

    # start_date - the first date for which labs should be generated

    # end_date - the last date for which labs should be generated

    # Make an empty data frame to store the panels for one subject
    set_of_panels <- data.frame()

    # determine how many panels to make for this study subject
    panels <- if (min_panel == max_panel)  5 else sample(min_panel:max_panel, 1)

    # make the panels for one study subject
    for (i in (1:panels)) {
        panel_df <- makeapanel(input_df, start_date, end_date, incomplete_panels)
        set_of_panels <- rbind(set_of_panels, panel_df)
    }

    return(set_of_panels)
}

makeapanel <- function (input_dataframe,
    start_date,
    end_date,
    incomplete_panels=FALSE) {

    # input_dataframe - a dataframe containing at a minimum a numeric named
    # "low" and a numeric named "high"

    # incomplete_panels - should we create panels with random missing values?

    # start_date - the first date for which labs should be generated

    # end_date - the last date for which labs should be generated

    # add a result column with a random value within the accpetable range for each test
    output <- cbind(result=round(runif(nrow(input_dataframe),
                        input_dataframe$low,
                        input_dataframe$high), digits=3),
            input_dataframe)

    # add a date column.
    # Use a one row data frame to trick rand.date into returning only one date value
    x <- data.frame(dummy=1)
    output$date_time_stamp=rand.date(start_date, end_date, x)

    # TODO provide a minimum components per panel
    if (incomplete_panels == TRUE) {
        row_mask <- sample(0:8, nrow(input_df), replace=T) > 1
        output <- subset(output, row_mask)
    }

    return (output)

}

rand.date=function(start.day,end.day,data){
# This function will generate a uniform sample of dates from
# within a designated start and end date:
# Copyright StackOverflow user Colin, http://stackoverflow.com/users/2986028/colin

  size=dim(data)[1]
  days=seq.Date(as.Date(start.day),as.Date(end.day),by="day")
  pick.day=runif(size,1,length(days))
  date=days[pick.day]
}
