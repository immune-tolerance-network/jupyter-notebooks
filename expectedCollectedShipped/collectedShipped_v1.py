# %%
# Import libraries
import pyodbc
import pandas as pd
from datetime import date
import re
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

    shipments = {}
    collections = {}

    # Retrieve Data
    query1 = "SELECT studynum,sitecode,Participant,KitBarcode,CollectionDate,tubetype,specimentype," \
             "barcode,visitnum,cohort" \
             " FROM rpt.vw_LabVantageVisits WHERE studynum='ITN080AI'"
    query2 = "SELECT StudyNum,SiteCode,Participant,VisitNum,kitbarcode,barcode,tubetype,specimentype," \
             "Activity,ShipDate,airbillnumber,ShipmentID" \
             " FROM rpt.vw_LabVantageShipments WHERE StudyNum='ITN080AI'"

    try:
        collections = pd.read_sql(query1, cnxn)
        shipments = pd.read_sql(query2, cnxn)

        # %%
        # Remove barcodes in lv shipments if their packages have been created or cancelled, but not shipped
        shipments = shipments[(shipments["Activity"] != "Cancelled") | (shipments["Activity"] != "Created")]

        # %%
        site_code_to_abbreviation = {
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

        sitecode_to_sitename = {"70125": "Ohio State University",
                                "70200": "University of Miami",
                                "70212": "University of North Carolina"}

        # %%
        # Get a list of unique barcodes that were collected / shipped
        lv_barcodes = collections["barcode"].unique()
        if None in lv_barcodes:
            lv_barcodes.remove(None)
        shipped_barcodes = shipments["barcode"].unique()

        result_df = pd.DataFrame(columns=['studynum', 'sitecode', 'Participant', 'KitBarcode', 'CollectionDate',
                                          'tubetype', 'specimentype', 'barcode', 'visitnum', 'cohort', 'message',
                                          'days overdue', 'alert'])

        barcode_pattern = re.compile(r'^\d\d\d\d\d\d-...?$')

        # If you can't find a barcode from lv collections in lv shipments, print an error message
        for i in collections["barcode"].unique():
            if i not in shipped_barcodes:
                # print(collections[collections["barcode"]==i].columns)
                alert = None
                message_components = collections[collections["barcode"] == i].values.flatten().tolist()
                days_since = message_components[4]-date.today()
                message = "{0}-{1}: Tube with barcode {2} has been collected but not shipped!" \
                          " It is for participant {3}" \
                          " at site {4} for visit {5} collected on {6}" \
                          " (overdue by {7} days).".format(message_components[0],
                                                           message_components[1],
                                                           message_components[7],
                                                           message_components[2],
                                                           site_code_to_abbreviation[message_components[1]],
                                                           message_components[8], message_components[4],
                                                           abs(days_since.days))

                if not barcode_pattern.match(message_components[7]):
                    message += " WARNING: Barcode does not match expected format of ######-xy or ######-xyz"
                    alert = "Barcode does not match expected format"
                message_components.append(message)
                message_components.append(abs(days_since.days))
                message_components.append(alert)
                result_df.loc[len(result_df)] = message_components

                # print(message_components)
                # print(message)

        # %%
        result_df.sort_values(by=["days overdue"])

        # exceptions:
        # PBMC Na Hep Tubes
        result_df.drop(result_df[(result_df["tubetype"] == "04 ml Na Heparin") |
                                 (result_df["tubetype"] == "10 ml Na Heparin") |
                                 (result_df["tubetype"] == "06 ml Na Heparin")].index, inplace=True
                       )

        # %%
        crsr = cnxn.cursor()
        crsr.execute('''DELETE FROM input.pythonCollectedShipped WHERE [Study Number]='ITN080AI' ''')
        crsr.commit()
        crsr.fast_executemany = True

        insert_string = '''INSERT INTO [DAVE].[input].[pythonCollectedShipped]
         (
            [Study Number],[Site Code],[Participant ID],[Kit Barcode],[Collection Date],[Tube Type],
            [Specimen Type],[Barcode],[Visit Number],[STS Cohort],[Message],[Days Overdue],[Alerts]
            ) VALUES 
            (?,?,?,?,?,?,?,?,?,?,?,?,?)'''

        tuples = [(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12])
                  for i in result_df.values.tolist()]

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
                  'collectedShipped_v1 ETL',
                  str(e.__class__),
                  str(e),
                  datetime.datetime.now().isoformat().encode('utf-8'),
                  str(datetime.datetime.now())[:19].replace('-', '/'))
        cursor.execute("{CALL [dbo].[SSIS_Process_LogHistory] (?,?,?,?,?,?,?,?,?,?)}", params)
        cnex.commit()
        cnex.commit()

    cnxn.close()

    print("Processing Complete. collectedShipped_v1 Processed ")

# print("end.")
