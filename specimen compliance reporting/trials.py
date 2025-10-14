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
                                    "B":['0B', '1B', '3B', '5B', '7B', '8B','9B', '10B', '11B', '12B', '13B', '14B', '15B', '16B', '17B','DVB']},
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

# clinical_trial object for T1DES:
t1des = clinical_trial(studynum = "ITN066AI",
                       visits = ['-1','0','1' ,'2' ,'3' ,'4' ,'5' ,'6' ,'7' ,'8' ,'9' ,'10' ,
                                 '11' ,'12' ,'13' ,'14' ,'15' ,'16' ,'17' ,'18' ,'19' ,'20' ,
                                 '21' ,'22' ,'23' ,'24' ,'25' ,'26' ,'27' ,'28' ,'29' ,'30' ,
                                 '31' ,'32' ,'33' ,'34' ,'35' ,'36' ,'37' ,'38' ,'39' ,'40' ,
                                 '41' ,'42' ,'43' ,'44' ,'45' ,'46' ,'47' ,'48' ,'49' ,'50' ,
                                 '51' ,'52' ,'53' ,'54' ,'55' ,'56' ,'57' ,'58' ,'59' ,'60' ,
                                 '61' ,'62' ,'63' ,'64' ,'65' ,'66' ,'67' ,'68' ,'69' ,'70' ,
                                 '71' ,'72' ,'73' ,'74' ,'75' ,'76' ,'77' ,'78' ,'79' ,'80' ,
                                 '81' ,'82' ,'83' ,'84' ,'85' ,'86' ,'87' ,'88' ,'89' ,'90' ,
                                 '91' ,'92' ,'93' ,'94' ,'95' ,'96' ,'97' ,'98' ,'99' ],
                        cohort = None,
                        specimen_types = {"Serum":['H01', 'H02', 'H03', 'H04', 'H05', 'H06', 'H07', 'H08', 'H09', 'H10', 'H11', 'H12', 'H13', 'H14', 'H15', 'H16'],
                                          "PBMC":['10A', '10B', '10C', '10D', '10E', '10F', '10G', '10H', '10I', '10J', '10K', '10L', '10M'],
                                          "Plasma/MMTT":['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10', 'S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S18', 'S19', 'S20', 
                                                         'S21', 'S22', 'S23', 'S24', 'S25', 'S26', 'S27', 'S28', 'S29', 'S30', 
                                                         'S31', 'S32', 'S33', 'S34', 'S35', 'S36', 'S37', 'S38', 'S39', 'S40', 'S41', 'S42', 'S43', 'S44'],
                                            "Gene Expression\nWhole Blood":["9A","9B","9C","9D"]},
                            exceptions=[])

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
                            visits = ['0','1','2','4','6','8','10','12','UR1','UR2','UR3','UR4','UR5','UR6','UR7','UR8','UR9','PT','L1','RL1'],
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
                                                                                
                                        ("CSF Transfix","2"),("CSF Super","2"),("CSF Pellet","2"),("Stem Cells","2"),
                                        ("CSF Transfix","4"),("CSF Super","4"),("CSF Pellet","4"),("Stem Cells","4"),
                                        ("Stem Cells","6"),
                                        ("CSF Transfix","8"),("CSF Super","8"),("CSF Pellet","8"),("Stem Cells","8"),
                                        ("CSF Transfix","10"),("CSF Super","10"),("CSF Pellet","10"),("Stem Cells","10"),
                                        ("Stem Cells","12"),
                                        ("Stem Cells","UR1"),
                                        ("Stem Cells","UR2"),
                                        ("Stem Cells","UR3"),
                                        ("Stem Cells","UR4"),
                                        ("Stem Cells","UR5"),
                                        ("Stem Cells","UR6"),
                                        ("Stem Cells","UR7"),
                                        ("Stem Cells","UR8"),
                                        ("Stem Cells","UR9"),
                                        
                                        ("Stem Cells","PT"),
                                        ("CSF Transfix","L1"),("CSF Super","L1"),("CSF Pellet","L1"),("Whole Blood\nPBMC","L1"),("Serum","L1"), ("Whole Blood\nDNA Isolation","L1"),("Whole Blood\nGene Expression","L1"),
                                        ("CSF Transfix","RL1"),("CSF Super","RL1"),("CSF Pellet","RL1"),("Whole Blood\nPBMC","RL1"),("Serum","RL1"),("Whole Blood\nDNA Isolation","RL1"),("Whole Blood\nGene Expression","RL1")]
                        )   

