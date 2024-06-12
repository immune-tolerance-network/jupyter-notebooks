
def get_lv_data(pd,cnxn,ct, cohort):
    
    lv_query = None
    if cohort == None:
        lv_query = '''SELECT * FROM rpt.LabVantageVisits WHERE studynum = '{}' '''.format(ct.studynum)
    else:
        lv_query = '''SELECT * FROM rpt.LabVantageVisits WHERE studynum = '{}' AND Cohort = '{}' '''.format(ct.studynum,cohort)
    output_df = pd.read_sql(lv_query,cnxn)

    output_df = output_df[['studynum',  'Participant', 'KitBarcode',
                            'CollectionDate',  'specimentype',
                            'visitnum', 'barcode', 'Sample Comment', 'Cohort', 'storagestatus',
                            'storagedisposalstatus', 'Shipping Status']]
    output_df = output_df[~output_df["storagedisposalstatus"].isin(['lostOrDamaged', 'Missing'])]
    if ct.studynum == "ITN080AI":
        output_df.drop(output_df[(output_df["barcode"] == "340236")].index, inplace = True)
    
    # Rename and specify sample types only for non-graduate
    #if ct.studynum != "ITN084AD" and ct.studynum != "ITN062ST":
    if  (isinstance(ct.specimen_types,dict)): 
        def specify_sample_type(bcde):
            # Turn the barcode into a list where the first entry is the kit and the second entry is the suffix
            bcde_components = bcde.split("-")
            # Get the suffix
            suffix = bcde_components[1]
            
            specimen_type_keys = list(ct.specimen_types.keys())
            #print(suffix)
            for s_t in specimen_type_keys:
                if suffix in ct.specimen_types[s_t]:
                    return s_t
            return None

        output_df["specimentype"] = output_df.apply(lambda x:specify_sample_type(x["barcode"]),axis = 1)

    # custom data cleaning for graduate:
    if ct.studynum == "ITN084AD":
        def assign_visit(kit,vis):
            if vis == None:
                if kit == "447410":
                    return "S3"
                elif kit == "715208":
                    return "0"
                elif kit == "822140":
                    return "-2"
                else:
                    return vis
            else:
                return vis
            
        def assign_pid(kit,pid):
            if pid == None:
                if kit == "447410":
                    return "11651"
                elif kit == "715208":
                    return "11539"
                elif kit == "822140":
                    return "11302"
                else:
                    return pid
            else:
                return pid
            
        output_df["visitnum"] = output_df.apply(lambda x: assign_visit(x["KitBarcode"],x["visitnum"]),axis = 1)
        output_df["Participant"] = output_df.apply(lambda x: assign_pid(x["KitBarcode"],x["Participant"]),axis = 1)        

    return output_df

# Get Rho data
def get_rho_data(pd,cnxn,ct,cohort):


    # If there is/n't multiple cohorts for the study
    if ct.cohort != None:
        rho_query = '''SELECT DISTINCT a.[ADINFC STUDYID],a.[RHO Screening Identifier],a.[Cohort],a.[Participant ID],c.VisitKey, c.[Visit Number],c.[Visit Ordinal],c.[DaysPostScreening]
                    FROM   [rpt].[Participant] a
                    JOIN   [rpt].[ParticipantActivity] b
                        ON     a.[ParticipantKey] = b.[ParticipantKey]
                        AND    b.[Activity] IN ('Visit','UnscheduledVisit')
                    JOIN   [rpt].[Visit] c
                        ON     b.[VisitKey] = c.[VisitKey]
                    JOIN   [rpt].[Site] d
                        ON     a.[SiteKey] = d.[SiteKey]
                    WHERE  a.[ADINFC STUDYID] = '{}' AND Cohort = 'Part {}' '''.format(ct.studynum,cohort)
    else:
        rho_query = '''SELECT DISTINCT a.[ADINFC STUDYID],a.[RHO Screening Identifier],a.[Cohort],a.[Participant ID], c.VisitKey, c.[Visit Number],c.[Visit Ordinal],c.[DaysPostScreening]
                    FROM   [rpt].[Participant] a
                    JOIN   [rpt].[ParticipantActivity] b
                        ON     a.[ParticipantKey] = b.[ParticipantKey]
                        AND    b.[Activity] IN ('Visit','UnscheduledVisit')
                    JOIN   [rpt].[Visit] c
                        ON     b.[VisitKey] = c.[VisitKey]
                    JOIN   [rpt].[Site] d
                        ON     a.[SiteKey] = d.[SiteKey]
                    WHERE  a.[ADINFC STUDYID] = '{}'  '''.format(ct.studynum)
    # Turn query results into a dataframe
    output_df = pd.read_sql(rho_query,cnxn)

    # Fix the lack of pids
    def fix_no_pid_rho(rho_si,pid):
        if pid == None:
            rho_si_components = rho_si.split("-")
            return rho_si_components[2]
        else:
            return pid
    output_df["Participant ID"] = output_df.apply(lambda x: fix_no_pid_rho(x["RHO Screening Identifier"],x["Participant ID"]),axis = 1)
    return output_df

def get_visit_info(pd,cnxn,ct):

    visit_query = '''SELECT a.[Study Number],b.[Visit Number],b.[Visit Ordinal],b.[DaysPostScreening] FROM rpt.Study a
                    JOIN rpt.Visit b
                        ON a.[StudyKey] = b.[Studykey]
                        WHERE a.[Study Number] = '{}'
                        ORDER BY [Visit Ordinal]
                    '''.format(ct.studynum)
    output_df = pd.read_sql(visit_query,cnxn)

    return output_df