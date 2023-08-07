# Import required libraries
import plotly.express as px

class heatMapItemsFrequencies:
    def __init__(self, data):
        self.data = data

    def plot_heatmap(self):
        # Extract data for plotting
        points = list(self.data.keys())
        frequencies = list(self.data.values())

        # Create a DataFrame for the HeatMap
        df = {'Points': points, 'Frequencies': frequencies}

        # Plot the HeatMap
        fig = px.density_mapbox(df, lat=0, lon=0, z='Frequencies',
                                radius=20, center=dict(lat=0, lon=0),
                                zoom=0, mapbox_style='open-street-map',
                                labels={'Frequencies': 'Frequency'})

        # Show the HeatMap
        fig.show()
