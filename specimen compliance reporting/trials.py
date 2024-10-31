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
                                            "CSF Super":["J"+"%02d" % i for i in list(range(1,49))],
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

# DARE APS
dare_aps = clinical_trial(studynum="ITN093AI",
                          visits = ['-1','0','4','8','9','10','11','12','13','DC'],
                          cohort = None,
                          specimen_types={"PBMC\n(Processed at PBMC Lab)":['10A','10B','10C','10D','10E','10F','10G'],
                                          "PBMC\n(Processed On-Site)":['-51'],
                                          "Plasma - Citrated":["S"+str(num).rjust(2,'0') for num in range(1,19)],
                                          "Serum":["H"+str(num).rjust(2,'0') for num in range(1,13)],
                                          "Whole Blood RNA":['9A','9B'],
                                          "Whole Blood DNA":['40','41','42','43','44','45']},
                          exceptions=[("Whole Blood RNA",'-1'),("Whole Blood DNA",'-1'),
                                      ("Whole Blood DNA",'4'),("Whole Blood DNA",'8'),("Whole Blood DNA",'9'),("Whole Blood DNA",'10'),("Whole Blood DNA",'11'),("Whole Blood DNA",'12'),("Whole Blood DNA",'13'),("Whole Blood DNA",'DC')]
                        )

# VIBRANT
vibrant = clinical_trial(studynum="ITN091AI",
                         visits = ['-1','0','1','2','3','4','5','6','7','8','9','10','11','12','13','DSC'],
                         cohort = None,
                         specimen_types={'Kidney Biopsy':["AE01"],
                                         'PBMC\n(Processed at PBMC Lab)':['10A','10B','10C','10D'],
                                         'PBMC\n(Processed On-Site)':[str(num) for num in range(40,48)],
                                         "Serum":["H"+str(num).rjust(2,'0') for num in range(1,11)],
                                         "Whole Blood DNA":['9A'],
                                         "Plasma":["S0"+str(num) for num in range(1,7)],
                                         "Whole Blood RNA":['51','52','53','54'],
                                         "Urine Super": ["D"+str(num).rjust(2,'0') for num in range(1,31)],
                                         "Urine Pellet":["R01","R02"]
                         },
                         exceptions=[
                             ('PBMC\n(Processed at PBMC Lab)','-1'),('PBMC\n(Processed On-Site)','-1'),("Serum",'-1'),("Whole Blood DNA",'-1'),("Plasma",'-1'),("Whole Blood RNA",'-1'),("Urine Super",'-1'),("Urine Pellet",'-1'),
                             ('Kidney Biopsy','0'),
                             ('Kidney Biopsy','1'),('PBMC\n(Processed at PBMC Lab)','1'),('PBMC\n(Processed On-Site)','1'),("Serum",'1'),("Whole Blood DNA",'1'),("Whole Blood RNA",'1'),("Urine Super",'1'),("Urine Pellet",'1'),
                             ('Kidney Biopsy','2'),('PBMC\n(Processed at PBMC Lab)','2'),('PBMC\n(Processed On-Site)','2'),("Serum",'2'),("Whole Blood DNA",'2'),("Whole Blood RNA",'2'),("Urine Pellet",'2'),
                             ('Kidney Biopsy','3'),('PBMC\n(Processed at PBMC Lab)','3'),('PBMC\n(Processed On-Site)','3'),("Serum",'3'),("Whole Blood DNA",'3'),("Whole Blood RNA",'3'),("Urine Super",'3'),("Urine Pellet",'3'),
                             ('Kidney Biopsy','4'),('PBMC\n(Processed at PBMC Lab)','4'),('PBMC\n(Processed On-Site)','4'),("Serum",'4'),("Whole Blood DNA",'4'),("Whole Blood RNA",'4'),("Urine Super",'4'),("Urine Pellet",'4'),
                             ('Kidney Biopsy','5'),
                             ('Kidney Biopsy','6'),('PBMC\n(Processed at PBMC Lab)','6'),('PBMC\n(Processed On-Site)','6'),("Serum",'6'),("Whole Blood DNA",'6'),("Whole Blood RNA",'6'),("Urine Super",'6'),("Urine Pellet",'6'),
                             ('Kidney Biopsy','7'),('PBMC\n(Processed at PBMC Lab)','7'),('PBMC\n(Processed On-Site)','7'),("Serum",'7'),("Whole Blood DNA",'7'),("Whole Blood RNA",'7'),("Urine Super",'7'),("Urine Pellet",'7'),
                             ('Kidney Biopsy','8'),
                             ('Kidney Biopsy','9'),('PBMC\n(Processed at PBMC Lab)','9'),('PBMC\n(Processed On-Site)','9'),("Serum",'9'),("Whole Blood DNA",'9'),("Whole Blood RNA",'9'),("Urine Super",'9'),("Urine Pellet",'9'),
                             ('Kidney Biopsy','10'),('PBMC\n(Processed at PBMC Lab)','10'),('PBMC\n(Processed On-Site)','10'),("Serum",'10'),("Whole Blood DNA",'10'),("Whole Blood RNA",'10'),("Urine Super",'10'),("Urine Pellet",'10'),
                             ('Kidney Biopsy','12'),
                             ('Kidney Biopsy','13'),
                             ('Kidney Biopsy','DSC')
                         ])

