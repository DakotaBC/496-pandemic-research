#!/usr/bin/env python

from calendar import week
from datetime import date
from tokenize import String
from unicodedata import name
from click import confirm
import networkx as nx
import matplotlib.pyplot as plt
import csv

"""main.py A simple graphical creation and visualization of 2020 U.S. air traffic flow. Each node is a state or territory. Edges are flights. 
Data: https://github.com/fshelobolin/C19DynamicGraph/"""

__author__      = "Dakota Badillo-Cochran"


def arriveOrLeave(name, route):
    if name == route[:6]:
        return 1
    else:
        return 0

def screenData(dataPoint):
    if dataPoint == "NA":
        return "0"
    else:
        return dataPoint

def generateVisual(G):
    """draw graph"""
    nx.draw_random(G, with_labels=True, font_weight='bold')
    plt.show()

def betweennessCent(G):
    bc = nx.betweenness_centrality(G)
    with open("./output/covid_graph_betweenness_centrality.csv", 'w', newline='') as newFile:
        doc = csv.writer(newFile)
        header = ['name', 'Betweenness Centrality']
        doc.writerow(header)
        for state in bc:
            doc.writerow([state, bc[state]])

def undirectedGraph():
    Map = nx.MultiGraph()
    Map.edges.data(data=True)
    i = 1
    while i < 11:
        with open('./C19Graphs/'+str(i)+'.csv', 'r')as file:
            dict = csv.DictReader(file)
            for row in dict:
                """if find_node == false create node x2"""
                if not row['origin_ID'] in Map:
                    Map.add_node(row['origin_ID'], name=row['origin_ID'], array=[])
                if not row['dest_ID'] in Map:
                    Map.add_node(row['dest_ID'], name=row['dest_ID'], array=[])
                """create an edge between the two nodes for each flight"""
                Map.add_edge(row['origin_ID'], row['dest_ID'], weight=int(
                    row['Prediction']), date=row['date'], route=row['ID'])

        i += 1

    """Create Data Structure for Map Nodes to store daily changes, allow for changes in population"""
    i = 1
    j = 0
    while i < 6:
        with open('./C19StateData/nodes'+str(i)+'.csv', 'r')as file:
            dict = csv.DictReader(file)
            newArray = [[0 for x in range(8)] for i in range(305)]
            for row in dict:
                """Input data into data structure to store daily data"""
                """Fields: Source ID, date, pop, deaths, confirmed, recovered, active, people hospitalized, hospitalization rate"""
                newArray[j][0] = row['date']
                newArray[j][1] = row['pop']
                newArray[j][2] = row['Deaths']
                newArray[j][3] = row['Confirmed']
                newArray[j][4] = row['Recovered']
                newArray[j][5] = row['Active']
                newArray[j][6] = row['People_Hospitalized']
                newArray[j][7] = row['Hospitalization_Rate']
                j += 1
                if j == 305:
                    j = 0
                    curr = (row['country_code']+", "+row['sub_region_1'])
                    if (curr == 'US, District of Columbia'):
                        Map.nodes['US, DC']['array'] = newArray
                    else:
                        """Everyone knows that Delaware doesn't exist"""
                        if (curr != 'US, DE'):
                            Map.nodes[curr]['array'] = newArray
                        else:
                            Map.add_node('US, DE', name='US, DE', array=newArray)
                    newArray = [[0 for x in range(8)] for i in range(305)]                
        i += 1

    """Node data only: Biweekly"""
    with open("./output/covid_node_data.csv", 'w', newline='') as newFile:
        doc = csv.writer(newFile)
        header = ['name', 'week', 'population', 'deaths', 'confirmed', 'recovered', 'active', 'hospitalized', 'hospitalization rate']
        doc.writerow(header)
        for node in Map.nodes:
            i = 0
            j = 0
            deaths = 0
            confirmed = 0
            recovered = 0
            active = 0
            hospitalized = 0
            hospitalization_rate = 0
            if node[:2] == "US":
                while i < 305:
                    if i == 0:
                        pop = int(screenData(Map.nodes[node]['array'][i][1]))
                    if j == 0:
                        week = Map.nodes[node]['array'][i][0]
                    deaths += int(screenData(Map.nodes[node]['array'][i][2]))
                    confirmed += int(screenData(Map.nodes[node]['array'][i][3]))
                    recovered += int(screenData(Map.nodes[node]['array'][i][4]))
                    active += int(screenData(Map.nodes[node]['array'][i][5]))
                    hospitalized += int(screenData(Map.nodes[node]['array'][i][6]))
                    hospitalization_rate += float(screenData(Map.nodes[node]['array'][i][7]))
                    if (j == 14 or i == 304):
                        doc.writerow([str(node), str(week), str(pop), str(deaths), str(confirmed), str(recovered), str(active), str(hospitalized), str(hospitalization_rate / j)])
                        j = -1
                        deaths = 0
                        confirmed = 0
                        recovered = 0
                        active = 0
                        hospitalized = 0
                        hospitalization_rate = 0    
                    i += 1
                    j += 1
    """Produce csv file with following output data: Deaths, Hospitalization Rate, Recovered, H#, and ID 
    - daily, weekly, or biweekly optional"""

    with open("./output/covid_graph_data.csv", 'w', newline='') as newFile:
        doc = csv.writer(newFile)
        header = ['name', 'week', 'population', 'flights', 'arrived', 'departed', 'deaths', 'confirmed', 'recovered', 'active', 'hospitalized', 'hospitalization rate']
        doc.writerow(header)
        for node in Map.nodes:
            i = 0
            j = 0
            deaths = 0
            confirmed = 0
            recovered = 0
            active = 0
            hospitalized = 0
            hospitalization_rate = 0
            flights = 0
            arrived = 0
            departed = 0
            if node[:2] == "US":
                while i < 305:
                    date = Map.nodes[node]['array'][i][0]
                    if i == 0:
                        pop = Map.nodes[node]['array'][i][1]
                    deaths = Map.nodes[node]['array'][i][2]
                    confirmed = Map.nodes[node]['array'][i][3]
                    recovered = Map.nodes[node]['array'][i][4]
                    active = Map.nodes[node]['array'][i][5]
                    hospitalized = Map.nodes[node]['array'][i][6]
                    hospitalization_rate = Map.nodes[node]['array'][i][7]
                    """This isn't working, we aren't getting our edge data!"""
                    for otherNode in Map.nodes:
                        aircraft = Map.number_of_edges(node, otherNode)
                        k = 0
                        for k in range(aircraft):
                            if date == Map[node][otherNode][k]["date"]:
                                flights = flights + 1
                                """
                                if arriveOrLeave(node, edge.route):
                                    pop = pop - edge.weight
                                    departed = departed + edge.weight
                                else:
                                    pop = pop + edge.weight
                                    arrived = arrived + edge.weight
                                    """
                    pop = int(pop) - int(screenData(deaths))
                    if (j == 14 or i == 304):
                        """Data can produce NA, consult if the data should be structured in the form of NA = 0"""
                        doc.writerow([str(node), str(week), str(pop), str(flights), str(arrived), str(departed), str(deaths), str(confirmed), str(recovered), str(active), str(hospitalized), str(float(screenData(hospitalization_rate)) / j)])
                        j = -1
                        deaths = 0
                        confirmed = 0
                        recovered = 0
                        active = 0
                        hospitalized = 0
                        hospitalization_rate = 0  
                        flights = 0
                        arrived = 0
                        departed = 0
                    i += 1
                    j += 1