# DARE APS
dare_aps = clinical_trial(studynum="ITN093AI",
                          visits = ['-1','0','4','8','9','10','11','12','13','DC'],
                          cohort = None,
                          specimen_types={"PBMC":['10A','10B','10C','10D','10E','10F','10G','51'],
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
                         specimen_types={'Kidney Biopsy':["AE01","AE02"],
                                         'PBMC\n(Processed at PBMC Lab)':['10A','10B','10C','10D'],
                                         'PBMC\n(Processed On-Site)':["F"+str(num) for num in range(40,48)],
                                         "Serum":["H"+str(num).rjust(2,'0') for num in range(1,11)],
                                         "Whole Blood RNA":['9A'],
                                         "Plasma":["S0"+str(num) for num in range(1,7)],
                                         "Whole Blood DNA":['51','52','53','54'],
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
                             ('Kidney Biopsy','5'),("Whole Blood DNA",'5'),
                             ('Kidney Biopsy','6'),('PBMC\n(Processed at PBMC Lab)','6'),('PBMC\n(Processed On-Site)','6'),("Serum",'6'),("Whole Blood DNA",'6'),("Whole Blood RNA",'6'),("Urine Super",'6'),("Urine Pellet",'6'),
                             ('Kidney Biopsy','7'),('PBMC\n(Processed at PBMC Lab)','7'),('PBMC\n(Processed On-Site)','7'),("Serum",'7'),("Whole Blood DNA",'7'),("Whole Blood RNA",'7'),("Urine Super",'7'),("Urine Pellet",'7'),
                             ('Kidney Biopsy','8'),("Whole Blood DNA",'8'),
                             ('Kidney Biopsy','9'),('PBMC\n(Processed at PBMC Lab)','9'),('PBMC\n(Processed On-Site)','9'),("Serum",'9'),("Whole Blood DNA",'9'),("Whole Blood RNA",'9'),("Urine Super",'9'),("Urine Pellet",'9'),
                             ('Kidney Biopsy','10'),('PBMC\n(Processed at PBMC Lab)','10'),('PBMC\n(Processed On-Site)','10'),("Serum",'10'),("Whole Blood DNA",'10'),("Whole Blood RNA",'10'),("Urine Super",'10'),("Urine Pellet",'10'),
                             ("Whole Blood DNA",'11'),
                             ('Kidney Biopsy','12'),("Whole Blood DNA",'12'),
                             ('Kidney Biopsy','13'),
                             ('Kidney Biopsy','DSC')
                         ])

# ADAPT
adapt = clinical_trial(
                studynum="ITN089ST",
                visits = ['-2', '-1', '0', '8', '9','14_1', '15', '17', '18', '22', '25', '26', 'T0', 'T4','T14',  'TUN1', 'TUN2', 'TUN3', 'TUN4','103', '104', '105', '202', '203', '204', '205', '206',  'A2' ],
                cohort = None,
                specimen_types={"Bone Marrow":["10"+chr(letter) for letter in range(81,88)],
                                "Lymph Node":["22A","22B"],
                                "Serum-None":["H"+str(num).rjust(2,'0') for num in range(1,15)],
                                "Spleen":["18A","18B","18C"],
                                "Whole Blood":["3A"] + ["10"+chr(letter) for letter in range(65,81)]},
                exceptions = [
                    ('Bone Marrow','-2'),('Lymph Node','-2'),('Serum-None','-2'),('Spleen','-2'),
                    ('Bone Marrow','-1'),('Lymph Node','-1'),('Spleen','-1'),
                    ('Bone Marrow',' 8'),('Lymph Node',' 8'),('Spleen',' 8'),
                    ('Bone Marrow',' 9'),('Lymph Node',' 9'),('Spleen',' 9'),
                    ('Bone Marrow',' 17'),('Lymph Node',' 17'),('Spleen',' 17'),
                    ('Bone Marrow',' 18'),('Lymph Node',' 18'),('Spleen',' 18'),
                    ('Bone Marrow',' 22'),('Lymph Node',' 22'),('Spleen',' 22'),
                    ('Bone Marrow',' 25'),('Lymph Node',' 25'),('Spleen',' 25'),
                    ('Bone Marrow',' 26'),('Lymph Node',' 26'),('Spleen',' 26'),
                    ('Bone Marrow',' 103'),('Lymph Node',' 103'),('Spleen',' 103'),
                    ('Bone Marrow',' 104'),('Lymph Node',' 104'),('Spleen',' 104'),
                    ('Bone Marrow',' 105'),('Lymph Node',' 105'),('Spleen',' 105'),
                    ('Bone Marrow',' 202'),('Lymph Node',' 202'),('Spleen',' 202'),
                    ('Bone Marrow',' 204'),('Lymph Node',' 204'),('Spleen',' 204'),
                    ('Bone Marrow',' 205'),('Lymph Node',' 205'),('Spleen',' 205'),
                    ('Bone Marrow',' 206'),('Lymph Node',' 206'),('Spleen',' 206'),
                    ('Bone Marrow',' 14_1'),('Lymph Node',' 14_1'),('Spleen',' 14_1'),
                    ('Bone Marrow',' T14'),('Lymph Node',' T14'),('Spleen',' T14'),
                    ('Bone Marrow',' T4'),('Lymph Node',' T4'),('Spleen',' T4'),
                    ('Bone Marrow',' TUN1'),('Lymph Node',' TUN1'),('Spleen',' TUN1'),
                    ('Bone Marrow',' TUN2'),('Lymph Node',' TUN2'),('Spleen',' TUN2'),
                    ('Bone Marrow',' TUN3'),('Lymph Node',' TUN3'),('Spleen',' TUN3'),
                    ('Bone Marrow',' TUN4'),('Lymph Node',' TUN4'),('Spleen',' TUN4'),
                    ('Lymph Node','0'),('Spleen','0'),
                    ('Lymph Node','15'),('Spleen','15'),
                    ('Lymph Node','203'),('Spleen','203'),
                    ('Bone Marrow','A2'),('Serum-None','A2'),('Spleen','A2'),

                ]

)

# ATTAIN
attain = clinical_trial(
    studynum= 'ITN090ST',
    visits = ['0', '5', '9', '11', '13', '14', '15', 'T0', 'T3', 'T5', '105', '109', '111', 'DT0', 'TUN1', 'TUN2', 'TUN3', 'TUN4', 'TUN5', 'TUN6', 'TUN7', 'TUN8', 'TUN9', 'TUN10', '1005', '1009', '1011', '1013', '1014', '1015', '1016', '1105', '1109', '1111', '1113', '1114', '1116'],
    cohort = None,
    specimen_types={"Bone Marrow":["10"+chr(letter) for letter in range(81,88)],
                    "Lymph Node":["22A","22B"],
                    "Serum-None":["H"+str(num).rjust(2,'0') for num in range(1,15)],
                    "Spleen":["18A","18B","18C"],
                    "Whole Blood":["3A","51"] + ["10"+chr(letter) for letter in range(65,81)]
                    },
    exceptions=[('Lymph Node','0'),('Spleen','0'),
                ('Lymph Node',' 11'),('Spleen',' 11'),
                ('Lymph Node',' 1011'),('Spleen',' 1011'),
                ('Bone Marrow','5'),('Lymph Node','5'),('Spleen','5'),
                ('Bone Marrow',' 9'),('Lymph Node',' 9'),('Spleen',' 9'),
                ('Bone Marrow',' 15'),('Lymph Node',' 15'),('Spleen',' 15'),
                ('Bone Marrow',' 105'),('Lymph Node',' 105'),('Spleen',' 105'),
                ('Bone Marrow',' 109'),('Lymph Node',' 109'),('Spleen',' 109'),
                ('Bone Marrow',' 111'),('Lymph Node',' 111'),('Spleen',' 111'),
                ('Bone Marrow',' 1005'),('Lymph Node',' 1005'),('Spleen',' 1005'),
                ('Bone Marrow',' 1009'),('Lymph Node',' 1009'),('Spleen',' 1009'),
                ('Bone Marrow',' 1013'),('Lymph Node',' 1013'),('Spleen',' 1013'),
                ('Bone Marrow',' 1014'),('Lymph Node',' 1014'),('Spleen',' 1014'),
                ('Bone Marrow',' 1015'),('Lymph Node',' 1015'),('Spleen',' 1015'),
                ('Bone Marrow',' 1016'),('Lymph Node',' 1016'),('Spleen',' 1016'),
                ('Bone Marrow',' 1105'),('Lymph Node',' 1105'),('Spleen',' 1105'),
                ('Bone Marrow',' 1109'),('Lymph Node',' 1109'),('Spleen',' 1109'),
                ('Bone Marrow',' 1111'),('Lymph Node',' 1111'),('Spleen',' 1111'),
                ('Bone Marrow',' 1113'),('Lymph Node',' 1113'),('Spleen',' 1113'),
                ('Bone Marrow',' 1114'),('Lymph Node',' 1114'),('Spleen',' 1114'),
                ('Bone Marrow',' 1116'),('Lymph Node',' 1116'),('Spleen',' 1116'),
                ('Bone Marrow',' 13'),('Lymph Node',' 13'),('Spleen',' 13'),
                ('Bone Marrow',' 14'),('Lymph Node',' 14'),('Spleen',' 14'),
                ('Bone Marrow',' T3'),('Lymph Node',' T3'),('Spleen',' T3'),
                ('Bone Marrow',' T5'),('Lymph Node',' T5'),('Spleen',' T5'),
                ('Bone Marrow',' TUN1'),('Lymph Node',' TUN1'),('Spleen',' TUN1'),
                ('Bone Marrow',' TUN10'),('Lymph Node',' TUN10'),('Spleen',' TUN10'),
                ('Bone Marrow',' TUN2'),('Lymph Node',' TUN2'),('Spleen',' TUN2'),
                ('Bone Marrow',' TUN3'),('Lymph Node',' TUN3'),('Spleen',' TUN3'),
                ('Bone Marrow',' TUN4'),('Lymph Node',' TUN4'),('Spleen',' TUN4'),
                ('Bone Marrow',' TUN5'),('Lymph Node',' TUN5'),('Spleen',' TUN5'),
                ('Bone Marrow',' TUN6'),('Lymph Node',' TUN6'),('Spleen',' TUN6'),
                ('Bone Marrow',' TUN7'),('Lymph Node',' TUN7'),('Spleen',' TUN7'),
                ('Bone Marrow',' TUN8'),('Lymph Node',' TUN8'),('Spleen',' TUN8'),
                ('Bone Marrow',' TUN9'),('Lymph Node',' TUN9'),('Spleen',' TUN9'),
                ('Bone Marrow','DT0'),('Serum-None','DT0'),
                ('Spleen',' T0')

                ]
)

