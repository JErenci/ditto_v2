import pandas as pd

# class MyClass:
dict_id_bundeslaender = {
    1:  'Schleswig-Holstein',
    2:  'Hamburg',
    3:  'Niedersachsen',
    4:  'Bremen',
    5:  'Nordrhein-Westfalen',
    6:  'Hessen',
    7:  'Rheinland-Pfalz',
    8:  'Baden-Württemberg',
    9:  'Bayern',
    10: 'Saarland',
    11: 'Berlin',
    12: 'Brandenburg',	
    13: 'Mecklenburg-Vorpommern',
    14: 'Sachsen',
    15: 'Sachsen-Anhalt',
    16: 'Thüringen'
}

dict_bundeslaender_id = {
    'Schleswig-Holstein': 1,
    'Hamburg': 2,
    'Niedersachsen': 3,
    'Bremen': 4,
    'Nordrhein-Westfalen': 5,
    'Hessen': 6,
    'Rheinland-Pfalz': 7,
    'Baden-Württemberg': 8,
    'Bayern': 9,
    'Saarland': 10,
    'Berlin': 11,
    'Brandenburg': 12,
    'Mecklenburg-Vorpommern': 13,
    'Sachsen': 14,
    'Sachsen-Anhalt': 15,
    'Thüringen': 16
}

dict_short_long_bundeslaender = {
    'DE-SH': 'Schleswig-Holstein',
    'DE-HH': 'Hamburg',
    'DE-NI': 'Niedersachsen',
    'DE-HB': 'Bremen',
    'DE-NW': 'Nordrhein-Westfalen',
    'DE-HE': 'Hessen',
    'DE-RP': 'Rheinland-Pfalz',
    'DE-BW': 'Baden-Württemberg',
    'DE-BY': 'Bayern',
    'DE-SL': 'Saarland',
    'DE-BE': 'Berlin',
    'DE-BB': 'Brandenburg',	
    'DE-MV': 'Mecklenburg-Vorpommern',
    'DE-SN': 'Sachsen',
    'DE-ST': 'Sachsen-Anhalt',
    'DE-TH': 'Thüringen'
}

dict_shortBL_id = {
    'DE-SH':  1,
    'DE-HH':  2,
    'DE-NI':  3,
    'DE-HB':  4,
    'DE-NW':  5,
    'DE-HE':  6,
    'DE-RP':  7,
    'DE-BW':  8,
    'DE-BY':  9,
    'DE-SL': 10,
    'DE-BE': 11,
    'DE-BB': 12,	
    'DE-MV': 13,
    'DE-SN': 14,
    'DE-ST': 15,
    'DE-TH': 16
}

def map_BL(pdf:pd.DataFrame, col_BL='ARS_BL') -> pd.DataFrame:
    """
    maps the Bundesland in the column 'col_BL' of 'pdf'
    """
    pdf['BL_name'] = pdf[col_BL].map(dict_id_bundeslaender)
    return pdf

def add_ARS_info(
    pdf:pd.DataFrame, 
    ars_column:str = 'ARS'
) -> pd.DataFrame:
    """ Adds the 'ARS' (Amtlicher Regionalschlüssel) in a column of 'pdf'
    ### Amtlicher Regionalschlüssel 
    Der Amtliche Regionalschlüssel (ARS) ist ein 12-stelliger Schlüssel des Statistischen Bundesamtes, der Gemeinden in Deutschland eindeutig identifiziert. Er besteht aus fünf Bestandteilen:

    2 Stellen für das Bundesland
    1 Stelle für den Regierungsbezirk
    2 Stellen für den Kreis
    4 Stellen für den Gemeindeverband
    3 Stellen für die Gemeinde
    
    """
    
    pdf['ARS_str'] = pdf[ars_column].astype(str)#[0:2]
    
    pdf['ARS_BL'] = pdf['ARS_str'].str[:2].astype(int)   #2
    pdf['ARS_REG_BEZ'] = pdf['ARS_str'].str[2:3].astype(int) #1
    pdf['ARS_KREIS'] = pdf['ARS_str'].str[3:5].astype(int) #2
    pdf['ARS_GEM_VERBAND'] = pdf['ARS_str'].str[5:9].astype(int) #4
    pdf['ARS_GEM'] = pdf['ARS_str'].str[9:12].astype(int) #3
    del pdf['ARS_str']
    return pdf

def parse_and_save_zensus_2022(
    filename_loaded:str='1000X-0001_de.csv',
    filename_saved: str='DE_2022.json',
    logging:bool=False
)-> pd.DataFrame:
    """Parses File from Census of Germany in 2022 in a pd.DataFrame.
    
    Args: 
        filename (str): Name of the file with the Census of Germany
            'filename' : '1000X-0001_de.csv',
            'name' : 'Personen: Amtliche Einwohnerzahl und Fläche (Gemeinden)',
            'code' : '1000X-0001',
            'date' : '09.05.2011
    Returns:
        pd.DatFrame: Containing columns [Anzahl,qkm,Ew/qkm]
        
    """

    pdf = pd.read_csv(
        filepath_or_buffer = filename_loaded, 
        header=0, 
        sep=';',
        dtype={'ARS': str, 'BEZ': str, 'Anzahl': int, 
              'e1': str, 'qkm' : str, 'e2':str, 'Ew/qkm':int, 'e3':str}
    )
    
    l_cols_to_delete = ['e1','e2','e3']
    pdf = pdf.drop(columns=l_cols_to_delete)
    
    pdf['qkm'] = pdf['qkm'].str.replace(',','.')
    pdf['qkm'] = pd.to_numeric(pdf['qkm'], errors='coerce')

    pdf = add_ARS_info(pdf)
    pdf = map_BL(pdf)
    pdf = pdf.drop_duplicates()

    # Save pd df
    if logging:
        print(f'Saving file {file}')
    # pdf.to_json(filename_saved, orient='records')
    
    return pdf

def load_zensus_2022(filename:str='DE_2022.json') -> pd.DataFrame:
    return pd.read_json(filename)

def load_zensus_2022_with_geom(filename:str='DE_2022_geom.json') -> pd.DataFrame:
    return pd.read_json(filename)

def gen_bund_summary(
    pdf:pd.DataFrame,
    l_groupby:list = ['ARS_BL','BL_name'],
    col_population='Anzahl',
    col_surface='qkm',
    col_density:str = 'ew_pro_qm',
    logging:bool=False
) -> pd.DataFrame:

    l_sum=[col_population,col_surface]
    pdf_sum = pdf.groupby(l_groupby)[l_sum].sum()
    pdf_sum[col_density] = pdf_sum[col_population]/pdf_sum[col_surface]
    
    return pdf_sum.sort_values(by='ew_pro_qm',ascending=False)
