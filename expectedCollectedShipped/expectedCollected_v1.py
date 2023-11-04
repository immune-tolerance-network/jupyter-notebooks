# %%
# Import libraries
import pyodbc      # Connect to SQL Servers
# Pandas for lv management
import pandas as pd
# Library to deal with date objects
from datetime import date
# Library to deal with differences between 2 dates (for dates between today and expected collection dates)
from datetime import timedelta
# Time for error handling
import datetime as datetime

if __name__ == "__main__":
    print("Starting...")
    # Connect to SQL server to error handling
    # Use below connection string when running in your IDE
    cnex = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'Server=<ServerName>;Database=<DatabaseName>;'
                          'Trusted_Connection=<ConnectionType>;')
    cursor = cnex.cursor()

    # Connect to DIVE and run query
    # Use below connection string when running in your IDE
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'Server=<ServerName>;Database=<DatabaseName>;'
                          'Trusted_Connection=<ConnectionType>;')

    # Retrieve Data
    query = "SELECT * FROM rpt.vw_LabVantageVisits WHERE studynum='ITN080AI' AND barcode NOT LIKE '%-10_'"
    lv = pd.read_sql(query, cnxn)
    query2 = '''SELECT a.[RHO Screening Identifier], a.[Participant ID]
                  , a.[Cohort], a.[Screening Date], a.[Enrollment Date], a.[Complete Date]
                  , a.[Terminate Date], a.[Terminate Reason], a.[Participant Status]
                  , d.[Site], b.[Activity], b.[Visit Date], c.[Visit Number]
                  , c.[Visit Ordinal], c.[Visit Description], c.[VisitCategory]
    FROM   [rpt].[Participant] a
    JOIN   [rpt].[ParticipantActivity] b
           ON     a.[ParticipantKey] = b.[ParticipantKey]
           AND    b.[Activity] IN ('Visit','UnscheduledVisit')
    JOIN   [rpt].[Visit] c
           ON     b.[VisitKey] = c.[VisitKey]
    JOIN   [rpt].[Site] d
           ON     a.[SiteKey] = d.[SiteKey]
    WHERE  a.[StudyKey] = 142
           
    ORDER BY b.[Visit Date]
    '''

    try:
        rho = pd.read_sql(query2, cnxn)

        # %%
        lv["specimentype"] = lv["specimentype"].str.title()

        # %%


        def pid_from_screening_identifier(rho_screening_identifier):
            return rho_screening_identifier[-5:]

        rho["Participant ID"] = rho.apply(lambda x: pid_from_screening_identifier(x["RHO Screening Identifier"]),
                                          axis=1)

        # %%
        expected_visits_for_pid = list()
        dv_visit = ""
        expected_date_weeks_from_0 = list()
        dictionaryA = {"Visit (A)": [0, 1, 2, 3, 4, 7, 10, 13, 17, 18, 19, 20, 21, 22, 23, 24, 25],
                       "Wk (A)": [0, 1, 2, 3, 4, 12, 24, 36, 52, 65, 78, 91, 104, 117, 130, 143, 156],
                       "Time from last (A)": [0, 7, 7, 7, 7, 56, 84, 84, 112, 91, 91, 91, 91, 91, 91, 91, 91]}

        scheduleA = pd.DataFrame(dictionaryA)

        dictionaryB = {"Visit (B)": [0, 1, 3, 5, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                       "Wk (B)": [0, 4, 12, 24, 36, 52, 65, 78, 91, 104, 117, 130, 143, 156],
                       "Time from last (B)": [0, 28, 56, 84, 84, 112, 91, 91, 91, 91, 91, 91, 91, 91]}

        scheduleB = pd.DataFrame(dictionaryB)

        # %%
        A_visit_names = ['0A', '1A', '2A', '3A', '4A', '7A', '10A', '13A', '17A', '18A', '19A',
                         '20A', '21A', '22A', '23A', '24A', '25A']
        A_visit_weeks = [0, 1, 2, 3, 4, 12, 24, 36, 52, 65, 78, 91, 104, 117, 130, 143, 156]
        B_visit_names = ['0B', '1B', '3B', '5B', '7B', '9B', '10B', '11B', '12B', '13B', '14B',
                         '15B', '16B', '17B']
        B_visit_weeks = [0, 4, 12, 24, 36, 52, 65, 78, 91, 104, 117, 130, 143, 156]

        visit_to_week_A = dict(zip(A_visit_names, A_visit_weeks))
        visit_to_week_B = dict(zip(B_visit_names, B_visit_weeks))

        all_visit_names = A_visit_names + B_visit_names
        all_visit_weeks = A_visit_weeks + B_visit_weeks
        all_visit_to_week = dict(zip(all_visit_names, all_visit_weeks))

        # %%
        a_vis = [str(i) + "A" for i in scheduleA["Visit (A)"].unique()]
        a_vis.append("DVA")
        b_vis = [str(int(i)) + "B" for i in scheduleB["Visit (B)"].unique()]
        b_vis.append("DVB")

        all_mechanistic_visits = a_vis + b_vis

        # print(all_mechanistic_visits)

        spectype = ["Serum-Clot", "Urine Pellet", "Urine Super", "Whole Blood"]

        # %%
        dictionary = {"PID": [],
                      "visitnum": [],
                      "specimentype": [],
                      "count": [],
                      "expectDate": [],
                      "cohort": [],
                      "site": []
                      }

        zero_df = pd.DataFrame(dictionary)

        # %%
        rho_pid_with_mech_visit = rho[rho["Visit Number"].isin(all_mechanistic_visits)]
        unique_pids_in_rho = list(rho_pid_with_mech_visit["Participant ID"].unique())
        if None in unique_pids_in_rho:
            unique_pids_in_rho.remove(None)

        unique_pids_in_rho.sort()

        unique_pids_in_lv = list(lv["Participant"].unique())
        unique_pids_in_lv.sort()

        unique_pids = list(set(unique_pids_in_lv+unique_pids_in_rho))

        # %%
        specimen_type = ["Serum-Clot", "Urine Pellet", "Urine Super", "Whole Blood"]

        # DELETE LATER ###
        # unique_pids=['10368']

        # For every participant that has a mechanistic visit...
        for participant in unique_pids:

            # Get data specific to that participant
            data_for_participant = lv[lv["Participant"] == participant]

            # Get the site for the participant
            try:
                site_code_for_participant = list(data_for_participant["sitecode"].unique())[0]
            except IndexError:
                site_code_for_participant = list(rho[(rho["Participant ID"] == participant)]["sitecode"].unique())[0]

            # Get all recorded visits for the participant (in LV and Rho)
            participant_visits_lv = list(data_for_participant["visitnum"].unique())
            participant_visits_rho = list(
                rho_pid_with_mech_visit[rho_pid_with_mech_visit["Participant ID"] ==
                                        participant]["Visit Number"].unique()
            )
            participant_visits = list(set(participant_visits_lv+participant_visits_rho))
            if None in participant_visits:
                participant_visits.remove(None)

            # Find the participant's cohort
            participant_cohort = \
                data_for_participant[data_for_participant["Participant"] == participant]["Cohort"].unique()[0]

            # If the cohort is A:
            if participant_cohort == "A":

                # Set the list of expected visits for that participant
                # to be the list of visits expected for cohort A, without DV
                expected_visits_for_pid = a_vis
                if "DVA" in expected_visits_for_pid:
                    expected_visits_for_pid.remove("DVA")

            # If the cohort is B:
            elif participant_cohort == 'B':

                # Set the list of expected visits for that participant
                # to be the list of visits expected for cohort B, without DV
                expected_visits_for_pid = b_vis
                if "DVB" in expected_visits_for_pid:
                    expected_visits_for_pid.remove("DVB")

            # For every visit we could possibly expect from a participant:
            for visit in expected_visits_for_pid:
                # For each specimen type we can expect:
                for specimen in specimen_type:
                    count = len(data_for_participant[(data_for_participant["visitnum"] == visit) &
                                                     (data_for_participant["specimentype"] == specimen)])
                    if visit == "0A" or visit == "0B":
                        expected_date = \
                            data_for_participant[(data_for_participant["visitnum"] ==
                                                  visit)]["CollectionDate"].unique()[0]
                        # print(participant,visit,specimen,count,expected_date)
                        append_list = [participant, visit, specimen, count, expected_date, participant_cohort,
                                       site_code_for_participant]
                        zero_df.loc[len(zero_df)] = append_list
                    else:
                        visit_0 = "0" + str(participant_cohort)
                        expected_date_v0 =\
                            data_for_participant[(data_for_participant["visitnum"] ==
                                                  visit_0)]["CollectionDate"].unique()[0]
                        if participant_cohort == "A":
                            expected_date_weeks_from_0 = timedelta(weeks=visit_to_week_A[visit])
                        elif participant_cohort == "B":
                            expected_date_weeks_from_0 = timedelta(weeks=visit_to_week_B[visit])

                        expected_date = expected_date_v0 + expected_date_weeks_from_0
                        # print(participant,visit,specimen,count,expected_date)

                        # Create a list that we will append to the output dataframe
                        append_list = [participant, visit, specimen, count, expected_date, participant_cohort,
                                       site_code_for_participant]
                        zero_df.loc[len(zero_df)] = append_list

            has_DV = ("DVA" in participant_visits) or ("DVB" in participant_visits)
            if has_DV:
                dv_visit_name = "DV"+participant_cohort
                expected_date_dv = \
                    data_for_participant[(data_for_participant["visitnum"] == dv_visit_name)]["CollectionDate"].unique()
                if len(expected_date_dv) == 0:
                    expected_date_dv = rho[(rho["Participant ID"] == participant) &
                                           (rho["Visit Number"] == dv_visit_name)]["Visit Date"].unique()[0]
                else:
                    expected_date_dv = expected_date_dv[0]
                for specimen in specimen_type:
                    count = len(data_for_participant[(data_for_participant["visitnum"] == dv_visit_name) &
                                                     (data_for_participant["specimentype"] == specimen)])
                    append_list = [participant, dv_visit_name, specimen, count, expected_date_dv,
                                   participant_cohort, site_code_for_participant]
                    zero_df.loc[len(zero_df)] = append_list

        # %%
        # Turn 10010's 1A to DVA

        # Drop DVA rows first
        zero_df.drop(zero_df[(zero_df["PID"] == "10010") & (zero_df["visitnum"] == 'DVA')].index, inplace=True)

        # Rename
        zero_df.loc[((zero_df["PID"] == "10010") & (zero_df["visitnum"] == "2A")), "visitnum"] = "DVA"

        # %%
        # Remove samples coming after DVA visits
        for i in list(zero_df["PID"].unique()):
            visits_for_pid = list(zero_df[zero_df["PID"] == i]["visitnum"].unique())
            if not (("DVA" in visits_for_pid) or ("DVB" in visits_for_pid)):
                continue
            else:
                if "DVA" in visits_for_pid:
                    dv_visit = "DVA"
                elif "DVB" in visits_for_pid:
                    dv_visit = "DVB"

                dv_expected_date = list(zero_df[(zero_df["PID"] == i) &
                                                (zero_df["visitnum"] == dv_visit)]["expectDate"].unique())[0]
                # print(dv_expected_date)
                zero_df.drop(zero_df[(zero_df["PID"] == i) &
                                     (zero_df["expectDate"] >= dv_expected_date)].index, inplace=True)

        # %%
        # Future Visits
        zero_df.drop(zero_df[zero_df["expectDate"] >= date.today()].index, inplace=True)

        # %%
        # visits 1A,2A,3A where we aren't expecting certain sampletypes
        zero_df.drop(zero_df[(zero_df["visitnum"].isin(['1A', '2A', '3A'])) &
                             (zero_df["cohort"] == 'A') &
                             (zero_df["specimentype"].isin(["Urine Pellet", "Urine Super", "Whole Blood"]))].index,
                     inplace=True)

        # %%
        # make an alert going into the details of count


        def count_alert(specimen, visit, count, participant):
            if specimen == "Serum-Clot":
                if visit == "0A":
                    if count > 20:
                        return "More {} tubes collected than expected for PID {} " \
                               "at visit {}!".format(specimen,
                                                     participant,
                                                     visit)
                    elif count < 20:
                        return "Less {} tubes collected than expected for PID {} " \
                               "at visit {}!".format(specimen,
                                                     participant,
                                                     visit)
                else:
                    if count > 23:
                        return "More {} tubes collected than expected for PID {} " \
                               "at visit {}!".format(specimen,
                                                     participant,
                                                     visit)
                    elif count < 23:
                        return "Less {} tubes collected than expected for PID {} " \
                               "at visit {}!".format(specimen,
                                                     participant,
                                                     visit)
            elif specimen == "Urine Pellet":
                if visit not in ["1A", "2A", "3A"]:
                    if count > 2:
                        return "More {} tubes collected than expected for PID {} " \
                               "at visit {}!".format(specimen,
                                                     participant,
                                                     visit)
                    elif count < 2:
                        return "Less {} tubes collected than expected for PID {} " \
                               "at visit {}!".format(specimen,
                                                     participant,
                                                     visit)
            elif specimen == "Urine Super":
                if visit not in ["1A", "2A", "3A"]:
                    if count > 10:
                        return "More {} tubes collected than expected for PID {} " \
                               "at visit {}!".format(specimen,
                                                     participant,
                                                     visit)
                    elif count < 10:
                        return "Less {} tubes collected than expected for PID {} " \
                               "at visit {}!".format(specimen,
                                                     participant,
                                                     visit)
            elif specimen == "Whole Blood":
                if visit in ["0A", "0B"]:
                    if count > 19:
                        return "More {} tubes collected than expected for PID {} " \
                               "at visit {}!".format(specimen,
                                                     participant,
                                                     visit)
                    elif count < 19:
                        return "Less {} tubes collected than expected for PID {} " \
                               "at visit {}!".format(specimen,
                                                     participant,
                                                     visit)
                else:
                    if count > 15:
                        return "More {} tubes collected than expected for PID {} at visit {}!".format(specimen,
                                                                                                      participant,
                                                                                                      visit)
                    elif count < 15:
                        return "Less {} tubes collected than expected for PID {} " \
                               "at visit {}!".format(specimen,
                                                     participant,
                                                     visit)


        zero_df["alert"] = \
            zero_df.apply(lambda x: count_alert(x["specimentype"], x["visitnum"], x['count'], x["PID"]), axis=1)


        def overdue(tdy, edate):
            return abs((edate-tdy).days)


        zero_df["overdue"] = zero_df.apply(lambda x: overdue(date.today(), x["expectDate"]), axis=1)

        # %%
        zero_df_alerts = zero_df.copy()

        # %%
        zero_df[(zero_df["PID"] == '10368') &
                (zero_df["visitnum"] == '13A') &
                (zero_df['specimentype'] == "Urine Pellet")]["count"].values[0]

        # %%
        # Samples we DO count something for
        zero_df.drop(zero_df[zero_df["count"] != 0].index, inplace=True)

        # %%
        # Create a dictionary that ties site codes to site abbreviations
        site_abb = {
            "70125": "OSU",
            "70200": "UMiami",
            "70212": "UNC",
            "71168": "NIDDK",
            "72173": "MAYOMN",
            "72174": "UPENN",
            "72175": "UAB",
            "72176": "UHN",
            "72177": "SUNNY",
            "72178": "UBC",
            "72179": "SU",
            "72180": "LundLA",
            "72181": "MCJ",
            "72182": "UWPROV",
            "72183": "CUMC",
            "72184": "VU",
            "72185": "UMinn",
            "72401": "WUSL",
            "72432": "UAMS",
            "72433": "JHUSM",
            "72435": "UNMC",
            "72449": "UMich",
            "72450": "CC",
            "72453": "UCSF"
        }

        # Function that creates message we want to send


        def mssg(s_ab, cde, ID, spec, vis, viswk, tdy, edate):
            dte = abs((edate-tdy).days)
            return '''ITN080AI REBOOT - {}/{} - PID {}; {} specimens @ Visit {} (Week {}) {} 
            days overdue for collection (from expected visit)'''.format(s_ab, cde, ID, spec, vis, viswk, dte)

        # Apply the message function

        if len(zero_df) != 0:
            zero_df["MSSG"] = zero_df.apply(lambda x: mssg(site_abb[x["site"]],
                                                           x["site"],
                                                           x["PID"], x["specimentype"],
                                                           x["visitnum"],
                                                           all_visit_to_week[x["visitnum"]],
                                                           date.today(),
                                                           x["expectDate"]),
                                            axis=1
                                            )

        # %%
        zero_df.reset_index(drop=True)
        zero_df["studynum"] = "ITN080AI"

        # %%

        crsr = cnxn.cursor()

        crsr.execute('''DELETE FROM input.pythonExpectedCollected WHERE [Study Number]='ITN080AI' ''')
        crsr.commit()

        crsr.fast_executemany = True
        insert_string = '''INSERT INTO [DAVE].[input].[pythonExpectedCollected] (
                        [Study Number],[Participant ID],[Visit Number],[Specimen Type],
                        [Visit Date],[STS Cohort],[Site Code],[Days Overdue],[Message]
                        ) VALUES (?,?,?,?,?,?,?,?,?)'''
        tuples = [(i[10], i[0], i[1], i[2], i[4], i[5], i[6], i[8], i[9])
                  for i in zero_df.values.tolist()]
        crsr.executemany(insert_string, tuples)
        crsr.commit()
        crsr.close()

    except Exception as e:
        print("Error: ", str(e))
        
        # Log Error to SQL Server
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
                  'Load Expected Collected Shipped to Reporting Server',
                  'DCT-SQL-01',
                  '0E984725-C51C-4BF4-9960-E1C80E27ABA0',
                  'Load_ExpectedCollectedShipped_ToReportingServer',
                  'expectedCollected_v1 ETL',
                  str(e.__class__),
                  str(e),
                  datetime.datetime.now().isoformat().encode('utf-8'),
                  str(datetime.datetime.now())[:19].replace('-', '/'))
        cursor.execute("{CALL [dbo].[SSIS_Process_LogHistory] (?,?,?,?,?,?,?,?,?,?)}", params)
        cnex.commit()
    
    cnxn.close()

    print("Processing Complete. expectedCollected_v1 Processed ")

# print("end.")
