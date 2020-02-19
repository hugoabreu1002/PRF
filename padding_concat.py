import pandas as pd
import sys

if __name__ == "__main__":

    df_19_pad = pd.read_excel('df_19_pad.xlsx')
    df_18_pad = pd.read_excel('df_18_pad.xlsx')
    df_17_pad = pd.read_excel('df_17_pad.xlsx')
    df_16_pad = pd.read_excel('df_16_pad.xlsx')

    df_19_18_17_16_pad = df_19_pad.copy()
    df_19_18_17_16_pad = df_19_18_17_16_pad.append(df_18_pad)
    df_19_18_17_16_pad.reset_index(inplace=True)
    df_19_18_17_16_pad = df_19_18_17_16_pad.append(df_17_pad)
    df_19_18_17_16_pad = df_19_18_17_16_pad.append(df_16_pad)

    df_19_18_17_16_pad.to_excel('df_19_18_17_16_pad.xlsx',index=None)
    df_19_18_17_16_pad.to_csv('df_19_18_17_16_pad.csv',index=None)