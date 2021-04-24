# define equivalence btw actual region names and map region codes
fr_region_codes = {
"Auvergne-Rhône-Alpes":"FR-X7",    
"Bourgogne-Franche-Comté":"FR-X1",
"Bretagne":"FR-E",
"Centre-Val de Loire":"FR-F",
"Corse":"FR-H",
"Grand Est":"FR-X4",
"Guadeloupe":"FR-GP",
"Guyane":"FR-GF",
"Hauts-de-France":"FR-X6",
"La Réunion":"FR-RE",
"Martinique":"FR-MQ",
"Mayotte":"FR-YT",
"Normandie":"FR-X3",
"Nouvelle-Aquitaine":"FR-X2",
"Occitanie":"FR-X5",
"Pays de la Loire":"FR-R",
"Provence-Alpes-Côte d'Azur":"FR-U",
"Île-de-France":"FR-J"
}

# define equivalence btw actual department names and map region codes
fr_department_codes = {
"Ain":"FR-01",
"Aisne":"FR-02",
"Allier":"FR-03",
"Alpes-de-Haute-Provence":"FR-04",
"Hautes-Alpes":"FR-05",
"Alpes-Maritimes":"FR-06",
"Ardèche":"FR-07",
"Ardennes":"FR-08",
"Ariège":"FR-09",
"Aube":"FR-10",
"Aude":"FR-11",
"Aveyron":"FR-12",
"Bouches-du-Rhône":"FR-13",
"Calvados":"FR-14",
"Cantal":"FR-15",
"Charente":"FR-16",
"Charente-Maritime":"FR-17",
"Cher":"FR-18",
"Corrèze":"FR-19",
"Corse-du-Sud":"FR-2A",
"Haute-Corse":"FR-2B",
"Côte-d'Or":"FR-21",
"Côtes-d'Armor":"FR-22",
"Creuse":"FR-23",
"Dordogne":"FR-24",
"Doubs":"FR-25",
"Drôme":"FR-26",
"Eure":"FR-27",
"Eure-et-Loir":"FR-28",
"Finistère":"FR-29",
"Gard":"FR-30",
"Haute-Garonne":"FR-31",
"Gers":"FR-32",
"Gironde":"FR-33",
"Hérault":"FR-34",
"Ille-et-Vilaine":"FR-35",
"Indre":"FR-36",
"Indre-et-Loire":"FR-37",
"Isère":"FR-38",
"Jura":"FR-39",
"Landes":"FR-40",
"Loir-et-Cher":"FR-41",
"Loire":"FR-42",
"Haute-Loire":"FR-43",
"Loire-Atlantique":"FR-44",
"Loiret":"FR-45",
"Lot":"FR-46",
"Lot-et-Garonne":"FR-47",
"Lozère":"FR-48",
"Maine-et-Loire":"FR-49",
"Manche":"FR-50",
"Marne":"FR-51",
"Haute-Marne":"FR-52",
"Mayenne":"FR-53",
"Meurthe-et-Moselle":"FR-54",
"Meuse":"FR-55",
"Morbihan":"FR-56",
"Moselle":"FR-57",
"Nièvre":"FR-58",
"Nord":"FR-59",
"Oise":"FR-60",
"Orne":"FR-61",
"Pas-de-Calais":"FR-62",
"Puy-de-Dôme":"FR-63",
"Pyrénées-Atlantiques":"FR-64",
"Hautes-Pyrénées":"FR-65",
"Pyrénées-Orientales":"FR-66",
"Bas-Rhin":"FR-67",
"Haut-Rhin":"FR-68",
"Rhône":"FR-69",
"Haute-Saône":"FR-70",
"Saône-et-Loire":"FR-71",
"Sarthe":"FR-72",
"Savoie":"FR-73",
"Haute-Savoie":"FR-74",
"Paris":"FR-75",
"Seine-Maritime":"FR-76",
"Seine-et-Marne":"FR-77",
"Yvelines":"FR-78",
"Deux-Sèvres":"FR-79",
"Somme":"FR-80",
"Tarn":"FR-81",
"Tarn-et-Garonne":"FR-82",
"Var":"FR-83",
"Vaucluse":"FR-84",
"Vendée":"FR-85",
"Vienne":"FR-86",
"Haute-Vienne":"FR-87",
"Vosges":"FR-88",
"Yonne":"FR-89",
"Territoire de Belfort":"FR-90",
"Essonne":"FR-91",
"Hauts-de-Seine":"FR-92",
"Seine-Saint-Denis":"FR-93",
"Val-de-Marne":"FR-94",
"Val-d'Oise":"FR-95",
"Guyane française":"FR-GF",
"Guadeloupe":"FR-GP",
"Martinique":"FR-MQ",
"La Réunion":"FR-RE",
"Mayotte":"FR-YT"
}

# SQL query for regions analysis
query_regions = '''SELECT COUNT(aa.nom_comm),aa.nom_region 
            FROM
            (SELECT DISTINCT(fr.nom_comm),fr.voie,cdr.nom_region
            FROM default.france_rues AS fr
            JOIN default.communes_departements_regions AS cdr
            ON fr.code_post=cdr.code_postal
            WHERE fr.voie LIKE '%{}%') AS aa
            GROUP BY aa.nom_region
            ORDER BY aa.nom_region'''

# SQL query for departments analysis            
query_departments = '''SELECT COUNT(aa.voie),aa.nom_departement
            FROM
            (SELECT DISTINCT(fr.nom_comm),fr.voie,cdr.nom_departement
            FROM default.france_rues AS fr
            JOIN default.communes_departements_regions AS cdr
            ON fr.code_post=cdr.code_postal
            WHERE fr.voie LIKE '%{}%') AS aa
            GROUP BY aa.nom_departement
            ORDER BY aa.nom_departement'''