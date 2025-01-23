import numpy as np
import pandas as pd

def importtab(df,CORRECTIFS_dict,CORRECTIFS_dict_esr,corrige_etabli2,corrige_all,annee):
    if ('ANNEE' in df.columns) and ('RENTREE' in df.columns):
        df=df.drop(['ANNEE', 'RENTREE'], axis=1)
    df['ANNEE']=str(annee + 1)
    df['RENTREE']=df['ANNEE']
    df['ETABLI']=df.loc[:,'ETABLI'].astype(str)
    df['COMPOS']=df.loc[:,'COMPOS'].astype(str)
    if 'CURSUS_LMD' in df.columns :
        df['CURSUS_LMD']=df.loc[:,'CURSUS_LMD'].astype(str)
    df['SECT']=df.loc[:,'SECT'].astype(str)
    df['FORMAT']=df.loc[:,'FORMAT'].astype(str)
    df['ACA_U']=df.loc[:,'ACA_U'].astype(str)
    if 'MIN_U' in df.columns :
        df['MINISTER']=df.loc[:,'MIN_U'].astype(str)
    if 'MIN_M' in df.columns :
        df['MIN_M']=df.loc[:,'MIN_M'].astype(str)
    df['FINECOLE']=df.loc[:,'FINECOLE'].astype(str)
    df['COM_U']=df.loc[:,'COM_U'].astype(str)
    df['COM_M']=df.loc[:,'COM_M'].astype(str)
    df['DIPLOM']=df.loc[:,'DIPLOM'].astype(str)
    df['DISCIPLI']=df.loc[:,'DISCIPLI'].astype(str)
    df[['EFFTOT']]=df[['EFFTOT']].apply(pd.to_numeric)

    if 'DNDU' not in df.columns :
        df['DNDU']=df.apply(lambda x: np.nan,axis=1)
    if 'DISCIPLI' not in df.columns :
        df['DISCIPLI']=df.apply(lambda x: np.nan,axis=1)
    if 'CURSUS_LMD' not in df.columns :
        df['CURSUS_LMD']=df.apply(lambda x: np.nan,axis=1)
    if 'FILIERE' not in df.columns :
        df['FILIERE']=df.apply(lambda x: np.nan,axis=1)
    if 'ETABLISSEMENT' not in df.columns :
        df['ETABLISSEMENT']=df.apply(lambda x: np.nan,axis=1)
    if 'UNIV' not in df.columns :
        df['UNIV']=df.apply(lambda x: np.nan,axis=1)
    if 'HSIFA' not in df.columns :
        df['HSIFA']=df.apply(lambda x: np.nan,axis=1)
    if 'HCPGE' not in df.columns :
        df['EFFECTIF_SANS_DOUBLE_COMPTE']=df.apply(lambda x: 0,axis=1)
        df['HCPGE']=df.apply(lambda x: 0,axis=1) 
    if 'DC' not in df.columns :
        df['DC']=df.apply(lambda x: 1,axis=1)
        
    dutbut=pd.DataFrame(CORRECTIFS_dict_esr['O_DUTBUT'])
    dutbut['DIPLOM'] = dutbut['DIPLOM'].astype(str)
    df = pd.merge(df,dutbut[['DIPLOM','CORRESPONDANCEIUT']].rename(columns={'CORRESPONDANCEIUT':'SPECIUT'}),how= 'left', on='DIPLOM') 
    df['SPECIUT']=df['SPECIUT'].apply(lambda x: 'AUTRES' if pd.isna(x) else x)
    df.loc[df['TYP_DIPL'].isin(["01","02","04","05","06","07","08","09","17","UA","UB","UC","UD","UE","UF","UG","UI","UJ","UO","UR","US","UT","UU","UV","UY","XF"]),'DNDU']='DU'
    df.loc[~(df['TYP_DIPL'].isin(["01","02","04","05","06","07","08","09","17","UA","UB","UC","UD","UE","UF","UG","UI","UJ","UO","UR","US","UT","UU","UV","UY","XF"])),'DNDU']='DN'
    lmddont=pd.DataFrame(CORRECTIFS_dict_esr['J_LMDDONT'])
    df['TYP_DIPL']=df.loc[:,'TYP_DIPL'].apply(lambda x: 'TYPE_NA' if x=='NA' else x)
    df = pd.merge(df,lmddont,how= 'left', on='TYP_DIPL')
    df['LMDDONT']=df['LMDDONT'].apply(lambda x: 'AUTRES' if pd.isna(x)==True else x)
    df['LMDDONTBIS']=df['LMDDONTBIS'].apply(lambda x: 'AUTRES' if pd.isna(x)==True else x)
    df.loc[df['DNDU']=='DU','LMDDONTBIS']='DU'
    dg_disc=pd.DataFrame(CORRECTIFS_dict_esr['DISCIPLINES_SISE'])[['GDDISC','DISCIPLI']].drop_duplicates()
    df = pd.merge(df,dg_disc,how= 'left', on='DISCIPLI').drop(['DISCIPLI'], axis=1).rename(columns={'GDDISC':'DISCIPLI'})
    df['DISCIPLI']=df['DISCIPLI'].apply(lambda x: 'AUTRES' if pd.isna(x) else x)
    df.loc[df['DIPLOM'].isin(['6001000','6004000','8000010']),'LMDDONT']='AUTRES'
    df.loc[df['DIPLOM'].isin(['6001000','6004000','8000010']),'LMDDONTBIS']='AUTRES'
     
    df=corrige_all(df, annee, CORRECTIFS_dict)
    if annee==2017:
        df.loc[df['FORMAT']=='soc','ETABLISSEMENT']='social'
        df.loc[df['FORMAT']=='san','ETABLISSEMENT']='paramedica'
    if annee==2016:
        df.loc[(df['COMPOS']=='0684045X'),'COMPOS']='0694045X'
        df.loc[(df['COMPOS']=='0684045X'),'MIN_M']='06'
        df.loc[(df['COMPOS']=='0684045X'),'MIN_U']='06'
        df.loc[(df['COMPOS']=='0684045X'),'NAT_M']='440'
        df.loc[(df['COMPOS']=='0684045X'),'NAT_U']='440'
    if annee==2015:   
        df.loc[(df['COMPOS']=='0755359T')& (pd.isna(df['MIN_M'])),'MIN_U']='38'
        df.loc[(df['COMPOS']=='0755359T')& (pd.isna(df['MIN_M'])),'MIN_M']='38'
        df.loc[(df['COMPOS']=='0161192P')& (pd.isna(df['MIN_M'])),'MIN_U']='38'
        df.loc[(df['COMPOS']=='0161192P')& (pd.isna(df['MIN_M'])),'MIN_M']='38'
    if annee==2015:    
        df.loc[(df['COMPOS']=='0410981U'),'COM_M']='18033'
        df.loc[(df['COMPOS']=='0410981U'),'DEP_ID_etab']='D018'
    if annee==2013:
        df.loc[((df['ETABLI'] == "0692459Y")|(df['ETABLI'] == "0753478Y")|(df['ETABLI'] == "0753486G")|(df['ETABLI'] == "0753494R")|(df['ETABLI'] == "0753742K")|(df['ETABLI'] == "0133968T")|(df['ETABLI'] == "0782019W")),'SECT']='PU'
        df.loc[(df['COMPOS']=='0490890B'),'SECT']='PU'
        df.loc[(df['FORMAT']=='CPESn') & (df['CPESN'] > 0) & (df['CPESN'] != df['EFFTOTN']),'EFFTOTN']=df.loc[(df['FORMAT']=='CPESn') & (df['CPESN'] > 0) & (df['CPESN'] != df['EFFTOTN']),'CPESN']
    if annee==2012:
        df.loc[(df['COMPOS']=='0490890B'),'SECT']='PU'
        df.loc[(df['FORMAT']=='CPESn') & (df['CPESN'] > 0) & (df['CPESN'] != df['EFFTOTN']),'EFFTOTN']=df.loc[(df['FORMAT']=='CPESn') & (df['CPESN'] > 0) & (df['CPESN'] != df['EFFTOTN']),'CPESN']
    df.loc[df['COMPOS']=='0673064S','SECT']='PR'
    df.loc[df['ETABLI']=='0772517T','MINISTER']='23'
    df['ETABLI2']=df.loc[:,'ETABLI']
    df['ETABLI2']=df.loc[:,'ETABLI2'].astype(str)
    df=corrige_etabli2(df, CORRECTIFS_dict)
    df.loc[(df['ETABLI']=='0753541S'),'SECT']='PR'
    final_columns=['ANNEE','DEGETU','PAYS_ID','DIPLOM','RENTREE','ENQ','MIN_U', 'MINISTER','SECT','COMPOS','NAT_U','SIGLE_U','LIB1_U','LIB2_U','COM_U','FINECOLE','ETABLI','ETABLI2','ETABLI3','SIGLE_M','LIB1_M','LIB2_M','COM_M','SPECIUT','EFFTOT','EFFTOTN','DC','LMDDONT','LMDDONTBIS','DNDU','DISCIPLI','CURSUS_LMD','FILIERE','ETABLISSEMENT','UNIV','HSIFA','EFFECTIF_SANS_DOUBLE_COMPTE','HCPGE','SEXE','NATION','FORMAT']
    columns=[ x for x in df.columns if x in final_columns]
    df=df[columns]
    return df