def directedGraph():
    G = nx.DiGraph()
    G.edges.data(data=True)

    i = 1
    while i < 11:
        with open('./C19Graphs/'+str(i)+'.csv', 'r')as file:
            dict = csv.DictReader(file)
            for row in dict:
                """if find_node == false create node x2"""
                if not row['origin_ID'] in G:
                    G.add_node(row['origin_ID'],
                                 name=row['origin_ID'], array=[])
                if not row['dest_ID'] in G:
                    G.add_node(row['dest_ID'], name=row['dest_ID'], array=[])
                """create an edge between the two nodes if one doesn't exist"""
                if G.has_edge(row['origin_ID'], row['dest_ID']):
                    G[row['origin_ID']][row['dest_ID']]['data'].append([row['Prediction'], row['date']])
                else:
                    G.add_edge(row['origin_ID'], row['dest_ID'])
                    G[row['origin_ID']][row['dest_ID']]['data'] = []
                    G[row['origin_ID']][row['dest_ID']]['data'].append([row['Prediction'], row['date']])

        i += 1
    
    i = 1
    j = 0
    """Update Nodes for new Di-Graph"""
    while i < 6:
        with open('./C19StateData/nodes'+str(i)+'.csv', 'r')as file:
            dict = csv.DictReader(file)
            newArray = [[0 for x in range(8)] for i in range(305)]
            for row in dict:
                """Input data into data structure to store daily data"""
                """Fields: Source ID, date, pop, deaths, confirmed, recovered, active, people hospitalized, hospitalization rate"""
                newArray[j][0] = row['date']
                newArray[j][1] = row['pop']
                newArray[j][2] = row['Deaths']
                newArray[j][3] = row['Confirmed']
                newArray[j][4] = row['Recovered']
                newArray[j][5] = row['Active']
                newArray[j][6] = row['People_Hospitalized']
                newArray[j][7] = row['Hospitalization_Rate']
                j += 1
                if j == 305:
                    j = 0
                    curr = (row['country_code']+", "+row['sub_region_1'])
                    if (curr == 'US, District of Columbia'):
                        G.nodes['US, DC']['array'] = newArray
                    else:
                        """This is a issue, we don't have flight data for Delaware"""
                        if (curr != 'US, DE'):
                            G.nodes[curr]['array'] = newArray
                        else:
                            G.add_node('US, DE', name='US, DE',
                                       array=newArray)
                    newArray = [[0 for x in range(8)] for i in range(305)]
        i += 1
    
    """Output Douglas Data for SVR algorithm in csv"""
    """with open("./output/covid_svr_data.csv", 'w', newline='') as newFile:
        doc = csv.writer(newFile)
        header = ['name', 'week', 'population', 'deaths', 'confirmed',
                  'recovered', 'active', 'hospitalized', 'hospitalization rate']
        for node in G.nodes:
            header.append(str(node) + ' - deaths')
            header.append(str(node) + ' - confirmed')
            header.append(str(node) + ' - recovered')
            header.append(str(node) + ' - hospitalized')
        doc.writerow(header)
        for node in G.nodes:
            i = 0
            j = 0
            deaths = 0
            confirmed = 0
            recovered = 0
            active = 0
            hospitalized = 0
            hospitalization_rate = 0
            week = 0
            if node[:2] == "US":
                while i < 305:
                    if i == 0:
                        pop = int(screenData(G.nodes[node]['array'][i][1]))
                    if j == 0:
                        week = G.nodes[node]['array'][i][0]
                        week = week + 1
                    deaths += int(screenData(G.nodes[node]['array'][i][2]))
                    confirmed += int(screenData(
                        G.nodes[node]['array'][i][3]))
                    recovered += int(screenData(
                        G.nodes[node]['array'][i][4]))
                    active += int(screenData(G.nodes[node]['array'][i][5]))
                    hospitalized += int(screenData(
                        G.nodes[node]['array'][i][6]))
                    hospitalization_rate += float(
                        screenData(G.nodes[node]['array'][i][7]))
                    if (j == 14 or i == 304):
                        doc.writerow([str(node), str(week), str(pop), str(deaths), str(confirmed), str(
                            recovered), str(active), str(hospitalized), str(hospitalization_rate / j)])
                        j = -1
                        deaths = 0
                        confirmed = 0
                        recovered = 0
                        active = 0
                        hospitalized = 0
                        hospitalization_rate = 0
                    i += 1
                    j += 1"""

    with open("./output/digraph_.csv", 'w', newline='') as newFile:
        doc = csv.writer(newFile)
        header = ['name', 'week', 'population', 'deaths', 'confirmed', 'recovered', 'active', 'flights_arrived', 'flights_departed', 'arrived', 'departed', 'hospitalized', 'hospitalization rate']
        doc.writerow(header)
        for node in G.nodes:
            i = 0
            j = 0
            deaths = 0
            confirmed = 0
            recovered = 0
            active = 0
            flights_arrived = 0
            flights_departed = 0
            passengers_arrived = 0
            passengers_departed = 0
            hospitalized = 0
            hospitalization_rate = 0

            if node[:2] == "US":
                while i < 305:
                    if i == 0:
                        pop = int(screenData(G.nodes[node]['array'][i][1]))
                    if j == 0:
                        week = G.nodes[node]['array'][i][0]
                    deaths += int(screenData(G.nodes[node]['array'][i][2]))
                    confirmed += int(screenData(G.nodes[node]['array'][i][3]))
                    recovered += int(screenData(G.nodes[node]['array'][i][4]))
                    active += int(screenData(G.nodes[node]['array'][i][5]))
                    hospitalized += int(screenData(G.nodes[node]['array'][i][6]))
                    hospitalization_rate += float(screenData(G.nodes[node]['array'][i][7]))
                    for u, v, data in G.in_edges(node, data=True):
                        for day in data['data']:
                            if day[1] == G.nodes[node]['array'][i][0]:
                                passengers_arrived = passengers_arrived + int(day[0])
                                flights_arrived = flights_arrived + 1
                    for u, v, data in G.out_edges(node, data=True):
                        for day in data['data']:
                            if day[1] == G.nodes[node]['array'][i][0]:
                                passengers_departed = passengers_departed + int(day[0])
                                flights_departed = flights_departed + 1
                    if (j == 14 or i == 304):
                        print(node+" now printing week: "+str(week))
                        doc.writerow([str(node), str(week), str(pop), str(deaths), str(confirmed), str(recovered), str(active), str(flights_arrived), str(flights_departed), str(passengers_arrived), str(passengers_departed), str(hospitalized), str(hospitalization_rate / j)])
                        j = -1
                        deaths = 0
                        confirmed = 0
                        recovered = 0
                        active = 0
                        flights_arrived = 0
                        flights_departed = 0
                        passengers_arrived = 0
                        passengers_departed = 0
                        hospitalized = 0
                        hospitalization_rate = 0    
                    i += 1
                    j += 1

def main():
    directedGraph()

main()