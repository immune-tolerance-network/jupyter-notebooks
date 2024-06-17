# Import libraries
import pandas as pd
import numpy as np
import pyodbc
from datetime import datetime

# Import scripts
import querying
import create_result_df

### On lines 17,18,19,24,25,and 26, please edit the connection string. ###

if __name__ == "__main__":
    print("Starting SRC Reporting Script (src_func_final.py)...")

    # Connect to SQL Server for Error Reporting
    cnex = pyodbc.connect(('DRIVER={ODBC Driver 17 for SQL Server};'
                          'Server=<ServerName>;Database=<DatabaseName>;'
                          'Trusted_Connection=<ConnectionType>;'))
    
    cursor = cnex.cursor()

    # Connect to DIVE and run queries
    cnxn = pyodbc.connect(('DRIVER={ODBC Driver 17 for SQL Server};'
                          'Server=<ServerName>;Database=<DatabaseName>;'
                          'Trusted_Connection=<ConnectionType>;'))

    # Define the clinical_trial class:
    class clinical_trial:
        def __init__(self,studynum,visits,cohort,specimen_types,exceptions):
            self.studynum = studynum
            self.visits = visits
            self.cohort = cohort
            self.specimen_types = specimen_types
            self.exceptions = exceptions

    # clinical_trial object for REBOOT:
    reboot = clinical_trial(studynum = "ITN080AI",
                            visits = {'A':['0A', '1A', '2A', '3A', '4A', '7A', '10A', '13A', '17A', '18A', '19A', '20A', '21A', '22A', '23A', '24A', '25A','DVA'],
                                      "B":['0B', '1B', '3B', '5B', '7B', '9B', '10B', '11B', '12B', '13B', '14B', '15B', '16B', '17B','DVB']},
                            cohort = ["A","B"],
                            specimen_types = {"Serum Clot":["H"+"%02d" % i for i in list(range(1,24))],
                                              "PBMC":['10A','10B','10C','10D','10E','10F','10G','10H','10I'],
                                              "Whole Blood\nTranscriptomics":['9A','9B'],
                                              "Whole Blood\nEpigenetic":['51','52','53','54'],
                                              "Urine Supernatant":["D"+"%02d" % i for i in list(range(1,11))],
                                              "Urine Pellet":['R01','R02']},
                            exceptions = {"A":[('PBMC','1A'),('PBMC','2A'),('PBMC','3A'),
                                               ('Urine Pellet','1A'),('Urine Pellet','2A'),('Urine Pellet','3A'),
                                               ('Urine Supernatant','1A'),('Urine Supernatant','2A'),('Urine Supernatant','3A'),
                                               ('Whole Blood\nEpigenetic','1A'),('Whole Blood\nEpigenetic','2A'),('Whole Blood\nEpigenetic','3A'),
                                               ('Whole Blood\nTranscriptomics','1A'),('Whole Blood\nTranscriptomics','2A'),('Whole Blood\nTranscriptomics','3A')],
                                         "B":[]},
                            )       

    # clinical_trial object for REVEAL:
    reveal = clinical_trial(studynum = "ITN086AI",
                            visits = ['0','3','6','8','9','10','WD'],
                            cohort = None,
                            specimen_types = {"Skin Biopsy":["M01","M02"],
                                              "Whole Blood RNA":['9A','9B','9C'],
                                              "Whole Blood DNA":['51','52','53','54','55','56'],
                                              "PBMC":["10A","10B","10C","10D","10E","10F"],
                                              "Serum":['H01', 'H02', 'H03', 'H04', 'H05', 'H06', 'H07', 'H08', 'H09', 'H10']},
                            exceptions = [('Skin Biopsy','3'),('Skin Biopsy','9')]
                           )

    # clinical_trial object for GRADUATE
    graduate = clinical_trial(studynum = "ITN084AD",
                              visits = ['-2','-1','0',"S1","S3","S4",'S5', 'S6','S8', 'S9','S10', 'S11',"S13",'S14','S15'],
                              cohort = None,
                              specimen_types = ['Nasal Brushing','Nasal Fluid','PBMC-Li Hep', 'Plasma-Li Hep', 'Serum-Clot',  'Whole Blood'],
                              exceptions = [("PBMC-Li Hep","-1"),("Plasma-Li Hep","-1"),
                                            ("Nasal Brushing","S1"),("PBMC-Li Hep","S1"),("Plasma-Li Hep","S1"),("Whole Blood","S1"),
                                            ("PBMC-Li Hep","S4"),("Plasma-Li Hep","S4"),
                                            ("Nasal Brushing","S6"),("PBMC-Li Hep","S6"),("Plasma-Li Hep","S6"),("Whole Blood","S6"),
                                            ("PBMC-Li Hep","S9"),("Plasma-Li Hep","S9"),
                                            ("Nasal Brushing","S11"),("PBMC-Li Hep","S11"),("Plasma-Li Hep","S11"),("Whole Blood","S11"),
                                            ("PBMC-Li Hep","S14"),("Plasma-Li Hep","S14"),
                                           ] # exceptions
                             )    

    # clinical_trial object for BEAT-MS
    beat_ms = clinical_trial(studynum = "ITN077AI",
                             visits = ['0','L1','1','2','4','6','8','10','12','PT'],
                             cohort = None,
                             specimen_types = {"Whole Blood\nPBMC":['10A','10B','10C','10D','10E','10F','10G','10H','10I','10J'],
                                               "Serum":["H"+"%02d" % i for i in list(range(1,21))],
                                               "Whole Blood\nDNA Isolation":['51','52','53','54','55','56'],
                                               "Whole Blood\nGene Expression":["9A","9B"],
                                               "CSF Transfix":["21A"],
                                               "CSF Super":["H"+"%02d" % i for i in list(range(1,49))],
                                               "CSF Pellet":["J49"],
                                               "Stem Cells":["SC01","SC02"]},
                             exceptions = [("Stem Cells","0"),
                                           ("CSF Transfix","1"),("CSF Super","1"),("CSF Pellet","1"),("Stem Cells","1"),
                                           ("CSF Transfix","L1"),("CSF Super","L1"),("CSF Pellet","L1"),("Whole Blood\nPBMC","L1"),("Serum","L1"),
                                           ("Whole Blood\nDNA Isolation","L1"),("Whole Blood\nGene Expression","L1"),
                                           ("CSF Transfix","2"),("CSF Super","2"),("CSF Pellet","2"),("Stem Cells","2"),
                                           ("CSF Transfix","4"),("CSF Super","4"),("CSF Pellet","4"),("Stem Cells","4"),
                                           ("Stem Cells","6"),
                                           ("CSF Transfix","8"),("CSF Super","8"),("CSF Pellet","8"),("Stem Cells","8"),
                                           ("CSF Transfix","10"),("CSF Super","10"),("CSF Pellet","10"),("Stem Cells","10"),
                                           ("Stem Cells","12"),
                                           ("Stem Cells","PT")]
                            )   
    # A list of clinical trial objects to iterate through:
    clinical_trials = [reboot,reveal,graduate,beat_ms]

    # Create a DataFrame we will append the results of each clinical trial to:
    output = pd.DataFrame(columns = ["Study","Cohort","Visit Number","Visit Ordinal","DaysPostScreening","Sample Type","Number at least 1 collected",
                                     "Number of recorded visits","Percent"])
    
    try:
        # For each clinical trial...
        for trial in clinical_trials:
            # If the trial has a list of cohorts...
            if type(trial.cohort) == list:
                # For each cohort...
                for chrt in trial.cohort:
                    # Get data from LV
                    lv_data = querying.get_lv_data(pd,cnxn,trial,chrt)
                    # Get RHO data
                    rho_data = querying.get_rho_data(pd,cnxn,trial,chrt)
                    # Get visit ordinals, etc. from server
                    visit_info = querying.get_visit_info(pd,cnxn,trial)
                    # If we are analyzing the first cohort:
                    if trial.cohort[0] == chrt:
                        # Analyze the data
                        result = create_result_df.create_result_df(pd,trial,chrt,rho_data,lv_data,visit_info)
                        # Remove exceptions
                        result = create_result_df.remove_exceptions(np,result,trial,chrt)
                    # Otherwise...
                    else:
                        # Analyze the data
                        result_to_add = create_result_df.create_result_df(pd,trial,chrt,rho_data,lv_data,visit_info)
                        # Remove exceptions
                        result_to_add = create_result_df.remove_exceptions(np,result_to_add,trial,chrt)
                        # Concatenate to the result DataFrame
                        result = pd.concat([result,result_to_add])
            # Otherwise if the study does not have cohorts...
            else:
                # Get data from LV
                lv_data = querying.get_lv_data(pd,cnxn,trial,None)
                # Get RHO data
                rho_data = querying.get_rho_data(pd,cnxn,trial,None)
                # Get visit ordinals, etc. from server
                visit_info = querying.get_visit_info(pd,cnxn,trial)
                # Analyze the data
                result = create_result_df.create_result_df(pd,trial,chrt,rho_data,lv_data,visit_info)
                # Remove exceptions
                result = create_result_df.remove_exceptions(np,result,trial,None)
            
            # Concatenate to the result DataFrame            
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

        ### TEMPORARY PLACEHOLDER FOR SITE CODE ###
        output["sitecode"] = None
        site_column = output.pop("sitecode")
        output.insert(5,"sitecode",site_column)
        #########

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
                  str(e.__class__),
                  str(e),
                  datetime.datetime.now().isoformat().encode('utf-8'),
                  str(datetime.datetime.now())[:19].replace('-', '/'))
        cursor.execute("{CALL [dbo].[SSIS_Process_LogHistory] (?,?,?,?,?,?,?,?,?,?)}", params)
        cnex.commit()
    cnxn.close()
    print("Processing Complete. src_func_final processed")


        