import numpy as np
import os
import pandas as pd
from datetime import datetime
from tqdm.notebook import tqdm
tqdm.pandas()

from utils.correcting_features import corrige_all, corrige_etabli2, corrige_rgp2, corrige_rgp3, corrige_op_ing
from utils.etablissements import etablissements
from utils.load_corrections import get_all_correctifs_from_google, load_all_correctifs
from utils.opendata import opendata_atlas
from utils.traitements import importtab, gentab

DATA_PATH=os.getcwd()
url_atlas='https://docs.google.com/spreadsheet/ccc?key=11NFXSIg6gQMCsMa8zWQQyypvvYBEmfyJfF2yytXqgMk&output=xls'
url_esr='https://docs.google.com/spreadsheet/ccc?key=1FwPq5Qw7Gbgj_sBD6Za4dfDDk6ydozQ99TyRjLkW5d8&output=xls'
VARS_atlas=['COM_U','COM_M', 'ETABLI', 'MINISTER', 'DC', 'NATION', 'ETABLI2', 'FORMAT','CURSUS_LMD', 'DISCIPLI','RGP2', 'RGP3','OP_ING','SECRET']
VARS_esr=['O_DUTBUT','J_LMDDONT','DISCIPLINES_SISE','FORMAT','LES_COMMUNES','D_EPE','C_ETABLISSEMENTS']

#get corrections
get_all_correctifs_from_google(url_atlas,VARS_atlas,'_atlas')
get_all_correctifs_from_google(url_esr,VARS_esr,'_esr')
CORRECTIFS_dict_esr = load_all_correctifs('_esr')
CORRECTIFS_dict = load_all_correctifs('_atlas')
formats=pd.DataFrame(CORRECTIFS_dict_esr['FORMAT']).drop_duplicates()
communes=pd.DataFrame(CORRECTIFS_dict_esr['LES_COMMUNES']).drop_duplicates()
communes['pays']=communes.loc[:,'REG_ID'].apply(lambda x: 'Étranger' if x=='R99' else 'France')

#get current year
current_year = int(datetime.now().year)

#create new files with modified and upgraded data 
for rentree_sco in range(2001,current_year):
    df=pd.read_parquet(f"./INPUT/ts{str(rentree_sco)[2:]}d_tot.parquet", engine='fastparquet')
    df.columns=[x.upper() for x in df.columns]
    df_up=importtab(df,CORRECTIFS_dict,CORRECTIFS_dict_esr,corrige_etabli2,corrige_all,rentree_sco)
    df_up2= gentab(df_up, rentree_sco, CORRECTIFS_dict, CORRECTIFS_dict_esr, corrige_rgp2, corrige_rgp3, corrige_op_ing)
    df_up2.to_json(f"./POST_GENTAB/atlas{str(rentree_sco)}.json")
    df_all=opendata_atlas(df_up2,rentree_sco)
    df_all.to_json(f"./OUTPUT_OPENDATA/atlas{rentree_sco}.json", orient='records')

#concatenate the data for all years
df1=pd.read_json(f"./OUTPUT_OPENDATA/atlas2001.json")
for i in range(2002,current_year,1):
    df2=pd.read_json(f"./OUTPUT_OPENDATA/atlas{i}.json")
    df1=pd.concat([df1,df2])
df=df1.sort_values(by=["rentree"], ascending=False)
df_tot=df.reset_index()
del df_tot['index']
df_com=df_tot
del df_tot['pays']
df_tot.to_csv("./OUTPUT_OPENDATA/OD_atlas_all.csv", sep=";", encoding="UTF-8", index=False)

#just the citys
df_com=df_com[(df_com.niveau_geo=='COMMUNE')&(df_com.regroupement!='TOTAL')].rename(columns={"geo_id":"com_id", "geo_nom":"com_nom"})
df_com=pd.merge(df_com,communes[['COM_CODE','UUCR_NOM','DEP_NOM','ACA_NOM','REG_NOM']], how='left', left_on='com_id', right_on='COM_CODE')
del df_com['niveau_geo']
del df_com['niveau_geographique']
df_com.to_csv("./OUTPUT_OPENDATA/OD_atlas_all_com.csv", sep=";", encoding="UTF-8", index=False)

#etablissements
df_etab=etablissements(current_year)
df_etab.to_csv("./OUTPUT_OPENDATA/OD_atlas_etab.csv", sep=";", encoding="UTF-8", index=False)













