from ipywidgets import widgets
import math

class Component(object):

    def __init__(self, feature, label, comparison_type=None, update_based_on=None):
        self.feature = feature
        self.label = label
        self.comparison_type = comparison_type
        self.update_based_on = update_based_on

    def create_component(self, dataframe):
        raise NotImplementedError("The method hasn't been implemented yet.")

    def callback(self, change):
        raise NotImplementedError("The method hasn't been implemented yet.")

    def _set_callback(self):
        raise NotImplementedError("The method hasn't been implemented yet.")

    def _remove_callback(self):
        raise NotImplementedError("The method hasn't been implemented yet.")

    def reset_options(self):
        self._remove_callback()
        self._reset_options()
        self._set_callback()

    def _reset_options(self):
        raise NotImplementedError("The method hasn't been implemented yet.")

    def update_options(self, dataframe):
        self._remove_callback()
        self._update_options(dataframe)
        self._set_callback()

    def _update_options(self, dataframe):
        raise NotImplementedError("The method hasn't been implemented yet.")

    def query_string(self):
        if self.comparison_type == 'equals':
            return self._equals()
        elif self.comparison_type == 'interval':
            return self._interval()
        else:
            return None

    def _equals(self):
        raise NotImplementedError("The method hasn't been implemented yet.")
        
    def _interval(self):
        raise NotImplementedError("The method hasn't been implemented yet.")

class FeatureBoxComponent(Component):

    def __init__(self, feature, label, comparison_type='equals', update_based_on=None, any_option='Todos', empty_options=False, options_sort_key=None):
        Component.__init__(self, feature, label, comparison_type, update_based_on)
        self.component = None
        self.handler = None
        self.any_option = any_option
        self.empty_options = empty_options
        self.initial_options = None
        self.options_sort_key = options_sort_key

    def _create_options(self, dataframe):
        unique_values = dataframe[self.feature].unique()
        unique_values = sorted(unique_values, key=self.options_sort_key)
        return [self.any_option, *unique_values] 
    
    def create_component(self, dataframe):
        if not self.empty_options:
            self.initial_options = self._create_options(dataframe)
        else:
            self.initial_options = [self.any_option]

        options = self.initial_options.copy()
        self.component = widgets.Dropdown(description=self.label, value=options[0], options=options)
        self._set_callback()
    
    def callback(self, change):
        self.handler(self.feature, change)
    
    def _set_callback(self):
        self.component.observe(self.callback, names='value')
    
    def _remove_callback(self):
        self.component.unobserve(self.callback, names='value')
        
    def _set_component_options(self, options, value):
        self.component.options = options
        self.component.value = options[0]
    
    def _reset_options(self):
        options = self.initial_options.copy()
        self._set_component_options(options, options[0])
        
    def _update_options(self, dataframe):
        options = self._create_options(dataframe)
        self._set_component_options(options, options[0])
    
    def _equals(self):
        if self.component.value == self.any_option:
            return None
        return '{} == "{}"'.format(self.feature, self.component.value)

class RankSliderComponent(Component):

    def __init__(self, feature, label, slider_range=(0,15), comparison_type=None, update_based_on=None):
        Component.__init__(self, feature, label, comparison_type, update_based_on)
        self.slider_range = slider_range
        self.component = None
        self.handler = None
        
    def create_component(self, dataframe):
        self.component = widgets.IntSlider(value=0,
                                              min=self.slider_range[0],
                                              max=self.slider_range[1],
                                              step=1,
                                              description=self.label,
                                              continuous_update=True,
                                              orientation='vertical',
                                              readout=True,
                                              readout_format='d'
                                              )
        self.component.observe(self.callback, names='value')
    
    def callback(self, change):
        self.handler(self.feature, change)

class IntervalSliderComponent(Component):

    def __init__(self, feature, label, slider_range=(0,15), comparison_type='interval', update_based_on=None):
        Component.__init__(self, feature, label, comparison_type, update_based_on)
        self.slider_range = slider_range
        self.component = None
        self.handler = None
        
    def create_component(self, dataframe):
        self.component = widgets.IntRangeSlider(value=self.slider_range,
                                                min=self.slider_range[0], 
                                                max=self.slider_range[1],
                                                step=1,
                                                description=self.label,
                                                disabled=False,
                                                continuous_update=True,
                                                orientation='vertical',
                                                readout=True,
                                                readout_format='d'
                                                )
        self._set_callback()
    
    def _update_options(self, dataframe):
        try:
            min_value = math.floor(dataframe[self.feature].min())
            max_value = math.ceil(dataframe[self.feature].max())
            if min_value > self.component.max:
                self.component.max = max_value
                self.component.min = min_value
            else:
                self.component.min = min_value
                self.component.max = max_value
            
            self.component.value = (self.component.min, self.component.max)
            self.component.disabled = False
        except Exception:
            self.component.disabled = True
    
    def callback(self, change):
        self.handler(self.feature, change)

    def _set_callback(self):
        self.component.observe(self.callback, names='value')
    
    def _remove_callback(self):
        self.component.unobserve(self.callback, names='value')

    def _interval(self):
        if self.component.disabled:
            return None
        return '{} <= {} < {}'.format(self.component.value[0], self.feature, self.component.value[1])
