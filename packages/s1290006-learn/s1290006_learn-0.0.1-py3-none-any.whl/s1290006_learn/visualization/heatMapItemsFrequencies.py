import pandas as pd
import plotly.express as px

class heatMapItemsFrequencies():
    def heatMapItemsFrequencies(self, countse):
        df = pd.DataFrame()
        df['Location'] = countse.index.to_list()
        df['Location'] = df['Location'].astype('str')
        df['count'] = countse.to_list()
    
        tmp = df['Location'].str.strip("'Point()'").str.split(' ', expand=True)
        df['lon'] = tmp[0]
        df['lat'] = tmp[1].str.strip(")',")
        print(df)
    
        fig = px.scatter_mapbox(
        # set deta_frame and latitude and longitude
        data_frame=df,
        lon="lon",
        lat="lat",
        
        # set marker
        size_max=100,
        opacity=0.4,
        
        color="count",
        size="count",
    
        # set figure
        center={'lat':34.686567, 'lon':135.52000},
        zoom=4,
        height=600,
        width=800)
        fig.update_layout(mapbox_style='open-street-map')
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.show()