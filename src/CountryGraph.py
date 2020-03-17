# computational needs
import networkx as nx
import pandas as pd
# local files
import roads
# others
from unidecode import unidecode
import random, json
import numpy as np, numpy.random

class CountryGraph:
    """Creates a distribution of the cities spatially based on data."""
    
    def __init__(self, country="Turkey"):
        self.country = country
        self.G = nx.Graph()
        
    @static
    def remove_duplicates(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]
    
    def create_graph(self):
        """Use information from different sources to 
        create a map of Turkey's cities."""

        cities = pd.read_csv("cities_turkey.csv")
        
        # Put everything in a graph
        G = nx.Graph()
        # create each city
        for city in list(cities['city']):
            # find position of city in map
            city_properties = cities[cities['city'] == city].iloc[0]
            # add the city to the graph
            G.add_node( city_properties['city'], 
                       pos  = ( city_properties['lat'], city_properties[ 'lng']),
                       size = int( city_properties['population']),
                       area = int( city_properties['Area(km²)'].replace(',','')),
                       unem = int( city_properties['Unemployment']))
        # put the edges connecting the cities
        # if found city in road, but not in data, fix manually
        for road in main_roads:
            # if any of the paths is not in the list, then mention it, fix it manually
            for each in road:
                if each not in list(cities['city']):
                    print("City not found in list: ",each) # TODO: deal automatically
            # remind the cities that are present
            for i in range(len(road)-1):
                # add a connection between each two cities
                G.add_edge( road[i], road[i+1], weight=10)
        # connect the cities not in the list with the closest city in the list
        not_found = set( cities['city'])- set(sum(main_roads,[]))
        for each in not_found:
            city = cities[ cities['city'] == each].iloc[0]
            # order cities present in list by distance to this city
            found = cities[cities['city'].isin( all_cities)]
            found['distance'] = ((found['lat']-city['lat'])**2 + (found['lng']-city['lng'])**2)
            closest_city = found.sort_values('distance').iloc[1]['city'] # get the closest
            # add road connecting these cities
            G.add_edge( city['city'], closest_city, weight=10)
        return G