import plotly.graph_objects as go
import plotly.express as px

class Plot(object):

    def __init__(self, title, layout=None):
        self.title = title
        self.layout = layout

    def _create_plot(self, dataframe):
        raise NotImplementedError("The method hasn't been implemented yet.")

    def update_plot(self, dataframe):
        raise NotImplementedError("The method hasn't been implemented yet.")

class MapPlot(Plot):

    def __init__(self, title, lat_col, lon_col, z_col, hovertext_cols, layout=None):
        Plot.__init__(self, title, layout)
        self.lat_col = lat_col
        self.lon_col = lon_col
        self.z_col = z_col
        self.hovertext_cols = hovertext_cols

class ScatterMapPlot(MapPlot):

    def __init__(self, title, lat_col, lon_col, z_col, hovertext_cols, layout=None, colorscale='plasma'):
        MapPlot.__init__(self, title, lat_col, lon_col, z_col, hovertext_cols, layout)
        self.figure = None
        self.colorscale = colorscale

    def _create_plot(self, dataframe):
        
        plot_parameters = dict(data_frame = dataframe, 
                               lat=self.lat_col, lon=self.lon_col,
                               color_continuous_scale=self.colorscale,
                               # range_color=[0,1],
                               zoom=6, height=700,
                               title=self.title,
                               size=self.z_col,
                               color=self.z_col,
                               hover_data=self.hovertext_cols)
        
#         if self.z_col[-8:] != 'relativo':
#             print(self.z_col)
#             plot_parameters.pop('range_color')
        
        plot = px.scatter_mapbox(**plot_parameters)
        
        plot.update_layout(mapbox_style="open-street-map")
        self.figure = go.FigureWidget(plot)

    def update_plot(self, dataframe):
        
        with self.figure.batch_update():
            self.figure.data[0].lat = dataframe[self.lat_col].values
            self.figure.data[0].lon = dataframe[self.lon_col].values
            self.figure.data[0].marker.size = dataframe[self.z_col] if dataframe[self.z_col].values.size != 0 else 0
            self.figure.data[0].marker.color = dataframe[self.z_col]
            self.figure.data[0].customdata = dataframe[self.hovertext_cols].values

class DensityMapPlot(MapPlot):

    def __init__(self, title, lat_col, lon_col, z_col, hovertext_cols, layout=None):
        MapPlot.__init__(self, title, lat_col, lon_col, z_col, hovertext_cols, layout)
        self.figure = None

    def _create_plot(self, dataframe):
        mapbox = go.Densitymapbox(lat=dataframe[self.lat_col], 
                                  lon=dataframe[self.lon_col], 
                                  z=dataframe[self.z_col], radius=10,
                                  #ids=df['id'], 
                                  text=dataframe[self.hovertext_cols], hoverinfo='all'
                                  )
        
        layout = {'title': self.title,
                  'mapbox_style': 'open-street-map',
                  'height': 700,
                  'mapbox_zoom': 6,
                  'mapbox_center': {'lat': -8.435386868049687, 'lon': -36.95741641661875}
                  }
        
        self.figure = go.FigureWidget(go.Figure(mapbox, layout=layout))

    def update_plot(self, dataframe):
        with self.figure.batch_update():
            self.figure.data[0].lat = dataframe[self.lat_col].values
            self.figure.data[0].lon = dataframe[self.lon_col].values
            self.figure.data[0].z = dataframe[self.z_col].values
            self.figure.data[0].customdata = dataframe[self.hovertext_cols].values

