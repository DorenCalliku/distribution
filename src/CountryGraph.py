import networkx as nx
import pandas as pd
import random, json
import numpy as np, numpy.random
from unidecode import unidecode

class CountryGraph:
    """
    Creates a distribution of the cities spatially based on data.
    
    To represent each city properly we need to pass them as nodes, 
    and put several factors that suggest the movement of the people
    in them.
    """
    
    
    def __init__(self, country="Turkey"):
        """
        country: the country's name, that will be read from a configuration file.
        subs:    the cities and their sub-cities which will be used for mapping back.
        G:       the graph containing the cities. 
        """
        
        self.country = country
        self.subs = {}
        self.G = nx.Graph()
        # setup
        self.__read_cities()
        # transportation
        self.__update_roads()
        #self.__update_ports()
        
    def __read_cities(self):
        """Update all the cities, and the sub-cities connected to them."""
        
        self.cities = pd.read_csv("geo_data/cities_" + self.country.lower() +".csv")
        cities_subs = pd.read_csv("geo_data/cities_" + self.country.lower() + "_subs.csv")
        for e in range(len(cities_subs)):
            self.subs[ cities_subs.iloc[e]['city']] = cities_subs.iloc[e]['admin']
        for city in list(self.cities['city']):
            city_properties = self.cities[self.cities['city'] == city].iloc[0]
            self.G.add_node(City( 
                name=city_properties['city'],
                position=(city_properties['lat'], city_properties[ 'lng']),
                area=int(city_properties['Area(km²)'].replace(',','')), 
                air=0, 
                port=0))
    
    def __update_roads(self):
        """Create the connections in the graph which represent roads."""
        
        with open("geo_data/roads_turkey") as f:
            self.roads = list(json.loads( json.load( f)).values())
        road_cities = []
        for road in self.roads:
            road = self.remove_duplicates([self.subs[i] for i in road])
            road_cities += road # add the cities which are connected to this road
            for i in range(len(road)-1):
                self.G.add_edge( road[i], road[i+1], weight=10)
        road_cities = set(road_cities)
        not_found = set( self.cities['city']) - set(road_cities)
        # order cities present in list by distance to this city
        for each in not_found:
            city = self.cities[ self.cities['city'] == each].iloc[0]
            found = self.cities[ self.cities['city'].isin( road_cities)]
            found['distance'] = ((found['lat']-city['lat'])**2 
                                 + (found['lng']-city['lng'])**2)
            closest_city = found.sort_values('distance').iloc[1]['city']
            self.G.add_edge( city['city'], closest_city, weight=10)
    
    def display_graph(self):
        pos = {city:(long, lat) 
               for (city, (lat,long)) in nx.get_node_attributes(self.G, 'position').items()}
        nx.draw(self.G, pos, with_labels=False, 
                node_size=10, node_color='r', edge_color='b')
       

    def __update_ports(self):
        with open("geo_data/ports_turkey.json") as f:
            ports = json.load(f)
        for each in ports['airport']:
            self.G.nodes[self.subs[each]]['air'] = 1
        for each in ports['port']:
            self.G.nodes[self.subs[each]]['port'] = 1
    
    @staticmethod
    def remove_duplicates(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]