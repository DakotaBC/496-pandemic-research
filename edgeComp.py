#!/usr/bin/env python

from calendar import week
from datetime import date
from tokenize import String
from unicodedata import name
from click import confirm
import csv
from datetime import datetime

"""edgeComp.py A simple program to compile edge data into a biweekly or weekly format
Data: https://github.com/fshelobolin/C19DynamicGraph/"""

__author__ = "Dakota Badillo-Cochran"

def main():
    i = 1
    """14 for bi-weekly"""
    AVERAGE = 7
    currDate = datetime(2020, 1, 1)
    lastDate = datetime(2020, 10, 31)
    with open("./output/weeklyflightData.csv", 'w', newline='') as newFile:
        outputDoc = csv.writer(newFile)
        header = ['origin_ID', 'dest_ID', 'ID', 'Prediction', 'date']
        outputDoc.writerow(header)
        while i < 11:
            with open('./C19Graphs/'+str(i)+'.csv', 'r')as file:
                dict = csv.DictReader(file)
                days = 0
                origin_ID = ""
                dest_ID = ""
                id = ""
                prediction = 0
                date = ""
                for row in dict:
                    readDate = datetime.strptime(row['date'], "%Y-%m-%d")
                    if days == 0:
                        origin_ID = row['origin_ID']
                        dest_ID = row['dest_ID']
                        id = row['ID']
                        prediction = prediction + int(row['Prediction'])
                        date = row['date']
                        days = days + 1
                    else:
                        days = days + (readDate - currDate).days
                        currDate = readDate
                        prediction = prediction + int(row['Prediction'])
                        if (days == AVERAGE) or (currDate == lastDate):
                            days = 0
                            outputDoc.writerow([str(origin_ID), str(dest_ID), str(id), str(prediction), str(date)])
                            prediction = 0
                            if currDate == lastDate:
                                currDate = datetime(2020, 1, 1)
            i += 1

main()