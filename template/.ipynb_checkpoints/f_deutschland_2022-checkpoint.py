import pandas as pd
import geopandas as gpd

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

def parse_geometry(
    filename:str, 
    index_col:list=[0],
    crs:str = None
)-> gpd.GeoDataFrame:
    if crs == None:
        crs = "EPSG:4326"
    
    pdf = pd.read_csv(filename, index_col=index_col)

    # Remove null rows
    pdf = pdf[pdf['geometry'].notnull()]
    gs = gpd.GeoSeries.from_wkt(pdf['geometry'])
    
    gdf = gpd.GeoDataFrame(pdf, geometry=gs, crs=crs)

    for colname, coltype in gpd.io.file.infer_schema(gdf).items():
        if coltype == 'bool':
            gdf[colname] = gdf[colname].fillna(0).astype(int)

    ## ADD INFORMATION COLUMNS
    # gdf['ARS_BL'] = gdf['id'].map(dict_shortBL_id)

    return gdf
    

def parse_census(
    table_code:str,
    filename:str=None,
    logging:bool=False
)-> pd.DataFrame:
    """Parses File from Census of Germany  in a pd.DataFrame.
    
    Args: 
        table_name (int): Code of the table of the Census of Germany
            '1000A-0001': 'Personen: Bevölkerungszahl und Fläche (Gemeinden)', '15.05.2022'
            
    Returns:
        pd.DatFrame: Containing columns ['ARS', 'BEZ', 'Anzahl', 'qkm', 'Ew/qkm', 'ARS_BL', 'ARS_REG_BEZ',
       'ARS_KREIS', 'ARS_GEM_VERBAND', 'ARS_GEM', 'BL_name']
        
    """
    if filename == None:
        filename=f'{table_code}.csv'

    pdf = pd.read_csv(
        filepath_or_buffer = filename, 
        skiprows=4,
        header=0, 
        sep=';',
        dtype={'Unnamed: 1': str}
    )[:-4]

    if table_code == '1000A-0001_de':
# https://ergebnisse.zensus2022.de/datenbank/online/statistic/1000A/table/1000A-0001'
# Personen: Bevölkerungszahl und Fläche (Gemeinden)
## Bevölkerungszahl: Personen, die in einem bestimmten Gebiet (z.B. Land, Region, Stadt) leben, unabhängig davon, ob sie dort arbeiten, wohnen oder sich aufhalten. Sie berücksichtigt auch Ausländer, die in Deutschland leben, sowie Personen, die mehrere Wohnsitze haben.

        l_col_drop = ['Unnamed: 0', 'Anzahl.1', 'qkm.1', 'Ew/qkm.1']
        pdf = pdf.drop(l_col_drop, axis=1)
        pdf = pdf.rename(columns={'Unnamed: 1' : 'ARS', 'Unnamed: 2' : 'BEZ'})

        col_flaeche = 'qkm'
    
    elif table_code == '1000X-0001_de':
        # https://ergebnisse.zensus2022.de/datenbank/online/statistic/1000A/table/1000X-0001
        # Personen: Amtliche Einwohnerzahl und Fläche (Gemeinden)
        ## Einwohnerzahl: Anzahl von Personen, die in einem bestimmten Gebiet (z.B. Gemeinde, Stadt, Landkreis) ihren Hauptwohnsitz haben. Sie berücksichtigt nur diejenigen Personen, die in diesem Gebiet ihre alleinige oder Hauptwohnung haben.

        l_col_drop = ['Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7']
        pdf = pdf.drop(l_col_drop, axis=1)
        pdf = pdf.rename(columns={'Unnamed: 0' : 'ARS', 'Unnamed: 1' : 'BEZ'})
        
        l_col_name_new = []
        l_col_name_old = ['Personen', 'Fläche', 'Bevölkerungsdichte']
        for name_old in l_col_name_old:
            name_new = pdf.loc[0,name_old]
            name_new = f'{name_old} [{name_new}]'
            l_col_name_new.append(name_new)
        
        dict_col_rename = dict(zip(l_col_name_old, l_col_name_new))
        pdf = pdf.rename(columns=dict_col_rename)
        pdf.drop(index=[0], inplace=True)
        
        col_flaeche =  'Fläche [qkm]'

    else:
        print(f'Invalid code [{table_code}]')
        return null
    
    pdf[col_flaeche] = pdf[col_flaeche].str.replace(',','.')
    pdf[col_flaeche] = pd.to_numeric(pdf[col_flaeche], errors='coerce')

    pdf = add_ARS_info(pdf)
    pdf = map_BL(pdf)
    pdf = pdf.drop_duplicates()

    # Save pd df
    if logging:
        print(f'Saving file {file}')
    
    # filename_saved=f'DE_2022_{table_code}.json',
    # pdf.to_json(filename_saved, orient='records')

    return pdf


def load_zensus(
    table_code:str,
) -> pd.DataFrame:
    """" Loads data from Zensus for a given year

    Inputs:
        - table_code,str: 
            1000X-0001_de --> Personen: Amtliche Einwohnerzahl und Fläche (Gemeinden)
            1000A-0001_de --> Personen: Bevölkerungszahl und Fläche (Gemeinden)

    Returns:
        pd.DatFrame: Containing columns ['ARS', 'BEZ', 'Anzahl', 'qkm', 'Ew/qkm', 'ARS_BL', 'ARS_REG_BEZ',
       'ARS_KREIS', 'ARS_GEM_VERBAND', 'ARS_GEM', 'BL_name']
    """
    pdf = pd.read_json(f'{table_code}_clean.json')
    # pdf['ARS'] = pdf ['ARS'].astype(str)
    # pdf = pdf.astype({col: 'int32' for col in pdf.select_dtypes('int64').columns})
    return pdf

def load_geometry(
    country:str='DE',
    geom_level:str='D1',
    index_col:list=[0],
    logging:bool=False
) -> pd.DataFrame:
    
    filename = f'{country}_{geom_level}_clean.csv'
    if logging:
        print(f'Reading {filename}...')
    return pd.read_csv(filename, index_col=index_col)
    
def load_zensus_with_geom(
    table_code:str,
    year:int = 2022
) -> pd.DataFrame:
    return pd.read_json(f'DE_{year}_{table_code}_geom.json')

def gen_bund_summary(
    pdf:pd.DataFrame,
    l_groupby:list = ['ARS_BL','BL_name'],
    col_population='Anzahl',
    col_surface:str='qkm',
    col_density:str = 'ew_pro_qm',
    logging:bool=False
) -> pd.DataFrame:

    l_sum=[col_population,col_surface]
    pdf_sum = pdf.groupby(l_groupby)[l_sum].sum()
    pdf_sum[col_density] = pdf_sum[col_population]/pdf_sum[col_surface]
    pdf_sum[col_density] = pdf_sum[col_density].round(2)
    
    return pdf_sum.sort_values(by=col_density,ascending=False)
