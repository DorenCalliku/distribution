import networkx as nx
import pandas as pd
import random, json
import numpy as np, numpy.random
from unidecode import unidecode

class CountryGraph:
    """Creates a distribution of the cities spatially based on data."""
    
    def __init__(self, country="Turkey"):
        self.country = country
        self.G = nx.Graph()
        self.subs = {}
        self.__update_cities()
        self.__update_subs()
        self.__update_roads()
        self.__create_graph()
        
    @staticmethod
    def remove_duplicates(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]
    
    def __update_cities(self):
        self.cities = pd.read_csv("geo_data/cities_"+ self.country.lower() +".csv")
        
    def __update_roads(self):
        with open("geo_data/roads_turkey") as f:
            self.roads = list(json.loads( json.load( f)).values())
        
    def __update_subs(self):
        # get the cities where the main roads pass from in turkey
        cities_subs = pd.read_csv('geo_data/cities_subs.csv')
        for e in range(len( cities_subs)):
            self.subs[ cities_subs.iloc[e]['city'] ] = cities_subs.iloc[e]['admin']  
        
    def __create_graph(self):
        """Update the graph of the country."""

        for city in list(self.cities['city']):
            city_properties = self.cities[self.cities['city'] == city].iloc[0]
            self.G.add_node( city_properties['city'], 
                       pos  = ( city_properties['lat'], city_properties[ 'lng']),
                       size = int( city_properties['population']),
                       area = int( city_properties['Area(km²)'].replace(',','')),
                       unem = int( city_properties['Unemployment']))
        road_cities = []
        for road in self.roads:
            road = self.remove_duplicates([self.subs[i] for i in road])
            road_cities += road # add the cities which are connected to this road
            for i in range(len(road)-1):
                self.G.add_edge( road[i], road[i+1], weight=10)
        road_cities = set(road_cities)
        not_found = set( self.cities['city']) - set(road_cities)
        for each in not_found:
            city = self.cities[ self.cities['city'] == each].iloc[0]
            # order cities present in list by distance to this city
            found = self.cities[ self.cities['city'].isin( road_cities)]
            found['distance'] = ((found['lat']-city['lat'])**2 + (found['lng']-city['lng'])**2)
            try:
                closest_city = found.sort_values('distance').iloc[1]['city'] # get the closest
                # add road connecting these cities
                self.G.add_edge( city['city'], closest_city, weight=10)
            except:
                found.sort_values('distance')
                
    def display_graph(self):
        pos = {city:(long, lat) for (city, (lat,long)) in nx.get_node_attributes(self.G, 'pos').items()}
        nx.draw(self.G, pos, with_labels=False, node_size=10, node_color='r', edge_color='b')