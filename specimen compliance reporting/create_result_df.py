# Create a result dataframe
def create_result_df(pd,ct,choose_cohort,rho_records,lv_data,visit_info):
    # Create the resulting dataframe
    result = pd.DataFrame(columns = ["Study","Cohort","Visit Number","Visit Ordinal","DaysPostScreening","Sample Type","Number at least 1 collected","Number of recorded visits","Percent"])
    
    visit_ord_dict = dict(zip(list(visit_info["Visit Number"]),list(visit_info["Visit Ordinal"])))
    days_post_dict = dict(zip(list(visit_info["Visit Number"]),list(visit_info["DaysPostScreening"])))
    
    if type(ct.cohort) == list:
        for visit in ct.visits[choose_cohort]:
            for sampletype in ct.specimen_types:
                result.loc[len(result)] = [ct.studynum,choose_cohort,visit,visit_ord_dict[visit],days_post_dict[visit],sampletype,None,None,None]
    else:
        for visit in ct.visits:
            for sampletype in ct.specimen_types:
                result.loc[len(result)] = [ct.studynum,None,visit,visit_ord_dict[visit],days_post_dict[visit],sampletype,None,None,None]

    number_of_recorded_visits = []
    def find_collection_stats(std,visnum,spectype):
        # Find the number of PIDs with a visit recorded
        rho_visits = rho_records[rho_records["Visit Number"] == visnum]
        pids_with_recorded_visit_rho = len(list(rho_visits["Participant ID"].unique()))
        pids_with_recorded_visit_lv = len(list(lv_data[lv_data["visitnum"] == visnum]["Participant"].unique()))
        pids_with_recorded_visit = max(pids_with_recorded_visit_rho,pids_with_recorded_visit_lv)
        #if pids_with_recorded_visit_rho != pids_with_recorded_visit_lv:
        #    print(ct.studynum + " " + visnum + ": RHO has {} visits recorded but LV has {} visits recorded".format(str(pids_with_recorded_visit_rho),str(pids_with_recorded_visit_lv)))
        
        # LV data with the specimen type and visit num
        lv_data_visit_spec = lv_data[(lv_data["specimentype"] == spectype) & (lv_data["visitnum"] == visnum)]

        # Number of unique pids that have the spec type for that visit
        pids_at_least_1_tube_for_this_spec_type_for_this_vis = len(list(lv_data_visit_spec["Participant"].unique()))

        percent = 0

        if pids_with_recorded_visit == 0:
            percent = 0
        else:
            percent = 100 * pids_at_least_1_tube_for_this_spec_type_for_this_vis / pids_with_recorded_visit
        
        number_of_recorded_visits.append(pids_with_recorded_visit)


        #print(spectype + " | " + visnum + ": " + str(pids_at_least_1_tube_for_this_spec_type_for_this_vis))

        return pids_at_least_1_tube_for_this_spec_type_for_this_vis, pids_with_recorded_visit,round(percent)

    result[["Number at least 1 collected","Number of recorded visits","Percent"]] = result.apply(lambda x: find_collection_stats(x["Study"],x["Visit Number"],x["Sample Type"]),axis = 1,result_type="expand")
    
    return result

def remove_exceptions(np,table,ct,chrt):
    if chrt != None:
        cohort_exceptions = ct.exceptions[chrt]
        for except_visit in cohort_exceptions:
            exception_indicies = table.index[(table["Sample Type"] == except_visit[0]) & (table["Visit Number"] == except_visit[1])].tolist()
            # table[(table["Sample Type"] == except_visit[0]) & (table["Visit Number"] == except_visit[1])]["Percent"] = np.nan
            table.loc[exception_indicies[0],["Percent"]] = np.nan
    else:
        for except_visit in ct.exceptions:
            exception_indicies = table.index[(table["Sample Type"] == except_visit[0]) & (table["Visit Number"] == except_visit[1])].tolist()
            # table[(table["Sample Type"] == except_visit[0]) & (table["Visit Number"] == except_visit[1])]["Percent"] = np.nan
            table.loc[exception_indicies[0],["Percent"]] = np.nan
    return table
        