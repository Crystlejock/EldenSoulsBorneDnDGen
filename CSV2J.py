#!env python
#from typing import Any

import os
import jsonlines
import argparse
import csv


def parseArgs():
    parser = argparse.ArgumentParser(description='Convert CSV to JSONL')
    parser.add_argument('file', type=str, help='csv file to read')
    args = parser.parse_args()
    print("Processing CSV File: " + args.file)
    return args.file


class ConvertFile:
    def init(self):
        self.originaldata = []

    def Convert(self, inputfile):
        # open source CSV for read
        try:
            self.infile = open(inputfile, newline='')
        except BaseException as e:
            print(e)
            raise (e)  # re-throw the error to end  process, after printing exception neatly
        # open JSON-L file for writing
        try:
            self.outfile = jsonlines.Writer(open(inputfile + ".jsonl", "w"))  # original filename with new extension)
        except BaseException as e:
            print(e)
            raise (e)  # re-throw the error to end  process, after printing exception neatly

        # read a line from the CSV file
        reader = csv.DictReader(self.infile, delimiter=',', quotechar='|')

        currentLine = ""
        for row in reader:
            self.outfile.write(row)
        self.outfile.close()


filename = parseArgs()
print("Loading " + filename)
converter = ConvertFile()
print("Converting " + filename + "to JSON-L")
converter.Convert(filename)
print("Completed: " + filename + ".jsonl")