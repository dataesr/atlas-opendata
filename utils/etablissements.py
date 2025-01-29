import numpy as np
import pandas as pd

def etablissements(current_year):
    liste_gentab=[]
    for i in range(2015,current_year,1):
        liste_gentab.append(pd.read_json(f"./POST_GENTAB/atlas{i}.json"))
    df_etab=pd.concat(liste_gentab)
    df_etab=df_etab[['RENTREE', 'ETABLISSEMENT', 'SECT', 'ETABLI', 'SIGLE_M', 'LIB1_M', 'LIB2_M', 'COMPOS', 'SIGLE_U', 'LIB1_U', 'LIB2_U', 'REG_ID', 'REG_NOM', 
    'ACA_ID', 'ACA_NOM', 'DEP_ID', 'DEP_NUM_NOM', 'UUCR_ID', 'UUCR_NOM', 'COM_CODE', 'COM_NOM', 'DEGETU', 'SEXE','EFFSDC']]
    dict_a={'RENTREE':'rentree','EFFSDC':'effectifhdccpge','SECT':'secteur_etablissement','ETABLI':'id_etablissement','SIGLE_M':'sigle_etablissement',
            'LIB1_M':'libelle_etablissement_1','LIB2_M':'libelle_etablissement_2','COMPOS':'id_composante', 'ETABLISSEMENT':'categorie_etablissement',
            'LIB2_U':'libelle_composante_2','LIB1_U':'libelle_composante_1','SIGLE_U':'sigle_composante',
            'REG_ID':'reg_id','ACA_ID':'aca_id','DEP_ID':'dep_id','UUCR_ID':'uucr_id','COM_CODE':'com_code',
            'REG_NOM':'reg_nom','ACA_NOM':'aca_nom','DEP_NUM_NOM':'dep_num_nom','UUCR_NOM':'uucr_nom','COM_NOM':'com_nom','DEGETU':'degetu'}
    df_etab=df_etab.rename(columns=dict_a)
    df_etab['dont_femmes'] = df_etab.apply(lambda row: row['effectifhdccpge'] if row['SEXE'] == 2 else 0, axis = 1)
    df_etab['dont_hommes'] = df_etab.apply(lambda row: row['effectifhdccpge'] if row['SEXE'] == 1 else 0, axis = 1)
    df1=df_etab[df_etab.rentree.isin([2015,2016,2017,2018,2019,2020])].groupby(['rentree', 'categorie_etablissement', 'secteur_etablissement',
        'id_etablissement', 'sigle_etablissement', 'libelle_etablissement_1',
        'libelle_etablissement_2', 'id_composante', 'sigle_composante',
        'libelle_composante_1', 'libelle_composante_2', 'reg_id', 'reg_nom',
        'aca_id', 'aca_nom', 'dep_id', 'dep_num_nom', 'uucr_id', 'uucr_nom',
        'com_code', 'com_nom']).agg({'effectifhdccpge':'sum','dont_hommes':'sum','dont_femmes':'sum'})
    df2=df_etab[df_etab.rentree.isin([2021,2022,2023])].groupby(['rentree', 'categorie_etablissement', 'secteur_etablissement',
        'id_etablissement', 'sigle_etablissement', 'libelle_etablissement_1',
        'libelle_etablissement_2', 'id_composante', 'sigle_composante',
        'libelle_composante_1', 'libelle_composante_2', 'reg_id', 'reg_nom',
        'aca_id', 'aca_nom', 'dep_id', 'dep_num_nom', 'uucr_id', 'uucr_nom',
        'com_code', 'com_nom', 'degetu']).agg({'effectifhdccpge':'sum','dont_hommes':'sum','dont_femmes':'sum'})
    df1=df1.reset_index()
    df2=df2.reset_index()
    df_etab2=pd.concat([df1,df2])
    dic_degetu = {'0':'Inférieur ou égal au baccalauréat','1':'BAC + 1','2':'BAC + 2','3':'BAC + 3','4':'BAC + 4','5':'BAC + 5','6':'BAC + 6 et plus'}
    dic_etablissement = {'archi':"Écoles d'architecture",'art':'Écoles supérieures artistiques et culturelles','autre':'Autres écoles de spécialités diverses','AUTRE UNIV':"Autre établissements d'enseignement universitaire",'autre univ':"Autre établissements d'enseignement universitaire",'commerce':'Écoles de commerce, gestion et vente','ens':'Écoles normales supérieures','gd etab':'Grands établissements','inge':"Écoles d'ingénieurs",'inp ut':'Instituts nationaux polytechniques et universités de technologie','journalism':'Écoles de journalisme et écoles littéraires','journalisme':'Écoles de journalisme et écoles littéraires','jurid adm':'Écoles juridiques et administratives','lycee':'Lycées','paramedica':'Écoles paramédicales hors université','paramedical':'Écoles paramédicales hors université','social':'Écoles préparant aux fonctions sociales','univ priv':"Établissements d'enseignement universitaire privés",'universite':'Universités','veto':'Écoles vétérinaires','':np.nan}
    dic_secteur = {'PR':'Privé','PU':'Public'}
    df_etab2['degre_etudes']=df_etab2.loc[:,'degetu'].apply(lambda x: dic_degetu[str(int(x))] if pd.isna(x)==False else np.nan)
    df_etab2.loc[:,'categorie_etablissement']=df_etab2.loc[:,'categorie_etablissement'].apply(lambda x: dic_etablissement[x] if (pd.isna(x)==False) else np.nan)
    df_etab2.loc[:,'secteur_etablissement']=df_etab2.loc[:,'secteur_etablissement'].apply(lambda x: dic_secteur[x] if pd.isna(x)==False else np.nan)
    df_etab2=df_etab2[['rentree', 'categorie_etablissement', 'secteur_etablissement',
        'id_etablissement', 'sigle_etablissement', 'libelle_etablissement_1',
        'libelle_etablissement_2', 'id_composante', 'sigle_composante',
        'libelle_composante_1', 'libelle_composante_2', 'reg_id', 'reg_nom',
        'aca_id', 'aca_nom', 'dep_id', 'dep_num_nom', 'uucr_id', 'uucr_nom',
        'com_code', 'com_nom', 'degetu', 'degre_etudes',
        'effectifhdccpge', 'dont_femmes', 'dont_hommes']]
    return df_etab2