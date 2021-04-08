import pandas as pd
import numpy as np
from var import COL_NAME, MONTH_CONVERT

    
def get_dataframe(path):
    iter_data = pd.read_csv(path, sep=";", decimal=',', encoding="latin-1", chunksize=500)
    data= pd.concat([i for i in iter_data])
    data.columns = map(str.lower, data.columns)
    data["year_month"] = data["mois_annee_fr"].str[-4:] + data["mois_annee_fr"].str[:3].map(MONTH_CONVERT)
    data = data[COL_NAME]

    data = data[(data["rea_post_op"]==1) & (data['sexe']!='I')].dropna()
    data ['imc'] = round(data.poids / (data.taille * 10**(-2))**2,2)
    data['asa_score'] = [ i[-1]for i in data["asa"]]
    data["sexe"] = data["sexe"].replace({"M":"1", "F":"0"})
    data[["sexe", "age", "urgence", "asa_score"]] = data[["sexe", "age", "urgence", "asa_score"]].astype(int)
    
    return data
