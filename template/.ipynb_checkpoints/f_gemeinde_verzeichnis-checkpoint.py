import f_deutschland_2022
import pandas as pd

def parse_GV100(path_read:str, widths:list, col_names:list,
                col_BL_number: str = 'BL_nr', 
                col_BL_name:str = 'BL_name',
                path_save:str=None, is_logging:bool=False) -> pd.DataFrame:
    df = pd.read_fwf(
        filepath_or_buffer= path_read, 
        widths=widths, 
        header=None,
        names=col_names,
        dtype={'EF3_ARS': str}
    )  # Specify column widths
    
    df.replace({
        'Ã¼': 'ü',
        'Ã¶': 'ö',
        'ÃŸ': 'ß',
        'Ã¤': 'ä',
    }, inplace=True)

    col_BL_number = 'BL_nr'
    col_BL_name = 'BL_name'

    ## ADDING column 'BL_nr' and set column type to int
    df[col_BL_number] = df['EF3_ARS'].str.slice(0, 2)
    df[col_BL_number] = df[col_BL_number].astype('int')
    # df['EF4_Verband'] = df['EF4_Verband'].fillna(0).astype('int')
    
    ## ADDING column 'BL_name'
    df[col_BL_name] = df[col_BL_number].map(f_deutschland_2022.dict_id_bundeslaender)

    if is_logging:
        print(f'df.shape={df.shape}')
    
    if path_save is not None:
        df.to_csv(path_file_saved)
    
    return df
def parse_60(df:pd.DataFrame, width_60:list) -> pd.DataFrame:
    cond_satzart_60 = df['EF1_Satzart'] == 60
    
    df_60 = df[cond_satzart_60]
    # df_60.head()
    
    
    l_satz60_fields = [
        'Fläche in ha', 
        'Bevölkerung, insgesamt',
        'Bevölkerung, männlich',
        'Leer_1',#None,  # Leer
        'Neue Postleitzahl',
        'Leer_2',#None,  # Leer
        'Finanzamtsbezirk',
        'Gerichtsbarkeit',
        'Arbeitsagenturbezirk',
        'Bundestagswahlkreise',
        'Leer_3',#None   # Leer
    ]
    
    l_satz60_types = [
        'int',     # 'Fläche in ha', 
        'int',    # 'Bevölkerung, insgesamt',
        'int',    # 'Bevölkerung, männlich',
        None,  # Leer
        None,    # 'Neue Postleitzahl',
        None,  # Leer
        None,    # 'Finanzamtsbezirk',
        None,    # 'Gerichtsbarkeit',
        None,    # 'Arbeitsagenturbezirk',
        None,    # 'Bundestagswahlkreise',
        # None,  # Leer
    ]
    
    
    # df
    
    col_REGBEZ_number = 'BEZ_NR'
    df_60[col_REGBEZ_number] = df_60['EF3_ARS'].str.slice(2, 3).astype('int')
    
    col_KREIS_number = 'KREIS_NR'
    df_60[col_KREIS_number] = df_60['EF3_ARS'].str.slice(3, 5).astype('int')
    
    col_GEMEINDE_number = 'GEM_NR'
    df_60[col_GEMEINDE_number] = df_60['EF3_ARS'].str.slice(5, 8).astype('int')
    
    col_VERBANDGEMEINDE_number = 'EF4_Verband'
    df_60[col_VERBANDGEMEINDE_number] = df_60[col_VERBANDGEMEINDE_number].astype('int')
    
    dict_keyField= {
        60 : 'Markt',
        61 : 'Kreisfreie Stadt',
        62 : 'Stadtkreis',
        63 : 'Stadt',
        64 : 'Kreisangehörige Gemeinde',
        65 : 'gemeindefreies Gebiet, bewohnt',
        66 : 'gemeindefreies Gebiet, unbewohnt',
        67 : 'große Kreisstadt'
    }
    df_60['EF7_Schlüsselfelder'] = df_60['EF7_Schlüsselfelder'].astype('int')
    df_60['GEM_TYPE'] = df_60['EF7_Schlüsselfelder'].map(dict_keyField)
    
    pos_start =0
    for width,field,field_type in zip(width_60,l_satz60_fields,l_satz60_types):
        pos_end = pos_start+width#-1
        if field is not None:
            df_60[field] = df_60.EF8_Leer.str[pos_start:pos_end]
            if field_type is not None:
                df_60[field] = df_60[field].fillna(0)
                df_60[field] = df_60[field].astype(field_type)
        pos_start = pos_end#+1
    
    
    l_cols_to_int = [
        'Finanzamtsbezirk', 
        'Gerichtsbarkeit',
        'Arbeitsagenturbezirk',
        'Bundestagswahlkreise',
    ]
    
    for col in l_cols_to_int:
        df_60[col] = pd.to_numeric(df_60[col], errors='coerce')
        df_60[col] = df_60[col].fillna(0).astype('int')
    # df_60
    
    
    print(f'sum(df_60)= {df_60.shape}')
    
    # df_60.head(10)
    return df_60

