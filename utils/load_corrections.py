import json
import os
import pandas as pd

DATA_PATH=os.getcwd()

def get_all_correctifs_from_google(url,VARS,type):
    CORRECTIFS_dict= dict()
    df_c = pd.read_excel(url, sheet_name=VARS, dtype=str)
    for VAR in VARS:
        correctifs = df_c.get(VAR).to_dict(orient='records')
        for c in correctifs:
            for f in c:
                if c[f] != c[f]: # nan
                    c[f] = ''
                if 'annee' in f.lower() or 'rentree' in f.lower():
                    c[f] = str(c[f])
                if isinstance(c[f], str):
                    c[f] = c[f].replace('.0','').strip()
                elif isinstance(c[f], float) or isinstance(c[f], int):
                    c[f] = str(c[f]).replace('.0','').strip()
        CORRECTIFS_dict[f'{VAR}'] = correctifs
    json.dump(CORRECTIFS_dict, open(f'{DATA_PATH}/correctifs{type}.json', 'w'))
    
def load_all_correctifs(type):
    try:
        correctifs = json.load(open(f'{DATA_PATH}/correctifs{type}.json', 'r'))
    except:
        correctifs = {}
    for k in correctifs:    
        for ix, e in enumerate(correctifs[k]):
            for f in e.copy():
                if f.upper() != f:
                    correctifs[k][ix][f.upper()] = correctifs[k][ix][f]
                    del correctifs[k][ix][f]
    return correctifs