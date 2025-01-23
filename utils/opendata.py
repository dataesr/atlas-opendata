def opendata_atlas(df,annee):
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
    df.loc[df['RENTREE'].isin(["2023","2022","2021","2020","2019","2018","2017","2016","2015","2014","2013","2012","2011","2010","2009","2008","2007"]),'ETABLI2']=df.loc[df['RENTREE'].isin(["2023","2022","2021","2020","2019","2018","2017","2016","2015","2014","2013","2012","2011","2010","2009","2008","2007"]),'ETABLI']=df.loc[df['RENTREE'].isin(["2022","2021","2020","2019","2018","2017","2016","2015","2014","2013","2012","2011","2010","2009","2008","2007"]),'ETABLI2']
    
    if annee in ["2014","2013","2012","2011","2010","2009","2008","2007"]:
        df=df[['RENTREE','PAYS_ID','REG_ID','ACA_ID','DEP_ID','UUCR_ID','COM_CODE2','COM_CODE','ETABLI','RGP3','FORMAT','SECT','INSPE','IUT','IUT2','ING','TOTAL','LMDDONT','DISCIPLI','CURSUS_LMD','UNIV','STS_ASS','DUT','SEXE','UUCR_NOM','DEP_NUM_NOM','ACA_NOM','REG_NOM','EFFTOT']]
    elif annee in ["2023","2022","2021","2020","2019","2018","2015","2016","2017"]:
        df=df[['RENTREE','PAYS_ID','REG_ID','ACA_ID','DEP_ID','UUCR_ID','COM_CODE2','COM_CODE','ETABLI','RGP3','FORMAT','SECT','INSPE','IUT','IUT2','ING','TOTAL','LMDDONT','DISCIPLI','CURSUS_LMD','UNIV','STS_ASS','DUT','SEXE','UUCR_NOM','DEP_NUM_NOM','ACA_NOM','REG_NOM','EFFTOT','EFFSDC', 'EFF_STS_APP',]]
    elif annee in ["2006","2005","2004","2003","2002","2001"]:
        df=df[['RENTREE','PAYS_ID','REG_ID','ACA_ID','DEP_ID','UUCR_ID','COM_CODE2','COM_CODE','ETABLI','RGP3','FORMAT','SECT','INSPE','IUT','IUT2','ING','TOTAL','UNIV','STS_ASS','DUT','SEXE','UUCR_NOM','DEP_NUM_NOM','ACA_NOM','REG_NOM','EFFTOT']]
    
    if annee in ["2014","2013","2012","2011","2010","2009","2008","2007"]:
        df=df.groupby(['RENTREE','PAYS_ID','REG_ID','ACA_ID','DEP_ID','UUCR_ID','COM_CODE2','COM_CODE','ETABLI','RGP3','FORMAT','SECT','INSPE','IUT','IUT2','ING','TOTAL','LMDDONT','DISCIPLI','CURSUS_LMD','UNIV','STS_ASS','DUT','SEXE','UUCR_NOM','DEP_NUM_NOM','ACA_NOM','REG_NOM'], as_index=False, dropna=False).agg({'EFFTOT': 'sum'}) 
    elif annee in ["2023","2022","2021","2020","2019","2018","2015","2016","2017"]:
        df=df.groupby(['RENTREE','PAYS_ID','REG_ID','ACA_ID','DEP_ID','UUCR_ID','COM_CODE2','COM_CODE','ETABLI','RGP3','FORMAT','SECT','INSPE','IUT','IUT2','ING','TOTAL','LMDDONT','DISCIPLI','CURSUS_LMD','UNIV','STS_ASS','DUT','SEXE','UUCR_NOM','DEP_NUM_NOM','ACA_NOM','REG_NOM'], as_index=False, dropna=False).agg({'EFFTOT': 'sum','EFFSDC': 'sum', 'EFF_STS_APP':'sum'}) 
    elif annee in ["2006","2005","2004","2003","2002","2001"]:
        df=df.groupby(['RENTREE','PAYS_ID','REG_ID','ACA_ID','DEP_ID','UUCR_ID','COM_CODE2','COM_CODE','ETABLI','RGP3','FORMAT','SECT','INSPE','IUT','IUT2','ING','TOTAL','UNIV','STS_ASS','DUT','SEXE','UUCR_NOM','DEP_NUM_NOM','ACA_NOM','REG_NOM'], as_index=False, dropna=False).agg({'EFFTOT': 'sum'}) 
    df.loc[df['RGP3']=='UNIV_PRIV','RGP3']='EPEU'
    df=df.rename(columns={'DEP_NUM_NOM':'DEP_NOM'})
    return df