def sum_de(
    df:pd.DataFrame, 
    l_by:list,
    col_BL_number: str = 'BL_nr', 
    col_BL_name:str = 'BL_name',
    col_REGBEZ_number:str = 'BEZ_NR',
    col_KREIS_number:str = 'KREIS_NR' ,
    col_VERBANDGEMEINDE_number:str = 'EF4_Verband',
    col_GEMEINDE_number:str ='GEM_NR',
    is_count_sum_added:bool=False
) -> pd.DataFrame :
    
    # l_agg = [EF1_Satzart',]
    d_agg = {
        col_BL_number : ['mean','count'],
        col_REGBEZ_number : ['mean','count'],
        col_KREIS_number : ['mean','count'],
        col_VERBANDGEMEINDE_number : ['mean','count'],
        col_GEMEINDE_number : ['mean','count'],
        'EF1_Satzart' : ['count'],
        'Fläche in ha' : ['sum','median','mean'],
        'Bevölkerung, insgesamt' : ['sum','median','mean'],
        'Bevölkerung, männlich': ['sum','median','mean'],
        'Neue Postleitzahl': ['nunique','unique'],
        'Finanzamtsbezirk': ['nunique','unique'],
        'Gerichtsbarkeit': ['nunique','unique'],
        'Arbeitsagenturbezirk': ['nunique','unique'],
        'Bundestagswahlkreise': ['nunique','unique'],
    }
    
    # dict_rename_cols = {'EF1_Satzart', 'Gemeinde'}
    df = df.groupby(l_by).agg(d_agg).round(2)
    # print(f'Rows = {df.shape}')
    # df_60_sum = df_60_sum.sort_values(by=['BL_name', 'mean'])

    if is_count_sum_added:
        totals = df.agg(['count', 'sum'])
        df = pd.concat([df, totals])
        df.index.names = [col_BL_name]
        
        #df.sort_values(by=[col_BL_name],axis=0)#,'BL_nr'])#,'mean'])

    df = df.rename(columns={
        col_BL_number: 'ADE2_LAND', 
        col_REGBEZ_number: 'ADE3_REG_BEZ', 
        col_KREIS_number: 'ADE4_KREIS',
        col_VERBANDGEMEINDE_number: 'ADE5_VERB_GEM',
        col_GEMEINDE_number: 'ADE6_GEMEINDE',
        # 'EF1_Satzart': 'Anzahl_GEMEINDE', 
    })
    return df


def add_ARS_to_pdf(
    df:pd.DataFrame,
    l_ARS_cols:list,
    # l_non_ARS_cols:list,
    l_ARS_const:str=None,
    is_first:bool=True, 
    is_logging:bool=False
) -> pd.DataFrame:


    # df['ARS'] = df['ADE2'] #+ '00000000'
    df['ARS'] = df[l_ARS_cols].agg(''.join, axis=1)

    if l_ARS_const is not None:
        df['ARS'] =df['ARS'] + l_ARS_const
    
    if is_first:
        tup_ARS = ('ARS','')    
        l_columns = list(df.columns)
        l_columns.remove(tup_ARS)
        if is_logging:
            print(l_columns)
            
        l_columns = [tup_ARS] +  l_columns
        multi_index = pd.MultiIndex.from_tuples(l_columns)
    
        if is_logging:
            print(multi_index.shape)
            
        df_reordered = df.reindex(columns=multi_index)
    return df_reordered
    
