from ipywidgets import widgets
import pandas as pd

from dash.helpers import *

class Dashboard(object):

    def __init__(self, dataframe, mapbox):
        self.dataframe = dataframe
        self.mapbox = mapbox
        self.boxes = []
        self.rank_slider = None
        self.output = None
        self.range_slider = None
    
    def add_box(self, box):
        self.boxes.append(box)

    def update(self, col, change):
        conditions = []
        for box in self.boxes:
            if box.update_based_on == col:
                box.update_options(self.dataframe[self.dataframe[col] == change.new])

            if box.query_string() != None:
                conditions.append(box.query_string())
        
        if self.range_slider:
            if self.range_slider.update_based_on == col:
                self.range_slider.update_options(self.dataframe[self.dataframe[col] == change.new])
            
            if self.range_slider.query_string() != None:
                conditions.append(self.range_slider.query_string())

        try:
            query_template = (len(conditions)-1)*'{} & ' + '{}'
            query_string = query_template.format(*conditions)
            temp_df = self.dataframe.query(query_string)
            
            # Contar num de acidentes nos trechos de acordo com a base filtrada
            update_acidentes_trecho(temp_df)
            
            # Contar num de mortes nos trechos de acordo com a base filtrada
            update_mortes_trecho(temp_df)
            
            # Atualizando fracoes de acidentes/mortos relativos ao valor maximo
            update_relativo(temp_df, "acidentes_trecho")
            update_relativo(temp_df, "mortos_trecho")
            
        except:
            temp_df = self.dataframe
            
        temp_df = temp_df.drop_duplicates(subset='trecho', keep='first')
        
        if self.rank_slider:
            rank = self.rank_slider.component.value
            if rank != 0:
                temp_df = temp_df.sort_values(by=self.mapbox.z_col, axis=0, ascending=False).head(rank)
                self.output.clear_output(wait=True)
                with self.output:
                    display(temp_df[self.mapbox.hovertext_cols]
                            .sort_values( rank_order(self.mapbox.z_col) , ascending = False)
                            .iloc[:, ::-1]
                            .set_index(pd.Index(list(map(lambda x : x + 1 ,
                                                         range(len(temp_df[self.mapbox.hovertext_cols])))))))

            else:
                self.output.clear_output(wait=False)

        self.mapbox.update_plot(temp_df)
        
    def _set_up(self):
        self.mapbox._create_plot(self.dataframe.drop_duplicates(subset='trecho', keep='first'))

        self.output = widgets.Output(layout={'border': '1px solid black'})

        for box in self.boxes:
            box.create_component(self.dataframe)
            box.handler = self.update
        
        c1 = widgets.HBox(children=[box.component for box in self.boxes])
        
        
        if (self.rank_slider != None) & (self.range_slider != None):
            self.rank_slider.create_component(None)
            self.rank_slider.handler = self.update
            
            self.range_slider.create_component(None)
            self.range_slider.handler = self.update
            self.range_slider.component.disabled = True

            c2 = widgets.VBox(children=[c1, self.mapbox.figure, self.output])
            c3 = widgets.VBox(children=[self.rank_slider.component, self.range_slider.component])
            c4 = widgets.HBox(children=[c3, c2])
            return c4
        
        c2 = widgets.VBox(children=[c1, self.mapbox.figure])
        return widgets.HBox(children=[self.output, c2])

    def dash(self):
        return self._set_up()
