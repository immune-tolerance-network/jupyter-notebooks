import pandas as pd
import numpy as np
import pyodbc
from datetime import datetime

# Import scripts
import querying
import create_result_df
from trials import reboot,reveal,graduate,beat_ms,vibrant,dare_aps



if __name__ == "__main__":
    print("Starting SRC Reporting Script (sitecomplianceparticipant.py)...")

    # Connect to SQL Server for Error Reporting
    cnex = pyodbc.connect(('DRIVER={ODBC Driver 17 for SQL Server};'
                           'Server=<ServerName>;Database=<DatabaseName>;'
                           'Trusted_Connection=<ConnectionType>;'))

    cursor = cnex.cursor()

    # Connect to DIVE and run queries
    cnxn = pyodbc.connect(('DRIVER={ODBC Driver 17 for SQL Server};'
                           'Server=<ServerName>;Database=<DatabaseName>;'
                           'Trusted_Connection=<ConnectionType>;'))
    




    # Make an empty dataframe we will append to
    output = pd.DataFrame(columns = [#"RowId",
                                     "Study Number","Cohort","Visit Number","Visit Ordinal","Days Post Screening","SiteCode","ParticipantID",
                                 "Sample Type","Collected","CollectionDate"])

    # Create a list of trials
    clinical_trials = [reboot,reveal,graduate,beat_ms,vibrant,dare_aps]
    
    # For each clinical trial
    errorCount = 0
    try:
        for trial in clinical_trials:
            # Create a blank output dataframe
            output_append = pd.DataFrame(columns = [#"RowId",
                                                    "Study Number","Cohort","Visit Number","Visit Ordinal","Days Post Screening","SiteCode","ParticipantID",
                                        "Sample Type","Collected","CollectionDate"])
            # Get lv data for that trial
            lv_data =  querying.get_lv_data(pd,cnxn,trial)
        
            # Get visit information for the trial
            visit_data = querying.get_visit_info(np,pd,cnxn,trial)
            # Get all the pids for the trial
            rho_data = querying.get_rho_data_participant(pd,cnxn,trial)
            rho_pids = list(rho_data["Participant ID"].unique())
            lv_pids = list(lv_data["Participant"].unique())
            all_pids = list(set(rho_pids + lv_pids))

            # Make a visit dictionary from visit_data
            visit_dict_vis_num = list(visit_data["Visit Number"])
            visit_dict_vis_ord = list(visit_data["Visit Ordinal"])
            visit_dict_vis_DPS = list(visit_data["DaysPostScreening"])

            visit_dict_vis_to_vis_ord = dict(zip(visit_dict_vis_num,visit_dict_vis_ord))
            visit_dict_vis_to_dps = dict(zip(visit_dict_vis_num,visit_dict_vis_DPS))
            # For each pid...
            for pid in all_pids:
                # Filter the lv data on the pid
                lv_data_pid = lv_data[lv_data["Participant"] == pid]
                # Get a list of visits the pid had
                lv_pid_visits = list(set(lv_data_pid["visitnum"].values))
            
                rho_data_pid = rho_data[rho_data["Participant ID"] == pid]
                rho_pid_visits = list(rho_data_pid["Visit Number"].unique())
                pid_visits = list(set(lv_pid_visits + rho_pid_visits))
                # TODO: get cohort of PID
                chrt_lst = list(lv_data_pid["Cohort"].unique())
                chrt_lst = [x for x in chrt_lst if x != None]

                if len(chrt_lst) != 0:
                    chrt = chrt_lst[0]
                else:
                    chrt = None
                # For each visit...
                for visit in pid_visits:
                    visit_ord = visit_dict_vis_to_vis_ord[visit]
                    d_p_s = visit_dict_vis_to_dps[visit]
                    # For each specimen type
                    trial_specimen_types = trial.specimen_types
                    if type(trial.specimen_types) == dict:
                        trial_specimen_types = list(trial.specimen_types.keys())

                    # Get the site code
                    site_code_options = list(lv_data_pid["sitecode"].unique())
                    if len(site_code_options) > 0:
                        sitecode = site_code_options[0]
                    else:
                        sitecode = None


                    for spc_tpe in trial_specimen_types:

                        # Filter the lv data on the visit number and specimen type
                        lv_data_pid_visit_spc = lv_data_pid[(lv_data_pid["visitnum"] == visit) & (lv_data_pid["specimentype"] == spc_tpe)]
                        # Get the number of rows in the df 
                        is_collected = not lv_data_pid_visit_spc.empty

                        # Get the collection date
                        collection_dates = list(lv_data_pid_visit_spc["CollectionDate"])
                        collection_dates = [dte for dte in collection_dates if dte != None]
                        collection_dates.sort()
                        if len(collection_dates) > 0:
                            collection_date = collection_dates[0]
                        else:
                            collection_date = None

                        


                        output_list = [#None, # RowID
                                    trial.studynum, # Study Number
                                    chrt, # Cohort
                                    visit, # Visit Number
                                    visit_ord,
                                    d_p_s,
                                    sitecode,
                                    pid, # ParticipantID
                                    spc_tpe, # specimen type
                                    is_collected, # Collected
                                    collection_date
                                    ]
                        output_append.loc[len(output_append)] = output_list
                        
                        # Get sample types expected for this visit
                        # If study has cohorts:
        # ["RowId","Study Number","Cohort","Visit Number","Visit Ordinal","Days Post Screening","SiteCode","ParticipantID",
                                        # "Sample Type","Collected"]
            # TODO: Remove exceptions
            if type(trial.cohort) == list:
                for trial_cohort in trial.cohort:
                    output_append = create_result_df.remove_exceptions_participant(np,output_append,trial,trial_cohort)
                    
                    #output_append.drop(columns='Percent',inplace=True)
                output = pd.concat([output,output_append])
            else:
                output_append = create_result_df.remove_exceptions_participant(np,output_append,trial,None)
                #output_append.drop(columns='Percent',inplace=True)
                output = pd.concat([output,output_append])
            
            
        # output["LastUpdatedDate"] = datetime.now()
        crsr = cnxn.cursor()
        crsr.execute('''TRUNCATE TABLE [DAVE].[input].[SiteCollectionComplianceParticipant]''')
        crsr.commit()
        crsr.fast_executemany = True

        insert_string = '''INSERT INTO [DAVE].[input].[SiteCollectionComplianceParticipant]
                        ([Study Number],
                        [Cohort],
                        [Visit Number],
                        [Visit Ordinal],
                        [Days Post Screening],
                        [SiteCode],
                        [Participant ID],
                        [Sample Type],
                        [Collected],
                        [CollectionDate]
                    
                        ) VALUES
                        (?,?,?,?,?,?,?,?,?,?)'''
        
        tuples = [(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]) for i in output.values.tolist()]


        crsr.executemany(insert_string,tuples)
        crsr.commit()
        crsr.close()

    except Exception as e:

        print("Error: ",str(e))
        errorCount =+ 1

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
                  'Load Site Collection Compliance Participant info to Reporting Server',
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