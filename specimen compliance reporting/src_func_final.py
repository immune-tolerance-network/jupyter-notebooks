# Import libraries
import pandas as pd
import numpy as np
import pyodbc
from datetime import datetime

# Import Secrets
import configparser

# Import scripts
import querying
import create_result_df
from trials import reboot,reveal,graduate,beat_ms,vibrant,dare_aps

### On lines 17,18,19,24,25,and 26, please edit the connection string. ###

if __name__ == "__main__":
    print("Starting SRC Reporting Script (src_func_final.py)...")
    configFilePath = r'C:\app\lib\CTG_reporting.ini'

    config = configparser.ConfigParser()
    config.read(configFilePath)

    # Access nested items
    ErrorLogServer = config.get('ErrorLog','ServerName')
    ErrorLogDB = config.get('ErrorLog','DBName')
    ErrorLogConnType = config.get('ErrorLog','ConnectionType')
    DataServer = config.get('Data','ServerName')
    DataDB = config.get('Data','DBName')
    DataConnType = config.get('Data','ConnectionType')


    # Connect to SQL Server for Error Reporting
    cnex = pyodbc.connect(('DRIVER={ODBC Driver 17 for SQL Server};'
                           f'Server={ErrorLogServer};Database={ErrorLogDB};'
                           f'Trusted_Connection={ErrorLogConnType};'))

    cursor = cnex.cursor()

    # Connect to SQL Server to retrieve data and run queries
    cnxn = pyodbc.connect(('DRIVER={ODBC Driver 17 for SQL Server};'
                           f'Server={DataServer};Database={DataDB};'
                           f'Trusted_Connection={DataConnType};'))

    
    # A list of clinical trial objects to iterate through:
    clinical_trials = [reboot,reveal,graduate,beat_ms,vibrant,dare_aps]

    # Create a DataFrame we will append the results of each clinical trial to:
    output = pd.DataFrame(columns = ["Study","Cohort","Visit Number","Visit Ordinal","DaysPostScreening","Sample Type","Number at least 1 collected",
                                     "Number of recorded visits","Percent"])

    errorCount = 0   #used for error logging to SQL
    try:
        # For each clinical trial...
        for trial in clinical_trials:
            # Get a list of sites:
            sites = querying.get_sites(pd,cnxn,trial)
            # Get data from LV:
            lv_data = querying.get_lv_data(pd,cnxn,trial)
            # Get data from RHO:
            rho_data = querying.get_rho_data(pd,cnxn,trial)  
            # Get visit ordinals, etc. from server
            visit_info = querying.get_visit_info(np,pd,cnxn,trial)
            # Make a temporary dataframe we will concatenate to the output dataframe defined above
            result = pd.DataFrame(columns = ["Study",'site',"Cohort","Visit Number","Visit Ordinal","DaysPostScreening","Sample Type",
                                             "Number at least 1 collected","Number of recorded visits","Percent"])

            # If the trial has a list of cohorts...
            if type(trial.cohort) == list:
                # Make a list of tuples that store all the possible sites, cohort, and visit combinations
                site_cohort_visit_list = []
                for s in sites:
                    for c in trial.cohort:
                        for v in trial.visits[c]:
                            site_cohort_visit_list.append((s,c,v))
                # For each possible site, cohort, and visit combination...
                for s_c_v in site_cohort_visit_list:
                    # Analyze the data
                    result_to_add = create_result_df.create_result_df(pd,trial,s_c_v[1],rho_data,lv_data,visit_info,s_c_v[0],s_c_v[2])
                    # Concatenate the current dataframe to the result dataframe defined in the for loop above
                    result = pd.concat([result,result_to_add])
                # Reset the index of the result dataframe
                result.reset_index(inplace=True,drop = True)
                # For each cohort in the trial...
                for chrt in trial.cohort:
                    # Remove the exceptions specified in the trial object
                    result = create_result_df.remove_exceptions(np,result,trial,chrt)
                # Concatenate the dataframe for the trial to the overall output dataframe
                output = pd.concat([output,result])

            # Otherwise if the study does not have cohorts...
            else:
                # Make a list of tuples that contain all the possible visits a site could have
                site_visit_list = []
                for s in sites:
                    for v in trial.visits:
                        site_visit_list.append((s,v))
                # For each possible visit at a site...
                for s_v in site_visit_list:
                    # Analyze the data
                    result_to_add = create_result_df.create_result_df(pd,trial,None,rho_data,lv_data,visit_info,s_v[0],s_v[1])
                    # Concatenate the current dataframe to the result dataframe defined in the for loop above
                    result = pd.concat([result,result_to_add])
                # Reset the index of the result dataframe
                result.reset_index(inplace=True,drop = True)
                # Remove the exceptions specified in the trial object
                result = create_result_df.remove_exceptions(np,result,trial,None)
                # Concatenate the dataframe for the trial to the overall output dataframe
                output = pd.concat([output,result])      

        # Reset the index
        output.reset_index(inplace = True)
        # Drop the index column
        output.drop(columns=["index"],inplace = True)
        # Add a LastUpdatedDate column
        output["LastUpdatedDate"] = datetime.now()
        # Write to the table
        crsr = cnxn.cursor()
        # Change DaysPostScreening and Percent as str
        output["DaysPostScreening"] = output["DaysPostScreening"].astype(str)
        output["Percent"] = output["Percent"].astype(str)

        # Move the site column to match the columns of the SQL table this will write to
        site_column = output.pop("site")
        output.insert(5,"site",site_column)

        # Truncate (delete all) the table
        crsr.execute('''TRUNCATE TABLE [DAVE].[input].[SiteCollectionCompliance]''')
        crsr.commit()
        crsr.fast_executemany = True

        insert_string = '''INSERT INTO [DAVE].[input].[SiteCollectionCompliance]
                        ([Study Number],[Cohort],[Visit Number],[Visit Ordinal],[Days Post Screening],[SiteCode],[Sample Type],[Number at Least One Collected],
                            [Number of Recorded Visits],[Percent]
                        ) VALUES
                        (?,?,?,?,?,?,?,?,?,?)'''
        
        tuples = [(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]) for i in output.values.tolist()]

        crsr.executemany(insert_string,tuples)
        crsr.commit()
        crsr.close()

    except Exception as e:
        print("Error: ",str(e))
        errorCount = + 1

        # Log error
        '''
        Parameters:
        @EventType              = 'Error'
        ,@JobName                = SQLAgent::JobName
        ,@MachineName            = System::MachineName
        ,@PackageLogID           = '0E984725-C51C-4BF4-9960-E1C80E27ABA0'
        ,@PackageName            = System::PackageName
        ,@TaskName               = System::TaskName
        ,@EventCode              = System::ErrorCode
        ,@EventDescription       = System::ErrorDescription
        ,@EventDate              = System::ErrorDateTime
        ,@PackageExecutionTime   = System::StartTime
        '''
        params = ('Error',
                  'Load Site Collection Compliance info to Reporting Server',
                  'DCT-SQL-01',
                  '0E984725-C51C-4BF4-9960-E1C80E27ABA0',
                  'Load_src_func_final_ToReportingServer',
                  'src_func_final ETL',
                  errorCount,
                  str(e))
        cursor.execute("{CALL [dbo].[SSIS_Process_LogHistory] (?,?,?,?,?,?,?,?)}", params)
        cnex.commit()
    cnxn.close()
    print("Processing Complete. src_func_final processed")


        