def process_sa60(
    df:pd.DataFrame,
    ADE_level:int,
    is_logging:bool=False,
    col_BL_number: str = 'BL_nr', 
    col_BL_name:str = 'BL_name',    
    col_REGBEZ_number:str = 'BEZ_NR',
    col_KREIS_number:str = 'KREIS_NR' ,
    col_VERBANDGEMEINDE_number:str = 'EF4_Verband',
    col_GEMEINDE_number:str ='GEM_NR',
    # l_group_by:list,
    # l_added_cols:list = [],
    # l_sort:list = [],
) -> pd.DataFrame:

    l_added_cols= []
    ## 1/4 GROUPBY and AGG
    ## 2/4 RENAME INDEXES and ADD ADE columns
    
    if ADE_level == 1:
        l_groupby = ['EF1_Satzart'] ## ADE=1
        l_sort = []  ## ADE=1
    elif ADE_level == 2:
        l_groupby = [col_BL_name, col_BL_number] ## ADE=2
        l_sort = ['ADE2']  ## ADE=2
    
    elif ADE_level == 3:
        l_groupby = [col_BL_name, col_BL_number,col_REGBEZ_number]  ## ADE=3
        l_sort = ['ADE2','ADE3']  ## ADE=3
    
    elif ADE_level == 4:    
        l_groupby = [col_BL_name, col_BL_number,col_REGBEZ_number,col_KREIS_number]  ## ADE=4
        l_sort = ['ADE2','ADE3','ADE4']  ## ADE=4
    
    elif ADE_level == 5:    
        l_groupby = [col_BL_name, col_BL_number,col_REGBEZ_number,col_KREIS_number, col_VERBANDGEMEINDE_number ]  ## ADE=5
        l_sort = ['ADE2','ADE3','ADE4','ADE5']  ## ADE=5
    
    elif ADE_level == 6:
        l_groupby = [col_BL_name, col_BL_number,col_REGBEZ_number,col_KREIS_number, col_VERBANDGEMEINDE_number ,col_GEMEINDE_number]  ## ADE=6
        l_added_cols = ['EF5_Verbandsbezeichnung', 'GEM_TYPE']
        l_sort = ['ADE2','ADE3','ADE4','ADE5','ADE6']  ## ADE=6

    if is_logging:
        print(f'l_groupby=[{l_groupby}]')
        
    pdf_sum_de = sum_de(
        df=df, l_by=l_groupby+l_added_cols, 
        col_BL_number= col_BL_number, 
        col_BL_name = col_BL_name,
        col_REGBEZ_number = col_REGBEZ_number,
        col_KREIS_number = col_KREIS_number ,
        col_VERBANDGEMEINDE_number = col_VERBANDGEMEINDE_number,
        col_GEMEINDE_number = col_GEMEINDE_number)
    
    if is_logging:
        print(f'pdf_sum_de.index.names={[pdf_sum_de.index.names]}')
        print(f'  length={[len(pdf_sum_de.index.names)]}')
    
    l_new_index = ['BL_name'] + l_sort + l_added_cols
    if is_logging:
        print(f'l_new_index={[l_new_index]}')
        print(f'  length={[len(l_new_index)]}')
    pdf_sum_de.index.names = l_new_index
    
    pdf_sum_de = pdf_sum_de.reset_index(drop=False)
    
    # ## 3/4 PARSE ADDED COLUMNS (ADE#)
    if not l_sort:
        num_zeros_added_to_ARS = 12
        
    if 'ADE2' in l_sort:
        pdf_sum_de['ADE2'] = pdf_sum_de['ADE2'].astype('str')
        pdf_sum_de['ADE2'] = pdf_sum_de['ADE2'].str.zfill(2)
        num_zeros_added_to_ARS = 10

    if 'ADE3' in l_sort:
        pdf_sum_de['ADE3'] = pdf_sum_de['ADE3'].astype('str')
        num_zeros_added_to_ARS = 9
        
    if 'ADE4' in l_sort:
        pdf_sum_de['ADE4'] = pdf_sum_de['ADE4'].astype('str')
        pdf_sum_de['ADE4'] = pdf_sum_de['ADE4'].str.zfill(2)
        num_zeros_added_to_ARS = 7
    
    if 'ADE5' in l_sort:
        pdf_sum_de['ADE5'] = pdf_sum_de['ADE5'].astype('str')
        pdf_sum_de['ADE5'] = pdf_sum_de['ADE5'].str.zfill(4)
        num_zeros_added_to_ARS = 3
        
    if 'ADE6' in l_sort:
        pdf_sum_de['ADE6'] = pdf_sum_de['ADE6'].astype('str')
        pdf_sum_de['ADE6'] = pdf_sum_de['ADE6'].str.zfill(3)
        num_zeros_added_to_ARS = 0

    str_to_be_add_to_ARS = '0' * num_zeros_added_to_ARS
    
    pdf_sum_ade = add_ARS_to_pdf(df= pdf_sum_de, l_ARS_cols=l_sort, l_ARS_const=str_to_be_add_to_ARS )
    
    # ## 4/4 SORT COLUMNS
    pdf_sum_ade = pdf_sum_ade.sort_values(by=l_sort).reset_index(drop=True)
    return pdf_sum_ade

def handle_col_names(df:pd.DataFrame, n_clear:int=1) -> pd.DataFrame:
    l_tups = list(df.columns[0:1+n_clear])
    l_new_tups = []
    for tup in l_tups:
        l_new_tups.append((tup[0],''))
    l_new_tups = l_new_tups + list(df.columns[n_clear+1:])
    pdf_columns = pd.MultiIndex.from_tuples(l_new_tups)
    df.columns = pdf_columns
    return df