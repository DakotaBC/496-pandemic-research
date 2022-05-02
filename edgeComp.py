#!/usr/bin/env python

from calendar import week
from datetime import date
from tokenize import String
from unicodedata import name
from click import confirm
import networkx as nx
import matplotlib.pyplot as plt
import csv

"""edgeComp.py A simple program to compile edge data into a biweekly or weekly format
Data: https://github.com/fshelobolin/C19DynamicGraph/"""

"""Incomplete"""

__author__ = "Dakota Badillo-Cochran"

def main():
    i = 1
    while i < 11:
        with open('./C19Graphs/'+str(i)+'.csv', 'r')as file:
            dict = csv.DictReader(file)
            for row in dict:
                
        i += 1

main()