import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
from tqdm import tqdm
import sys

def padding_for_year(df, v_year=2019, days_to_pad=366):
    
    map_weekday = {0:'segunda',1:'terca',2:'quarta',3:'quinta',4:'sexta',5:'sabado',6:'domingo'}

    df.sort_values(by='data')
    periodos = df.periodo.unique()
    data_min = dt.datetime(v_year,1,1)

    df_year_padded = pd.DataFrame(columns=df.columns)

    zero_padding_dict = {}
    for c in df.columns:
        zero_padding_dict[c] = [0]

    zero_padding_dict['ano'] = [v_year]

    dfy = df[(df.ano == v_year)]

    for br_selected in tqdm(dfy.br.unique()):
        
        zero_padding_dict['br'] = br_selected
        dfb = dfy[(dfy.br==br_selected)]

        for kmb in tqdm(dfb.km_bins.unique()):

            zero_padding_dict['km_bins'] = [kmb]
            zero_padding_dict['tracado_via'] = [dfb[(dfb.km_bins == kmb)].tracado_via.mode().values[0]]
            zero_padding_dict['tipo_pista'] = [dfb[(dfb.km_bins == kmb)].tipo_pista.mode().values[0]]
            zero_padding_dict['tracado_via'] = [dfb[(dfb.km_bins == kmb)].tracado_via.mode().values[0]]
            zero_padding_dict['uso_solo'] = [dfb[(dfb.km_bins == kmb)].uso_solo.mode().values[0]]
            
            data = data_min
            for day in range(1, days_to_pad):
                zero_padding_dict['data'] = data
                month = data.month
                dia = data.day

                dfmd = dfb[(dfb.month_number == month) & (dfb.dia == dia)]

                try:
                    last_meteo = dfmd.condicao_meteorologica.mode().values[0]
                except:
                    last_meteo = 'ignorada'

                zero_padding_dict['month_number'] = [month]
                zero_padding_dict['dia'] = [dia]
                zero_padding_dict['dia_semana'] = map_weekday[data.weekday()]

                try:
                    zero_padding_dict['feriado'] = dfmd.feriado.mode().values[0]
                except:
                    zero_padding_dict['feriado'] = 'not-feriado'

                for p in periodos:
                    df_to_append = dfmd[(dfmd.km_bins == kmb) & (dfmd.periodo == p)].copy()

                    if len(df_to_append) == 1:
                        df_year_padded = df_year_padded.append(df_to_append, ignore_index=True)
                        last_meteo = df_to_append.condicao_meteorologica.values[0]
                    
                    elif len(df_to_append) > 1:
                        to_sum_cols = ['mortos', 'feridos_leves', 'feridos_graves','ilesos', 'ignorados', 'feridos', 'veiculos']
                        all_other_cols = list(set(dfmd.columns) - set(to_sum_cols))

                        dict_to_append_squished = {}

                        for sc in to_sum_cols:
                            dict_to_append_squished[sc] = [df_to_append[sc].sum()]

                        for aoc in all_other_cols:
                            dict_to_append_squished[aoc] = [df_to_append[aoc].mode().values[0]]

                        df_year_padded = df_year_padded.append(pd.DataFrame.from_dict(dict_to_append_squished), ignore_index=True)

                    else:                       
                        zero_padding_dict['periodo'] = [p]
                        zero_padding_dict['condicao_meteorologica'] = [last_meteo]
                        df_year_padded = df_year_padded.append(pd.DataFrame.from_dict(zero_padding_dict), ignore_index=True)
                
                data = data_min + dt.timedelta(days=day)
                
    return df_year_padded

if __name__ == "__main__":

    df = pd.read_csv('data/partial_pedataset.csv')

    clima_replace = {
        'sol': 'tempo_claro',
        'céu_claro': 'tempo_claro',
        'ignorado': 'ignorado',
        'chuva': 'tempo_adverso',
        'nublado': 'tempo_adverso',
        'nevoeiro_neblina': 'tempo_adverso'
    }

    for d in clima_replace:
        df.condicao_meteorologica.replace(to_replace=d,
                                        value=clima_replace[d],
                                        inplace=True)

    df.drop(['mes'], axis=1, inplace=True)
    df['dia'] = [int(str(d)[8:10]) for d in pd.to_datetime(df['timestamp'])]
    df['data'] = pd.to_datetime(df.timestamp, yearfirst=True, errors='ignore')
    df.drop([
        'timestamp', 'municipio', 'tipo_acidente', 'classificacao_acidente', 'fase_dia',
        'sentido_via', 'pessoas', 'label','causa_acidente','uf'],axis=1, inplace=True)

    df = df[((df['br']==104) | (df['br']==232) & (df['km']>=102)& (df['km']<=213))]

    df_year = df[df.ano==int(sys.argv[1])]

    print(df_year.head())

    df_year_new = padding_for_year(df_year, v_year=int(sys.argv[1]), days_to_pad=int(sys.argv[2]))

    df_year_new.to_excel('df_'+str(sys.argv[1])[-2:]+'_pad_'+str(sys.argv[2])+'.xlsx',index=None)