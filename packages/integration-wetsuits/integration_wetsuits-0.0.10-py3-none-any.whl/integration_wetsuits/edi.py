import requests
import clappform
import clappform.dataclasses as cldc
import pandas as pd

class Edi:

    edifact_order_header_regexes =  {
        "messagenumber": "BGM\+\d+\+([\d:]+)\+",
        "messagedate": "DTM\+137:([^:]+)",
        "buyerid":"(?<=NAD\+BY\+)([^:]+)",
        "buyerreference":"(?<=NAD\+SU\+)([^:]+)",
        "deliveryaddressID":"(?<=NAD\+DP\+)([^:]+)",
        #"deliverypartyname":"(?<=NAD\+DP\+\d{13}::\d+\+\+)[^+]+",
        "deliverypartyaddress":"NAD\+DP\+\d{13}::\d+\+\+\+[^+]+", # not working
    }

    edifact_order_lines_regexes = {
        "currency":"CUX\+2:([A-Z]{3}):",
        "lineitemnr":"LIN\+(\d+)\+\+",
        "barcode":"LIN.[a-z0-9]*\+\+([0-9]*)",
        "fedas":"PIA.[a-z0-9]*\+(\d+).GD",
        "quantity":"PIA.[a-z0-9]*\+(\d+).ST",
        "itemNr":"PIA.[a-z0-9]*\+(\d+).SA",
        "itemcolor":"(?<=IMD\+C\+35\+)\d+",
        "itemsize":"(?<=IMD\+C\+98\+).[a-z0-9]*",
        "deliverydate":"(?<=DTM\+2:)\d{8}",
        "grossprice":"(?<=PRI\+AAB:)(\d*.\d*)?",
        "netprice": "(?<=PRI\+NTP:)(\d*.\d*)?"
    }

    id=None

    def __init__(self, message):
        self.message = message

    def parser(self):
        for reg in self.edifact_order_lines_regexes.items():
            print(reg)


