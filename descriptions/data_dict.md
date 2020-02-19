# Info

## Datasets

> The data groups information about accident occurences in Brazilian roads from 2007 to 2019. Every year is provided as a separate dataset. Begining in the year 2017 new columns reporting geocoordinates and operational information have been added.

## Data dictionary

> - **id**:
int, identifies the accidents.

> - **data_inversa**: string, accident date.

> - **dia_semana**: string, day of the week.

> - **horario**: string, accident time. In the 24hr format hh:mm:ss.

> - **uf**: string, state.

> - **br**: int, road identification.

> - **km**: float, road KM on which the accident took place.

> - **municipio**: string, city name.

> - **causa_acidente**: string, presumable cause of accident.

> - **tipo_acidente**: string, type of accident.

> - **classificacao_acidente**: string, rating of accident gravity based if casualities or injured were reported. Can assume 4 values 'Sem Vítimas', 'Com Vítimas Feridas', 'Com Vítimas Fatais' or 'Ignorado'. 'Ignorado' is used for occurences in which victims states weren't reported.

> - **fase_dia**: string, stage of the day the accident occured. Can assume the values: 'Pleno dia', 'Plena noite', 'Amanhecer' or 'Anoitecer'.

> - **sentido_via**: string, way of the road considering the collision point. Can be 'Crescente' or 'Decrescente'.

> - **condicao_metereologica**: string, description of wheater condition at the time of accident.

> - **tipo_pista**: string, road type based on the number of lanes. Can assume the values: 'Dupla', 'Simples' or 'Múltipla'.

> - **tracado_via**: string, description of road layout.

> - **uso_solo**: string, description of the local of the accident.

> - **ano**: int, year the accident occured. This column is present untill 2015.

> - **pessoas**: int, number of people involved in the accident.

> - **mortos**: int, number of casualties.

> - **feridos_leves**: int, number of slightly injured.

> - **feridos_graves**: int, number of seriously injured.

> - **ilesos**: int, number of uninjured people.

> - **ignorados**: int, number of involved people which health states weren't reported.

> - **feridos**: int, total number of injured people. Sum of 'feridos_leves' and 'feridos_graves'.

> - **veiculos**: int, number of vehicles involved in the accident.

### Features added to 2017 dataset onwards

> - **latitude**: float, latitude coordinate.

> - **longitude**: float, longitude coordinate.

> - **regional/delegacia/uop**: string, PRF operational information.

## Missing values

> - Missing values appear in the form of a **'(null)'** string in the raw datasets.

## Issues

> - **id**: Values are unique in the same year and can repeat between different years.

> - **data_inversa**: Variable name suggests it comes in a year first format, however the format is not consistent across years. It can appear in year first or day first formats and use '/' or '-' as separators.

> - **dia_semana**: Names are capitalized till 2016. From 2017 onwards names aren't capitalized and the suffix '-feira' is added.

> - **km**: Starting 2016 a comma is used as decimal point.

> - **classificacao_acidente**: Missing values which can be infered from some numeric columns.

> - **condicao_metereologica**: Column name typo.

> - **uso_solo**: Till 2016 can assume values 'Urbano' or 'Rural'. From 2017 onwards: 'Sim' for 'Urbano' or 'Não' for 'Rural'.

> - **ano**: This column is dropped after 2015.

> - **pessoas**: Some rows have inconsistent values for this column.

> - **latitude/longitude**: Present in datasets starting in 2017. In 2019 values have a comma for decimal point.

> - **string columns**: Minor differences in values occur due to whitespaces, capitalization or typos

---
