import pandas as pd

def plz_group_agg(
    pdf: pd.DataFrame, 
    l_by: list, 
    d_agg: dict, 
    is_reset_index:bool=True,
    is_flatten_cols:bool=True
):
    
    pdf_sum = pdf.groupby(l_by).agg(d_agg)
    if is_reset_index:
        pdf_sum =pdf_sum.reset_index()#.round(2)('plz')

    # pdf_ort_sum
    
    ## Flattening column names
    if (is_flatten_cols):
        pdf_sum.columns = ['_'.join(col) for col in pdf_sum.columns.values if len(col)==2]
        
        l_cols_old_rename = [x for x in pdf_sum if x[-1] == '_']
        l_cols_new_rename = [x[:-1] for x in l_cols_old_rename]
        pdf_sum = pdf_sum.rename(columns=dict(zip(l_cols_old_rename, l_cols_new_rename)))
    
    return pdf_sum