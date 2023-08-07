#!/usr/bin/python3

# Copyright (c) 2020, 2021, 2022, 2023 Humanitarian OpenStreetMap Team
#
# This file is part of OSM-Fieldwork.
#
#     OSM-Fieldwork is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     OSM-Fieldwork is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with OSM-Fieldwork.  If not, see <https:#www.gnu.org/licenses/>.
#

import os
from osm_fieldwork.yamlfile import YamlFile
from osm_fieldwork.xlsforms import xlsforms_path
import logging
import argparse
import sys

# Instantiate logger
log = logging.getLogger(__name__)


def escape(value: str):
    """Escape characters like embedded quotes in text fields"""
    # tmp = value.replace(" ", "_")
    tmp = value.replace("&", " and ")
    return tmp.replace("'", "&apos;")


class Convert(YamlFile):
    """A class to apply a YAML config file and convert ODK to OSM"""

    def __init__(self,
                 xform: str = None
                 ):
        path = xlsforms_path.replace("xlsforms", "")
        if xform is not None:
            file = xform
        else:
            file = f"{path}/xforms.yaml"
        self.yaml = YamlFile(file)
        self.filespec = file
        # Parse the file contents into a data structure to make it
        # easier to retrieve values
        self.convert = dict()
        self.ignore = list()
        self.private = list()
        for item in self.yaml.yaml["convert"]:
            key = list(item.keys())[0]
            value = item[key]
            # print("ZZZZ: %r, %r" % (key, value))
            if type(value) is str:
                self.convert[key] = value
            elif type(value) is list:
                vals = dict()
                for entry in value:
                    if type(entry) is str:
                        # epdb.st()
                        tag = entry
                    else:
                        tag = list(entry.keys())[0]
                        vals[tag] = entry[tag]
                self.convert[key] = vals
        self.ignore = self.yaml.yaml["ignore"]
        self.private = self.yaml.yaml["private"]
        if "multiple" in  self.yaml.yaml:
            self.multiple = self.yaml.yaml["multiple"]
        else:
            self.multiple = list()

    def privateData(self,
                    keyword: str
                    ):
        """See is a keyword is in the private data category"""
        return keyword.lower() in self.private

    def convertData(self,
                    keyword: str
                    ):
        """See is a keyword is in the convert data category"""
        return keyword.lower() in self.convert

    def ignoreData(self,
                   keyword: str
                   ):
        """See is a keyword is in the convert data category"""
        return keyword.lower() in self.ignore

    def getKeyword(self,
                   value: str
                   ):
        """Get the value for a keyword from the yaml file"""
        key = self.yaml.yaml(value)
        if type(key) == bool:
            return value
        if len(key) == 0:
            key = self.yaml.getKeyword(value)
        return key

    def getValues(self,
                  tag: str = None
                  ):
        """Get the values for a primary key"""
        if tag is not None:
            if tag in self.convert:
                return self.convert[tag]
        else:
            return None

    def convertEntry(self,
                     tag: str,
                     value: str
                     ):
        """Convert a tag and value from the ODK represention to an OSM one"""
        all = list()

        # If it's not in any conversion data, pass it through unchanged.
        if tag.lower() in self.ignore:
            # logging.debug(f"FIXME: Ignoring {tag}")
            return None
        low = tag.lower()
        if (
            low not in self.convert
            and low not in self.ignore
            and low not in self.private
        ):
            return {tag: value}

        newtag = tag.lower()
        newval = value
        # If the tag is in the config file, convert it.
        if self.convertData(newtag):
            newtag = self.convertTag(newtag)
            if newtag != tag:
                logging.debug(f"Converted Tag for entry {tag} to {newtag}")

        # Truncate the elevation, as it's really long
        if newtag == "ele":
            value = value[:7]
        newval = self.convertValue(newtag, value)
        logging.debug("Converted Value for entry '%s' to '%s'" % (value, newval))
        # there can be multiple new tag/value pairs for some values from ODK
        if type(newval) == str:
            all.append({newtag: newval})
        elif type(newval) == list:
            for entry in newval:
                if type(entry) == str:
                    all.append({newtag: newval})
                elif type(entry) == dict:
                    for k, v in entry.items():
                        all.append({k: v})
        return all

    def convertValue(self,
                     tag: str,
                     value: str
                     ):
        """Convert a single tag value"""
        all = list()

        vals = self.getValues(tag)
        # There is no conversion data for this tag
        if vals is None:
            return value

        if type(vals) is dict:
            if value not in vals:
                all.append({tag: value})
                return all
            if type(vals[value]) is bool:
                entry = dict()
                if vals[value]:
                    entry[tag] = "yes"
                else:
                    entry[tag] = "no"
                all.append(entry)
                return all
            for item in vals[value].split(","):
                entry = dict()
                tmp = item.split("=")
                if len(tmp) == 1:
                    entry[tag] = vals[value]
                else:
                    entry[tmp[0]] = tmp[1]
                    logging.debug("\tValue %s converted to %s" % (value, entry))
                all.append(entry)
        return all

    def convertTag(self,
                   tag: str
                   ):
        """Convert a single tag"""
        low = tag.lower()
        if low in self.convert:
            newtag = self.convert[low]
            if type(newtag) is str:
                logging.debug("\tTag '%s' converted to '%s'" % (tag, newtag))
                tmp = newtag.split("=")
                if len(tmp) > 1:
                    newtag = tmp[0]
            elif type(newtag) is list:
                logging.error("FIXME: list()")
                # epdb.st()
                return low
            elif type(newtag) is dict:
                # logging.error("FIXME: dict()")
                return low
            return newtag.lower()
        else:
            return low

    def dump(self):
        """Dump the contents of the yaml file"""
        print("YAML file: %s" % self.filespec)
        print("Convert section")
        for key, val in self.convert.items():
            if type(val) is list:
                print("\tTag %s is" % key)
                for data in val:
                    print("\t\t%r" % data)
            else:
                print("\tTag %s is %s" % (key, val))

        print("Ignore Section")
        for item in self.ignore:
            print(f"\tIgnoring tag {item}")

