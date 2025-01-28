import pandas as pd
from datetime import datetime

def opendata_atlas(df,annee, CORRECTIFS_dict_esr):
    df.columns=[x.upper() for x in df.columns]
    df.loc[df['REG_ID']!="R99","PAYS_ID"]="PAYS_100"
    df.loc[df['REG_ID']=="R99","PAYS_ID"]="PAYS_999"
    df.loc[(df['IUT']=="IUT")&(df['SPECIUT']=="AUTRES"),"IUT2"]="AUTRE"
    df.loc[(df['IUT']=="IUT")&(df['SPECIUT']!="AUTRES"),"IUT2"]="DUT"
    df.loc[(df['IUT2']=="DUT")&(df['FORMAT'].isin(["iutsec","iutsge","gdiuts"])),"DUT"]="SEC"
    df.loc[(df['IUT2']=="DUT")&(df['FORMAT'].isin(["iutter","iuttge","gdiutt"])),"DUT"]="TER"
    df.loc[(df['RGP3']=="STS")&(df['FORMAT']=="dcesf"),"STS_ASS"]="dce"
    df.loc[(df['RGP3']=="STS")&(df['FORMAT']=="dmapr"),"STS_ASS"]="DMA"
    df.loc[(df['RGP3']=="STS")&(df['FORMAT']=="dmase"),"STS_ASS"]="DMA"
    df.loc[(df['RGP3']=="STS")&(df['FORMAT']=="nivpr"),"STS_ASS"]="NIV"
    df.loc[(df['RGP3']=="STS")&(df['FORMAT']=="nivse"),"STS_ASS"]="NIV"
    df.loc[(df['RGP3']=="STS")&(df['FORMAT']=="stsag"),"STS_ASS"]="STS"
    df.loc[(df['RGP3']=="STS")&(df['FORMAT']=="stspr"),"STS_ASS"]="STS"
    df.loc[(df['RGP3']=="STS")&(df['FORMAT']=="stsse"),"STS_ASS"]="STS"
    df.loc[(df['FORMAT']=="cpgeag"),"FORMAT"]="cpgesc"
    df.loc[df['RGP3']=='UNIV','UNIV']='UNIV'
    df.loc[~df['RGP3'].isin(["ENS","GE","INP","IUFM","UNIV","UT"]),'ETABLI']=""
    df.loc[~df['RGP3'].isin(["ENS","GE","INP","IUFM","UNIV","UT"]),'DISCIPLI']=""
    df.loc[~df['RGP3'].isin(["ENS","GE","INP","IUFM","UNIV","UT"]),'CURSUS_LMD']=""
    df.loc[df['RENTREE'].apply(lambda x: int(x) > 2006),'ETABLI2']=df.loc[df['RENTREE'].apply(lambda x: int(x) > 2006),'ETABLI']
    
    if annee in ["2014","2013","2012","2011","2010","2009","2008","2007"]:
        df=df[['RENTREE','PAYS_ID','REG_ID','ACA_ID','DEP_ID','UUCR_ID','COM_CODE2','COM_CODE','ETABLI','RGP3','FORMAT','SECT','INSPE','IUT','IUT2','ING','TOTAL','LMDDONT','DISCIPLI','CURSUS_LMD','UNIV','STS_ASS','DUT','SEXE','UUCR_NOM','DEP_NUM_NOM','ACA_NOM','REG_NOM','EFFTOT']]
    elif int(annee) > 2016:
        print('ok')
        df=df[['RENTREE','PAYS_ID','REG_ID','ACA_ID','DEP_ID','UUCR_ID','COM_CODE2','COM_CODE','ETABLI','RGP3','FORMAT','SECT','INSPE','IUT','IUT2','ING','TOTAL','LMDDONT','DISCIPLI','CURSUS_LMD','UNIV','STS_ASS','DUT','SEXE','UUCR_NOM','DEP_NUM_NOM','ACA_NOM','REG_NOM','EFFTOT','EFFSDC', 'EFF_STS_APP',]]
    elif annee in ["2006","2005","2004","2003","2002","2001"]:
        df=df[['RENTREE','PAYS_ID','REG_ID','ACA_ID','DEP_ID','UUCR_ID','COM_CODE2','COM_CODE','ETABLI','RGP3','FORMAT','SECT','INSPE','IUT','IUT2','ING','TOTAL','UNIV','STS_ASS','DUT','SEXE','UUCR_NOM','DEP_NUM_NOM','ACA_NOM','REG_NOM','EFFTOT']]
    
    if annee in ["2014","2013","2012","2011","2010","2009","2008","2007"]:
        df=df.groupby(['RENTREE','PAYS_ID','REG_ID','ACA_ID','DEP_ID','UUCR_ID','COM_CODE2','COM_CODE','ETABLI','RGP3','FORMAT','SECT','INSPE','IUT','IUT2','ING','TOTAL','LMDDONT','DISCIPLI','CURSUS_LMD','UNIV','STS_ASS','DUT','SEXE','UUCR_NOM','DEP_NUM_NOM','ACA_NOM','REG_NOM'], as_index=False, dropna=False).agg({'EFFTOT': 'sum'}) 
    elif int(annee) > 2016:
        print('ok')
        df=df.groupby(['RENTREE','PAYS_ID','REG_ID','ACA_ID','DEP_ID','UUCR_ID','COM_CODE2','COM_CODE','ETABLI','RGP3','FORMAT','SECT','INSPE','IUT','IUT2','ING','TOTAL','LMDDONT','DISCIPLI','CURSUS_LMD','UNIV','STS_ASS','DUT','SEXE','UUCR_NOM','DEP_NUM_NOM','ACA_NOM','REG_NOM'], as_index=False, dropna=False).agg({'EFFTOT': 'sum','EFFSDC': 'sum', 'EFF_STS_APP':'sum'}) 
    elif annee in ["2006","2005","2004","2003","2002","2001"]:
        df=df.groupby(['RENTREE','PAYS_ID','REG_ID','ACA_ID','DEP_ID','UUCR_ID','COM_CODE2','COM_CODE','ETABLI','RGP3','FORMAT','SECT','INSPE','IUT','IUT2','ING','TOTAL','UNIV','STS_ASS','DUT','SEXE','UUCR_NOM','DEP_NUM_NOM','ACA_NOM','REG_NOM'], as_index=False, dropna=False).agg({'EFFTOT': 'sum'}) 
    df.loc[df['RGP3']=='UNIV_PRIV','RGP3']='EPEU'
    df=df.rename(columns={'DEP_NUM_NOM':'DEP_NOM'})
    

    dict_rentree={}
    dict_annee={}
    for year in range(2001,int(datetime.now().year)):
        dict_annee[str(year)]=str(year + 1)
        if year < 2009:
            dict_rentree[str(year)]=f"{year}-0{int(str(year)[2:])+1}"
        else:
            dict_rentree[str(year)]=f"{year}-{int(str(year)[2:])+1}"
    rentree=pd.DataFrame(dict_rentree.items(), columns=['RENTREE', 'annee_universitaire'])
    annee2=pd.DataFrame(dict_annee.items(), columns=['RENTREE', 'annee'])
    NIVEAU=pd.DataFrame({"ACADEMIE":"Académie","COMMUNE":"Commune","DEPARTEMENT":"Département","PAYS":"Pays","REGION":"Région","UNITE_URBAINE":"Unité urbaine"}.items(), columns=['NIVEAU', 'niveau_geographique'])
    rgp=pd.DataFrame({"CPGE":"Classes préparatoires aux grandes écoles (CPGE)","EC_ART":"Écoles supérieures art et culture","EC_autres":"Autres écoles de spécialités diverses","EC_COM":"Écoles de commerce, gestion et comptabilité","EC_JUR":"Écoles juridiques et administratives","EC_PARAM":"Écoles paramédicales et sociales","ENS":"Écoles normales supérieures (ENS)","GE":"Grands établissements MENESR","ING_autres":"Autres formations d'ingénieurs","INP":"Instituts nationaux polytechniques (INP)","IUFM":"Instituts universitaires de formation des maîtres","STS":"Sections de techniciens supérieurs (STS) et assimilés","TOTAL":"Total des formations d'enseignement supérieur","UNIV":"Universités","EPEU":"Établissements d'enseignement universitaire privés","UT":"Universités de technologie (UT)"}.items(), columns=['RGP3', 'rgp_formations_ou_etablissements'])
    sect=pd.DataFrame({"PU":"Établissements publics","PR":"Établissements privés"}.items(), columns=['SECT', 'secteur_de_l_etablissement'])
    sexe=pd.DataFrame({"1":"Masculin","2":"Feminin"}.items(), columns=['SEXE', 'sexe_de_l_etudiant'])
    niveau=['PAYS','REGION','ACADEMIE','DEPARTEMENT','UNITE_URBAINE','COMMUNE']
    tab=['PAYS','REGIONS','ACADEMIES','DEPARTEMENTS','UNITE_URBAINES','COMMUNES']
    varid=[['PAYS_ID'],['REG_ID'],['ACA_ID'],['DEP_ID'],['UUCR_ID'],['COM_CODE']]
    varlib=['PAYS_NOM','REG_NOM','ACA_NOM','DEP_NOM','UUCR_NOM','COM_NOM']
    geolist=['','REG','REG ACA','REG ACA DEP','REG UUCR','REG ACA DEP UUCR']
    geolist2=['','reg_id','reg_id aca_id','reg_id aca_id dep_id','reg_id uucr_id','reg_id aca_id dep_id uucr_id']
    geolist3=['','reg_nom','reg_nom aca_nom','reg_nom aca_nom dep_nom','reg_nom uucr_nom','reg_nom aca_nom dep_nom uucr_nom']
    df['REG']=df.loc[:,'REG_ID']
    df['ACA']=df.loc[:,'ACA_ID']
    df['DEP']=df.loc[:,'DEP_ID']
    df['UUCR']=df.loc[:,'UUCR_ID']
    dict_a={'RENTREE':'rentree','EFFTOT':'effectif','EFFSDC':'effectifhdccpge','SEXE':'sexe','SECT':'secteur','RGP3':'regroupement','PAYS_ID':'geo_id','REG_ID':'geo_id','ACA_ID':'geo_id','DEP_ID':'geo_id','UUCR_ID':'geo_id','COM_CODE':'geo_id'}
    dict_b={'PAYS_NOM':'geo_nom','REG_NOM':'geo_nom','ACA_NOM':'geo_nom','DEP_NOM':'geo_nom','UUCR_NOM':'geo_nom','COM_NOM':'geo_nom'}
    dict_c={'EFFTOT':'effectif_dut'}
    dict_d={'EFFTOT':'effectif_ing'}
    dict_e={'EFFTOT':'effectif_form_ens'}
    dict_g={'EFF_STS_APP':'effectif_apprentis_en_sts'}
    dict_f={'ACA':'aca_id','DEP':'dep_id','UUCR':'uucr_id','REG':'reg_id'}
    df['RENTREE']=df['RENTREE'].astype('str')
    df['SEXE']=df['SEXE'].astype('str')
    communes=pd.DataFrame(CORRECTIFS_dict_esr['LES_COMMUNES']).drop_duplicates()
    communes['pays']=communes.loc[:,'REG_ID'].apply(lambda x: 'Étranger' if x=='R99' else 'France')

    for i in range(6):
        if 'EFFSDC' not in df.columns:
            df['EFFSDC']=0
        if 'EFF_STS_APP' not in df.columns:
            df['EFF_STS_APP']=0
        print(i)
        if i==0:
            t1=df.groupby(['RENTREE','RGP3','SECT','SEXE']+varid[i], as_index=False, dropna=False).agg({'EFFTOT': 'sum','EFFSDC': 'sum'}) 
            t2=df.loc[df['ING']=='ING'].groupby(['RENTREE','RGP3','SECT','SEXE']+varid[i], as_index=False, dropna=False).agg({'EFFTOT': 'sum','EFFSDC': 'sum'}) 
            t3=df.loc[df['IUT']=='IUT'].groupby(['RENTREE','RGP3','SECT','SEXE']+varid[i], as_index=False, dropna=False).agg({'EFFTOT': 'sum','EFFSDC': 'sum'}) 
            t4=df.loc[df['INSPE']=='ESPE'].groupby(['RENTREE','RGP3','SECT','SEXE']+varid[i], as_index=False, dropna=False).agg({'EFFTOT': 'sum','EFFSDC': 'sum'}) 
            t5=df.loc[df['EFF_STS_APP']!=0].groupby(['RENTREE','RGP3','SECT','SEXE']+varid[i], as_index=False, dropna=False).agg({'EFF_STS_APP':'sum'}) 
            
            t11=t1.groupby(['RENTREE','SECT','SEXE']+varid[i], as_index=False, dropna=False).agg({'EFFTOT': 'sum','EFFSDC': 'sum'}) 
            t22=t2.groupby(['RENTREE','RGP3','SECT','SEXE']+varid[i], as_index=False, dropna=False).agg({'EFFTOT': 'sum','EFFSDC': 'sum'}) 
            t33=t3.groupby(['RENTREE','SECT','SEXE']+varid[i], as_index=False, dropna=False).agg({'EFFTOT': 'sum','EFFSDC': 'sum'}) 
            t44=t4.groupby(['RENTREE','SECT','SEXE']+varid[i], as_index=False, dropna=False).agg({'EFFTOT': 'sum','EFFSDC': 'sum'}) 
            t55=t5.groupby(['RENTREE','SECT','SEXE']+varid[i], as_index=False, dropna=False).agg({'EFF_STS_APP':'sum'}) 
        else:
            t1=df.groupby(['RENTREE','RGP3','SECT','SEXE']+varid[i]+list(geolist[i].split(' ')), as_index=False, dropna=False).agg({'EFFTOT': 'sum','EFFSDC': 'sum'}) 
            t2=df.loc[df['ING']=='ING'].groupby(['RENTREE','RGP3','SECT','SEXE']+varid[i]+geolist[i].split(' '), as_index=False, dropna=False).agg({'EFFTOT': 'sum','EFFSDC': 'sum'}) 
            t3=df.loc[df['IUT']=='IUT'].groupby(['RENTREE','RGP3','SECT','SEXE']+varid[i]+geolist[i].split(' '), as_index=False, dropna=False).agg({'EFFTOT': 'sum','EFFSDC': 'sum'}) 
            t4=df.loc[df['INSPE']=='ESPE'].groupby(['RENTREE','RGP3','SECT','SEXE']+varid[i]+geolist[i].split(' '), as_index=False, dropna=False).agg({'EFFTOT': 'sum','EFFSDC': 'sum'}) 
            t5=df.loc[df['EFF_STS_APP']!=0].groupby(['RENTREE','RGP3','SECT','SEXE']+varid[i]+geolist[i].split(' '), as_index=False, dropna=False).agg({'EFF_STS_APP':'sum'}) 


            t11=t1.groupby(['RENTREE','SECT','SEXE']+varid[i]+geolist[i].split(' '), as_index=False, dropna=False).agg({'EFFTOT': 'sum','EFFSDC': 'sum'}) 
            t22=t2.groupby(['RENTREE','RGP3','SECT','SEXE']+varid[i]+geolist[i].split(' '), as_index=False, dropna=False).agg({'EFFTOT': 'sum','EFFSDC': 'sum'}) 
            t33=t3.groupby(['RENTREE','SECT','SEXE']+varid[i]+geolist[i].split(' '), as_index=False, dropna=False).agg({'EFFTOT': 'sum','EFFSDC': 'sum'}) 
            t44=t4.groupby(['RENTREE','SECT','SEXE']+varid[i]+geolist[i].split(' '), as_index=False, dropna=False).agg({'EFFTOT': 'sum','EFFSDC': 'sum'}) 
            t55=t5.groupby(['RENTREE','SECT','SEXE']+varid[i]+geolist[i].split(' '), as_index=False, dropna=False).agg({'EFF_STS_APP':'sum'}) 
        
        t111=pd.concat([t1,t11])
        t111.loc[pd.isna(t111['RGP3']),'RGP3']='TOTAL'
        t111['NIVEAU']=[niveau[i] for x in range(0,len(t111))]
        t111=pd.merge(t111,rentree,on='RENTREE',how='left')
        t111=pd.merge(t111,annee2,on='RENTREE',how='left')
        t111=pd.merge(t111,NIVEAU,on='NIVEAU',how='left')
        t111=pd.merge(t111,rgp,on='RGP3',how='left')
        t111=pd.merge(t111,sect,on='SECT',how='left')
        t111=pd.merge(t111,sexe,on='SEXE',how='left')
        t111['niveau_geo']=t111.loc[:,'NIVEAU']

        t222=pd.concat([t2,t22])
        t222.loc[pd.isna(t222['RGP3']),'RGP3']='TOTAL'

        t333=pd.concat([t3,t33])
        t333.loc[pd.isna(t333['RGP3']),'RGP3']='TOTAL'

        t444=pd.concat([t4,t44])
        t444.loc[pd.isna(t444['RGP3']),'RGP3']='TOTAL'

        t555=pd.concat([t5,t55])
        t555.loc[pd.isna(t555['RGP3']),'RGP3']='TOTAL'

        if i==0:
            A=['RENTREE','annee_universitaire','annee','niveau_geo','niveau_geographique','RGP3','rgp_formations_ou_etablissements','SECT','secteur_de_l_etablissement','SEXE','sexe_de_l_etudiant','EFFTOT','EFFSDC']+varid[i]
            df1=t111[A]
            df1['pays']=df1.loc[:,'PAYS_ID'].apply(lambda x: 'Étranger' if x=='PAYS_999' else 'France')
            df1=df1.rename(columns=dict_a)
            df1=df1.rename(columns=dict_b)
            print(df1.columns)
        else:
            A=['RENTREE','annee_universitaire','annee','niveau_geo','niveau_geographique','RGP3','rgp_formations_ou_etablissements','SECT','secteur_de_l_etablissement','SEXE','sexe_de_l_etudiant','EFFTOT','EFFSDC']+varid[i]+geolist[i].split(' ')
            T=t111[A].rename(columns=dict_a)
            C=communes[[varlib[i],varid[i][0],'pays']].rename(columns=dict_b).drop_duplicates()
            df1=pd.merge(T,C,how= 'left', left_on='geo_id', right_on=varid[i][0])
            del df1[varid[i][0]]
            print(df1.columns)
        
        df2=pd.merge(df1,t333[['EFFTOT','RGP3','SECT','SEXE',varid[i][0]]].rename(columns=dict_c).drop_duplicates(),how= 'left', left_on=['geo_id','regroupement','secteur','sexe'], right_on = [varid[i][0],'RGP3','SECT','SEXE'])
        df2=df2.drop([varid[i][0],'RGP3','SECT','SEXE'], axis=1)
        df3=pd.merge(df2,t222[['EFFTOT','RGP3','SECT','SEXE',varid[i][0]]].rename(columns=dict_d).drop_duplicates(),how= 'left', left_on=['geo_id','regroupement','secteur','sexe'], right_on = [varid[i][0],'RGP3','SECT','SEXE'])
        df3=df3.drop([varid[i][0],'RGP3','SECT','SEXE'], axis=1)
        df4=pd.merge(df3,t444[['EFFTOT','RGP3','SECT','SEXE',varid[i][0]]].rename(columns=dict_e).drop_duplicates(),how= 'left', left_on=['geo_id','regroupement','secteur','sexe'], right_on = [varid[i][0],'RGP3','SECT','SEXE'])
        df4=df4.drop([varid[i][0],'RGP3','SECT','SEXE'], axis=1)
        df5=pd.merge(df4,t555[['EFF_STS_APP','RGP3','SECT','SEXE',varid[i][0]]].rename(columns=dict_g).drop_duplicates(),how= 'left', left_on=['geo_id','regroupement','secteur','sexe'], right_on = [varid[i][0],'RGP3','SECT','SEXE'])
        df5=df5.drop([varid[i][0],'RGP3','SECT','SEXE'], axis=1)

        df5['geo_id']=df5.loc[:,'geo_id'].apply(lambda x: 'PAYS_AUTRE' if x=='PAYS_999' else x)

        df5['effectif_dut']=df5.loc[:,'effectif_dut'].apply(lambda x: 0 if pd.isna(x) else x)
        df5['effectif_ing']=df5.loc[:,'effectif_ing'].apply(lambda x: 0 if pd.isna(x) else x)
        df5['effectif_form_ens']=df5.loc[:,'effectif_form_ens'].apply(lambda x: 0 if pd.isna(x) else x)
        df5['effectif_apprentis_en_sts']=df5.loc[:,'effectif_apprentis_en_sts'].apply(lambda x: 0 if pd.isna(x) else x)


        if i==0:
            df6=df5.drop_duplicates(subset=['rentree', 'annee_universitaire', 'annee', 'niveau_geo','niveau_geographique', 'regroupement',
            'rgp_formations_ou_etablissements', 'secteur',
            'secteur_de_l_etablissement', 'sexe', 'sexe_de_l_etudiant', 'effectif',
            'effectifhdccpge','geo_id','pays'])

            df7=df6.groupby(['rentree', 'annee_universitaire', 'annee', 'niveau_geo','niveau_geographique', 'regroupement',
                'rgp_formations_ou_etablissements', 'secteur',
                'secteur_de_l_etablissement', 'sexe', 'sexe_de_l_etudiant', 'geo_id','pays'], as_index=False, dropna=False).agg({'effectif': 'sum','effectifhdccpge': 'sum','effectif_dut': 'sum','effectif_ing': 'sum','effectif_form_ens': 'sum','effectif_apprentis_en_sts':'sum'}) 
        
        else:
            l1=['rentree', 'annee_universitaire', 'annee', 'niveau_geo','niveau_geographique', 'regroupement',
            'rgp_formations_ou_etablissements', 'secteur',
            'secteur_de_l_etablissement', 'sexe', 'sexe_de_l_etudiant', 'effectif',
            'effectifhdccpge','effectif_apprentis_en_sts','geo_id', 'geo_nom']+geolist2[i].split(' ')+['pays']
            df6=df5.rename(columns=dict_f).drop_duplicates(subset=l1)

            l2=['rentree', 'annee_universitaire', 'annee', 'niveau_geo','niveau_geographique', 'regroupement',
                'rgp_formations_ou_etablissements', 'secteur',
                'secteur_de_l_etablissement', 'sexe', 'sexe_de_l_etudiant', 'geo_id', 'geo_nom']+geolist2[i].split(' ')+['pays']
            df7=df6.groupby(l2, as_index=False, dropna=False).agg({'effectif': 'sum','effectifhdccpge': 'sum','effectif_dut': 'sum','effectif_ing': 'sum','effectif_form_ens': 'sum','effectif_apprentis_en_sts':'sum'}) 

        df7['a_des_effectifs_dut']=df7.loc[:,'effectif_dut'].apply(lambda x: 'oui' if x>0 else 'non')
        df7['a_des_effectifs_ing']=df7.loc[:,'effectif_ing'].apply(lambda x: 'oui' if x>0 else 'non')
        df7['a_des_effectifs_form_ens']=df7.loc[:,'effectif_form_ens'].apply(lambda x: 'oui' if x>0 else 'non')
        df7['a_des_effectifs_apprentis_sts']=df7.loc[:,'effectif_apprentis_en_sts'].apply(lambda x: 'oui' if x>0 else 'non')

        df8=df7[df7.effectif!=0]
        if i==4:
            df8['uu']=df8['geo_id'].apply(lambda x: True if str(x)[:2]=='UU' else False)
            df8=df8[df8['uu']==True]
            del df8['uu']
        niveau[i]=df8
    df_all=pd.concat([niveau[0],niveau[1],niveau[2],niveau[3],niveau[4],niveau[5]])
    df_all.index=[x for x in range(len(df_all))]
    df_all=df_all[['rentree', 'annee_universitaire', 'annee', 'regroupement','niveau_geo','niveau_geographique',
       'rgp_formations_ou_etablissements', 'secteur',
       'secteur_de_l_etablissement', 'sexe', 'sexe_de_l_etudiant', 'geo_id',
       'effectif', 'effectifhdccpge', 'effectif_dut', 'effectif_ing',
       'effectif_form_ens', 'effectif_apprentis_en_sts', 'a_des_effectifs_dut',
       'a_des_effectifs_ing', 'a_des_effectifs_form_ens',
       'a_des_effectifs_apprentis_sts', 'geo_nom', 'pays', 'reg_id', 'aca_id',
       'dep_id', 'uucr_id']]
    return df_all