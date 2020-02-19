# Funções Helper para update dos DataFrames


# Para atualizar o número de acidentes nos trechos filtrados
def update_acidentes_trecho(df):
    df.loc[:, "acidentes_trecho"] = df["trecho"].replace( dict(df["trecho"].value_counts()) )
    
    
# Para atualizar o número de mortes nos trechos filtrados
def update_mortes_trecho(df):
    dicionario = {trecho:df[df["trecho"] == trecho]["mortos_original"].sum() for trecho in df["trecho"].unique()}
    
    df.loc[:, "mortos_trecho"] = df["trecho"].replace(dicionario)

    
def update_relativo(df, col):
    col_relativo = col[:-7] + "_relativo"
    
    df.loc[:, col_relativo] = (df[col]/df[col].max()) if (df[col].max() != 0) else 0
    
    
def rank_order(col):
    
    mortos_acidentes = ['mortos_trecho', 'acidentes_trecho']
    
    dicionario = {'mortos_trecho': mortos_acidentes,
                  'acidentes_trecho': mortos_acidentes[::-1],
                  'mortos_relativo': mortos_acidentes, 
                  'acidentes_relativo': mortos_acidentes[::-1]}
    
    return dicionario[col]
    

    
    
# def update_mortes_trecho(df):
    
#     helperdf = df[["trecho", "mortos_original"]].copy()
    
#     mortos_update = helperdf.groupby("trecho").sum()
    
#     df["mortos_trecho"] = helperdf.merge(mortos_update, 
#                                          on = "trecho", 
#                                          suffixes= ('', '__trecho_update')
#                                         )["mortos_original__trecho_update"].fillna(value= 0)    
