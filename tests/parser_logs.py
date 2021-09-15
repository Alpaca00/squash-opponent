import argparse
from collections import defaultdict
import re
import json


parser = argparse.ArgumentParser(description="Process access.log")
parser.add_argument("-f", dest="file", action="store", help="Path to logfile")
parser.add_argument(
    "-c",
    dest="choice",
    action="store_true",
    help="Parser for methods or browser. If param choice true: methods, else browser",
)
args = parser.parse_args()

dict_for_methods = defaultdict(
    lambda: {"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0, "HEAD": 0}
)
dict_for_browser = {}


def reader(log):
    with open(args.file) as file:
        for index, line in enumerate(file.readlines()):
            ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line).group()
            if args.choice:
                method = re.search(r"\] \"(POST|GET|PUT|DELETE|HEAD)", line).groups()[0]
                dict_for_methods[ip][method] += 1
            else:
                browser = re.search(
                    r"(Opera|Chrome|Safari|Firefox|Android|HeadlessChrome|Mobile Safari)",
                    line,
                )
                dict_for_browser[ip] = browser

            if index > 50:
                break
        if not args.choice:
            dict_f = {}
            for k, v in dict_for_browser.items():
                dict_f[k] = v.group()
            write_json(dict_f)
        else:
            return write_json(dict_for_methods)


def write_json(dict_f):
    with open("access_logs.json", "a+") as json_file:
        json.dump(dict_f, json_file, sort_keys=True)


if __name__ == "__main__":
    reader(args.file)
