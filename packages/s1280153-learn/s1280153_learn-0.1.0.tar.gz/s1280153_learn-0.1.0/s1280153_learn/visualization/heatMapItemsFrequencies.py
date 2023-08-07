# visualization/heatMapItemsFrequencies.py
import plotly.express as px

class HeatMapItemsFrequencies:
    def __init__(self, items_freq_dict):
        self.items_freq_dict = items_freq_dict

    def plot_heatmap(self):
        data = {'Item': list(self.items_freq_dict.keys()), 'Frequency': list(self.items_freq_dict.values())}
        fig = px.scatter_mapbox(data, lat=[0] * len(data['Item']), lon=[0] * len(data['Item']),
                                hover_data={'Item': data['Item'], 'Frequency': data['Frequency']},
                                mapbox_style="open-street-map")
        fig.update_traces(marker=dict(size=15, color=data['Frequency'], colorscale='Viridis'), selector=dict(mode='markers'))
        fig.show()