#
# This script can be run standalone for debugging purposes. It's easier to debug
# this way than using pytest,
#
if __name__ == "__main__":
    # Enable logging to the terminal by default
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    root.addHandler(ch)

    parser = argparse.ArgumentParser(description="Read and parse a YAML file")
    parser.add_argument("-x", "--xform", default="xform.yaml", help="Default Yaml file")
    parser.add_argument(
        "-i",
        "--infile",
        help="The CSV input file",
    )
    args = parser.parse_args()

    # convert = Convert(args.xform)
    convert = Convert("xforms.yaml")
    print("-----")
    # tag = convert.convertTag("waterpoint_seasonal")
    # entry = convert.convertEntry("waterpoint_seasonal")
    # print("YY: %r" % entry)

    # print(convert.convertTag("tourism"))
    # entry = convert.convertEntry("tourism")
    # print(entry)
    # value = convert.convertEntry("waterpoint_seasonal")
    # print(value)
    # print("===============")

    # tag = convert.convertTag("waterpoint")
    # print(tag)
    # value = convert.convertValue("waterpoint", "well")
    # print(value)
    # value = convert.convertValue("power", "solar")

    entry = convert.convertEntry("waterpoint", "faucet")
    for i in entry:
        print("XX: %r" % i)

    entry = convert.convertEntry("operational_status", "closed")
    for i in entry:
        print("XX: %r" % i)

    entry = convert.convertEntry("seasonal", "wet")
    for i in entry:
        print("XX: %r" % i)

    entry = convert.convertEntry("seasonal", "rainy")
    for i in entry:
        print("XX: %r" % i)

    entry = convert.convertEntry("power", "solar")
    for i in entry:
        print("XX: %r" % i)
