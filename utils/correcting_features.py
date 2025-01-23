import numpy as np
import pandas as pd

def corrige_com_u(df, CORRECTIFS_dict):
    df['COM_U']=df['COM_U'].astype('str')
    VAR = 'COM_U'
    print(VAR)
    for c in CORRECTIFS_dict[VAR]:
        if c['ANNEE']!= '' :
            if c['COMPOS']!= '' :
                if c['IN'] == "' '":
                    df.loc[((df[VAR] == '')|(df[VAR] is np.nan)) & (df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                else:
                    df.loc[(df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
            else:
                if c['IN'] == "' '":
                    df.loc[((df[VAR] == '')|(pd.isna(df[VAR])) |(df[VAR]==None)) & (df['FINECOLE']==c['FINECOLE']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                else:
                    df.loc[(df['FINECOLE']==c['FINECOLE']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
        else:
            if c['COMPOS']!= '' :
                df.loc[(df['COMPOS']==c['COMPOS']), VAR]=c['OUT']
            else:
                if c['IN'] == "' '":
                    df.loc[(df[VAR] == '') & (df['FINECOLE']==c['FINECOLE']) , VAR]=c['OUT']
                else :
                    if c['FINECOLE'] != '':
                        df.loc[(df[VAR] == c['IN']) & (df['FINECOLE']==c['FINECOLE']) , VAR]=c['OUT']
                    else:
                        df.loc[(df[VAR] == c['IN']) , VAR]=c['OUT']
    return df

def corrige_com_m(df, CORRECTIFS_dict):
    df['COM_M']=df['COM_M'].astype('str')
    VAR = 'COM_M'
    print(VAR)
    for c in CORRECTIFS_dict[VAR]:
        if c['ANNEE']!= '' :
            if c['COMPOS']!= '' :
                if c['IN'] == "' '":
                    df.loc[((df[VAR] == '')|(pd.isna(df[VAR])) |(df[VAR]==None)) & (df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                elif c['ETABLI']!= '' :
                    if c['FORMAT']!= '' :
                        df.loc[(df['FORMAT']==c['FORMAT'])& (df['ETABLI']==c['ETABLI']) & (df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                    else:
                        df.loc[(df['ETABLI']==c['ETABLI']) & (df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                elif c['DIPLOM']!= '' :
                    df.loc[(df['DIPLOM']==c['DIPLOM']) & (df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                elif c['COM_U']!= '' :
                    df.loc[((df['COM_U'] == "' '")|(df['COM_U'] is np.nan)) & (df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                else:
                    if c['OUT'] == 'com_u':
                        df.loc[(df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=df.loc[(df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), 'COM_U']
                    else:
                        df.loc[(df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
            elif c['ETABLI']!= '' :
                df.loc[(df['ETABLI']==c['ETABLI']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
            else:
                df.loc[(df['FINECOLE']==c['FINECOLE']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
        else:
            if c['COMPOS']!= '' :
                df.loc[(df['COMPOS']==c['COMPOS']), VAR]=c['OUT']
            else:
                if c['FINECOLE'] != '':
                    if c['IN'] == "' '":
                        df.loc[((df[VAR] == '')|(pd.isna(df[VAR])) |(df[VAR]==None)) & (df['FINECOLE']==c['FINECOLE']) , VAR]=c['OUT']
                    else:
                        df.loc[(df[VAR] == c['IN']) & (df['FINECOLE']==c['FINECOLE']) , VAR]=c['OUT']
                else :
                    df.loc[(df[VAR] == c['IN']) , VAR]=c['OUT']
    return df

def corrige_etabli(df, CORRECTIFS_dict):
    VAR = 'ETABLI'
    print(VAR)
    for c in CORRECTIFS_dict[VAR]:
        if c['ANNEE']!= '' :
            if c['COMPOS']!= '' :
                if c['IN'] != "''":
                    if c['FORMAT'] != '':
                        df.loc[(df[VAR] == c['IN']) & (df['FORMAT']==c['FORMAT']) & (df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                    else:
                        df.loc[(df[VAR] == c['IN']) & (df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                if c['DIPLOM'] != '':
                    df.loc[(df['DIPLOM']==c['DIPLOM']) & (df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                else:
                    df.loc[(df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
            else:
                if c['DIPLOM'] != '':
                    df.loc[(df[VAR] == c['IN']) & (df['DIPLOM']==c['DIPLOM']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                elif c['FORMAT'] != '':
                    df.loc[(df[VAR] == c['IN']) & (df['FORMAT']==c['FORMAT']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                elif c['CURSUS_LMD'] != '':
                    df.loc[(df[VAR] == c['IN']) & (df['CURSUS_LMD']==c['CURSUS_LMD']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                else:
                    df.loc[(df[VAR] == c['IN']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
        else:
            df.loc[(df['COMPOS']==c['COMPOS']), VAR]=c['OUT']
    return df

def corrige_minister(df, annee, CORRECTIFS_dict):
    VAR = 'MINISTER'
    print(VAR)
    if annee >= 2004 :
        for c in CORRECTIFS_dict[VAR]:
            if c['ANNEE']!= '' :
                df.loc[df['ANNEE']==c['ANNEE'], VAR]=df.loc[df['ANNEE']==c['ANNEE'],c['OUT']]
            else:
                df.loc[(df['ETABLI']==c['ETABLI']), VAR]=c['OUT']
    else:
        return df
    return df

def corrige_dc(df, CORRECTIFS_dict):
    VAR = 'DC'
    print(VAR)
    for c in CORRECTIFS_dict[VAR]:
        df.loc[(df['ANNEE']==c['ANNEE']), VAR]=int(c['OUT'])
    return df

def corrige_nation(df,annee, CORRECTIFS_dict):
    VAR = 'NATION'
    print(VAR)
    if annee >= 2015:
        for c in CORRECTIFS_dict[VAR]:
            df.loc[(df['ANNEE']==c['ANNEE']), VAR]=df.loc[(df['ANNEE']==c['ANNEE']), c['OUT']]
    else:
        return df
    return df

def corrige_etabli2(df, CORRECTIFS_dict):
    VAR = 'ETABLI2'
    print(VAR)
    for c in CORRECTIFS_dict[VAR]:
        if c['COMPOS']!= '' :
            df.loc[(df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
        else:
            if c['ACA_U']!= '' :
                df.loc[(df['ACA_U']==c['ACA_U']) & (df['FORMAT']==c['FORMAT']) & (df['ETABLI']==c['ETABLI']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
            else:
                df.loc[(df['FORMAT']==c['FORMAT']) & (df['ETABLI']==c['ETABLI']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
    return df

def corrige_format(df, CORRECTIFS_dict):
    VAR = 'FORMAT'
    print(VAR)
    for c in CORRECTIFS_dict[VAR]:
        if c['ANNEE']!= '' :
            if c['SECT']!= '' :
                    df.loc[(df[VAR] == c['IN']) & (df['SECT']==c['SECT']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
            elif c['COMPOS']!= '' :
                if c['IN']!= '' :
                    df.loc[(df[VAR] == c['IN']) & (df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                elif c['DIPLOM']!= '' :
                    df.loc[(df['DIPLOM'] == c['DIPLOM']) &(df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                else:
                    df.loc[(df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
            else:
                if c['IN']!= '' :
                    df.loc[(df[VAR] == c['IN']) & (df['ETABLI']==c['ETABLI'])& (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                elif c['NOT IN']!= '' :
                    df.loc[(df[VAR] != c['NOT IN']) & (df['ETABLI']==c['ETABLI']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                elif c['TYP_DIPL']!= '' :
                    if c['NOT DIPLOM']!= '' :
                        df.loc[(df['DIPLOM'] != c['NOT DIPLOM']) & (df['TYP_DIPL']==c['TYP_DIPL']) & (df['ETABLI']==c['ETABLI']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                    else:
                        df.loc[(df['TYP_DIPL']==c['TYP_DIPL']) & (df['ETABLI']==c['ETABLI']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                else:
                    df.loc[(df['ETABLI']==c['ETABLI']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
        else:
            if c['IN']!= '' :
                df.loc[(df[VAR] == c['IN']) & (df['ETABLI']==c['ETABLI']), VAR]=c['OUT']
            else:
                df.loc[(df[VAR] != c['NOT IN']) & (df['ETABLI']==c['ETABLI']), VAR]=c['OUT']
    return df

def corrige_cursus_lmd(df, CORRECTIFS_dict):
    VAR = 'CURSUS_LMD'
    print(VAR)
    for c in CORRECTIFS_dict[VAR]:
        if c['ANNEE']!= '' :
            if c['ETABLI']!= '' :
                if c['IN']== "' '" :
                    df.loc[((df[VAR] == '')|(pd.isna(df[VAR])) |(df[VAR]==None)) & (df['ETABLI']==c['ETABLI']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                else:
                    df.loc[(df[VAR] == c['IN']) & (df['ETABLI']==c['ETABLI']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
            elif c['TYP_DIPL']!= '' :
                df.loc[((df[VAR] == '')|(df[VAR] is np.nan)) & (df['TYP_DIPL']==c['TYP_DIPL']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
            elif c['DIPLOM']!= '' :
                df.loc[((df[VAR] == '')|(df[VAR] is np.nan)) & (df['DIPLOM'] == c['DIPLOM']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
            else:
                if c['IN']== "' '" :
                    df.loc[((df[VAR] == '')|(df[VAR] is np.nan)) & (df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
                else:
                    df.loc[ (df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
        else:
            df.loc[((df[VAR] == '')|(df[VAR] is np.nan)) & (df['ENQ']==c['ENQ']) & (df['ETABLI']==c['ETABLI']) , VAR]=c['OUT']
    return df

def corrige_discipli(df, CORRECTIFS_dict):
    VAR = 'DISCIPLI'
    print(VAR)
    for c in CORRECTIFS_dict[VAR]:
        if c['ETABLI']!= '' :
            df.loc[(df[VAR] == c['IN']) & (df['ETABLI']==c['ETABLI']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
        else:
            if c['IN']== "' '" :
                df.loc[((df[VAR] == '')|(pd.isna(df[VAR])) |(df[VAR]==None)) & (df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
            elif c['IN']== '' :
                df.loc[ (df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
            else:
                df.loc[(df[VAR] == c['IN']) & (df['COMPOS']==c['COMPOS']) & (df['ANNEE']==c['ANNEE']), VAR]=c['OUT']
    return df

def corrige_rgp2(df, annee, CORRECTIFS_dict):
    VAR = 'RGP2'
    print(VAR)
    for c in CORRECTIFS_dict[VAR]:
        df.loc[(df['ETABLI']==c['ETABLI']) & (annee==c['ANNEE']), VAR]=c['OUT']
    return df

def corrige_rgp3(df, annee, CORRECTIFS_dict):
    VAR = 'RGP3'
    print(VAR)
    for c in CORRECTIFS_dict[VAR]:
        if c['NOT IN']== '' :
            df.loc[(df['ETABLI']==c['ETABLI']) & (annee==c['ANNEE']), VAR]=c['OUT']
        else:
            df.loc[(df['ETABLI']==c['ETABLI']) & (df[VAR]!=c['NOT IN']), VAR]=c['OUT']
    return df

def corrige_op_ing(df, annee, CORRECTIFS_dict):
    VAR = 'OP_ING'
    print(VAR)
    for c in CORRECTIFS_dict[VAR]:
        if annee in range(int(c['DEB']),int(c['FIN'])+1,1):
            df.loc[(df['COMPOS']==c['COMPOS'])&(df['ING']=='ING'), 'RGP3']='ING_autres'
            df.loc[(df['COMPOS']==c['COMPOS'])&(df['ING']=='ING'), 'RGP4']='ING_autres'
            df.loc[(df['COMPOS']==c['COMPOS'])&(df['ING']=='NO_ING'), 'RGP3']='EC_autres'
            df.loc[(df['COMPOS']==c['COMPOS'])&(df['ING']=='NO_ING'), 'RGP4']='EC_autres'
    return df

def corrige_all(df,annee,CORRECTIFS_dict):
    return corrige_cursus_lmd(corrige_nation(corrige_minister(corrige_format(corrige_discipli(corrige_etabli(corrige_com_m(corrige_com_u(df, CORRECTIFS_dict), CORRECTIFS_dict), CORRECTIFS_dict), CORRECTIFS_dict), CORRECTIFS_dict),annee, CORRECTIFS_dict),annee, CORRECTIFS_dict), CORRECTIFS_dict)