def gentab(df, rentree_sco, CORRECTIFS_dict, CORRECTIFS_dict_esr, corrige_rgp2, corrige_rgp3, corrige_op_ing):
    if rentree_sco >= 2021:
        a='rentree, a.dc, a.enq, a.MINISTER, a.sect, a.compos, a.nat_u, a.sigle_u, a.lib1_u, a.lib2_u, a.FINECOLE, a.etabli, a.sigle_m, a.lib1_m, a.lib2_m, a.com_u, a.com_m, a.etabli2, a.speciut, a.efftot, a.EFF_STS_APP, a.EFFSDC, a.sexe, a.univ, a.LMDdont, a.LMDdontbis, a.DNDU, a.DISCIPLI, a.CURSUS_LMD, a.filiere, a.etablissement, a.format, a.degetu' 
    else:
        a='rentree, a.dc, a.enq, a.MINISTER, a.sect, a.compos, a.nat_u, a.sigle_u, a.lib1_u, a.lib2_u, a.FINECOLE, a.etabli, a.sigle_m, a.lib1_m, a.lib2_m, a.com_u, a.com_m, a.etabli2, a.speciut, a.efftot, a.EFF_STS_APP, a.EFFSDC, a.sexe, a.univ, a.LMDdont, a.LMDdontbis, a.DNDU, a.DISCIPLI, a.CURSUS_LMD, a.filiere, a.etablissement, a.format'   
    b='UUCR_ID, b.DEP_ID, b.COM_CODE, b.COM_NOM, b.COM_CODE1, b.COM_CODE2, b.UUCR_NOM, b.SACLAY_ID, b.EPCI_ID, b.DEP_NUM_NOM, b.ACA_ID, b.ACA_NOM, b.REG_ID, b.REG_NOM, b.REGRGP_NOM, b.REG_ID_OLD, b.REG_NOM_OLD'
    d='libell_, d.rgp, d.rgp2, d.rgp3, d.rgp4, d.ING, d.IUT, d.INSPE, d.total, d.format'
    h=['rentree', 'enq', 'MINISTER','sect', 'COMPOS', 'nat_u', 'sigle_u', 'lib1_u', 'lib2_u', 'COM_CODE','COM_NOM', 'COM_CODE1', 'COM_NOM1', 'COM_CODE2', 'COM_NOM2', 'UUCR_ID','UUCR_NOM', 'SACLAY_ID', 'EPCI_ID', 'DEP_ID', 'DEP_NUM_NOM', 'ACA_ID','ACA_NOM', 'REG_ID', 'REG_NOM', 'REGRGP_NOM', 'REG_ID_OLD','REG_NOM_OLD', 'FINECOLE', 'ETABLI', 'COM_CODE_ETAB', 'sigle_m', 'lib1_m','lib2_m', 'UUCR_ID_etab', 'DEP_ID_etab', 'ETABLI2','format', 'speciut', 'libell_', 'rgp', 'rgp2', 'rgp3','rgp4', 'ING', 'IUT', 'INSPE', 'total','LMDdont', 'LMDdontbis', 'DNDU', 'DISCIPLI', 'CURSUS_LMD', 'filiere','etablissement', 'UNIV', 'SEXE']

    A=[x.upper() for x in a.split(', a.')]+['memeCOM']
    B=[x.upper() for x in b.split(', b.')]
    C=['UUCR_ID','DEP_ID','COM_CODE']
    D=[x.upper() for x in d.split(', d.')]
    E=['ETABLI','SECRET']
    F=['COM_CODE','COM_NOM']
    G=['COM_CODE','COM_NOM']
    if rentree_sco >= 2021:
        H=[x.upper() for x in h]+['DEGETU','memeCOM','memeUUCR']
    else:
        H=[x.upper() for x in h]+['memeCOM','memeUUCR']
    
    dict_df_group={'RENTREE': pd.Int64Dtype(),'ENQ': str,'MINISTER': str,'SECT': str,'COMPOS': str,'NAT_U': str,'SIGLE_U': str,'LIB1_U': str,'LIB2_U': str,'COM_CODE': str,'COM_NOM': str,'COM_CODE1': str,'COM_NOM1': str,'COM_CODE2': str,'COM_NOM2': str,'UUCR_ID': str,'UUCR_NOM': str,'SACLAY_ID': str,'EPCI_ID': str,'DEP_ID': str,'DEP_NUM_NOM': str,'ACA_ID': str,'ACA_NOM': str,'REG_ID': str,'REG_NOM': str,'REG_ID_OLD': str,'REG_NOM_OLD': str,'REGRGP_NOM': str,'FINECOLE': str,'ETABLI': str,'SIGLE_M': str,'LIB1_M': str,'LIB2_M': str,'COM_CODE': str,'COM_CODE_ETAB': str,'UUCR_ID_ETAB': str,'DEP_ID_ETAB': str,'ETABLI2': str,'FORMAT': str,'SPECIUT': str,'LIBELL_': str,'RGP': str,'RGP2': str,'RGP3': str,'RGP4': str,'ING': str,'IUT': str,'INSPE': str,'TOTAL': str,'LMDDONT': str,'LMDDONTBIS': str,'DNDU': str,'DISCIPLI': str,'CURSUS_LMD': str,'FILIERE': str,'ETABLISSEMENT': str,'UNIV': str,'SEXE': str,'memeUUCR': str,'memeCOM': str,'EFFTOT': pd.Int64Dtype(),'EFFSDC': pd.Int64Dtype(),'EFF_STS_APP': pd.Int64Dtype()}
    
    if 'HCPGE' in df.columns:
        df.loc[(df['HCPGE']!=0.0),'EFFSDC']=df.loc[(df['HCPGE']!=0.0),'EFFTOT']
        df.loc[(df['HCPGE']==0.0),'EFFSDC']=0
        df['EFFSDC']=df.loc[:,'EFFSDC'].astype('Int64')
    else:
        df['EFFSDC']=df.apply(lambda x: np.nan,axis=1)

    if 'HSIFA' in df.columns:
        df.loc[(df['HSIFA']==0.0),'EFF_STS_APP']=df.loc[(df['HSIFA']==0.0),'EFFTOT']
        df.loc[(df['HSIFA']!=0.0),'EFF_STS_APP']=0
        df['EFF_STS_APP']=df.loc[:,'EFF_STS_APP'].astype('Int64')
    else:
        df['EFF_STS_APP']=df.apply(lambda x: np.nan,axis=1)

    df.loc[df['COM_U']==df['COM_M'],'memeCOM']=True
    df.loc[df['COM_U']!=df['COM_M'],'memeCOM']= False
    df=df.loc[(df['DC']== 1.0) & (df['EFFTOT']>0),:]
    df=df.groupby(A, as_index=False, dropna=False).agg({'EFFTOT': 'sum', 'EFFSDC': 'sum', 'EFF_STS_APP': 'sum'}) 
    communes=pd.DataFrame(CORRECTIFS_dict_esr['LES_COMMUNES'])
    communes['COM_CODE']=communes.loc[:,'COM_CODE'].astype(str)
    df = pd.merge(df[A],communes[B],how= 'left', left_on='COM_U',right_on='COM_CODE')  
    df = pd.merge(df.rename(columns={'COM_M':'COM_CODE_ETAB'}),communes[C].rename(columns={'UUCR_ID':'UUCR_ID_ETAB','DEP_ID':'DEP_ID_ETAB'}),how= 'left', left_on='COM_CODE_ETAB',right_on='COM_CODE')
    del df['COM_CODE_y']
    df=df.rename(columns={'COM_CODE_x':'COM_CODE'})
    df.loc[df['UUCR_ID']==df['UUCR_ID_ETAB'],'memeUUCR']=True
    df.loc[df['UUCR_ID']!=df['UUCR_ID_ETAB'],'memeUUCR']= False

    formats=pd.DataFrame(CORRECTIFS_dict_esr['FORMAT']).drop_duplicates()
        
    df = pd.merge(df,formats[D],how= 'left', on='FORMAT')
    communes['COM_CODE1']=communes.loc[:,'COM_CODE1'].astype(str)
    communes['COM_CODE2']=communes.loc[:,'COM_CODE2'].astype(str)
    df = pd.merge(df,communes[F].rename(columns={'COM_NOM': 'COM_NOM1'}),how= 'left', left_on='COM_CODE1',right_on='COM_CODE')
    del df['COM_CODE_y']
    df=df.rename(columns={'COM_CODE_x':'COM_CODE'})
    df = pd.merge(df,communes[G].rename(columns={'COM_NOM': 'COM_NOM2'}),how= 'left', left_on='COM_CODE2',right_on='COM_CODE')
    del df['COM_CODE_y']
    df=df.rename(columns={'COM_CODE_x':'COM_CODE'})
    for i in dict_df_group:
        df[i]=df[i].astype(dict_df_group[i])
    df=df.groupby(H, as_index=False, dropna=False).agg({'EFFTOT': 'sum', 'EFFSDC': 'sum', 'EFF_STS_APP': 'sum'}) 
    df=corrige_rgp2(df,str(rentree_sco), CORRECTIFS_dict)
    df=corrige_rgp3(df,str(rentree_sco), CORRECTIFS_dict)
    df.loc[((df['ING'] == '')|(pd.isna(df['ING'])) |(df['ING']==None)|(df['ING']=='None')),'ING']='NO_ING'
    df.loc[((df['IUT'] == '')|(pd.isna(df['IUT'])) |(df['IUT']==None)|(df['IUT']=='None')),'IUT']='NO_IUT'
    df.loc[((df['INSPE'] == '')|(pd.isna(df['INSPE'])) |(df['INSPE']==None)),'INSPE']='NO_INSPE'
    df.loc[((df['INSPE'] != '') & (pd.isna(df['INSPE'])==False) & (df['INSPE']!=None) & (df['INSPE']!='NO_INSPE')),'SECT']='PU'
    df.loc[((df['IUT'] != '')|(pd.isna(df['IUT'])==False) |(df['IUT']!=None)|(df['IUT']!='IUT')) & (df['SPECIUT']=='AUTRES'),'IUT']='NO_IUT'
    df['ID']=df.loc[:,'REG_ID']
    df.loc[(df['REG_ID'].isin(["R01","R02","R03","R04","R06"])),'ID']='FD112'
    df=corrige_op_ing(df,rentree_sco, CORRECTIFS_dict)
    df.loc[(df.ETABLI=='0753471R')&(df.RGP3!='STS'),"RGP3"]="GE" #CNAM 
    return df

