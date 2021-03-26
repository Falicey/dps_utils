import argparse
from asnake.aspace import ASpace
import csv
import json


URI_INDEX = 5
KALTURA_ID_INDEX = 8


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file")
    parser.add_argument("-u", '--user')
    parser.add_argument('-pw', '--password')
    args = parser.parse_args()
    csv_file = args.csv_file
    username = args.user
    password = args.password
    aspace = ASpace(baseurl="http://as02.coalliance.org:8080",
                    username=username,
                    password=password)
    with open(csv_file, newline='') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            uri = row[URI_INDEX]
            kaltura_id = row[KALTURA_ID_INDEX]
            print(uri)
            update_as(aspace, uri, kaltura_id)


def update_as(aspace, uri, kaltura_id):
    res = aspace.client.get(uri + "\\tree")
    res_json = res.json()
    #print(json.dumps(res_json, indent=2))
    comp_uri = res_json['children'][0]['record_uri']
    #print(comp_uri)
    comp = aspace.client.get(comp_uri)
    comp_json = comp.json()
    #print(json.dumps(comp_json, indent=2))
    comp_json['component_id'] = kaltura_id
    r = aspace.client.post(comp_uri, json=comp_json)
    message = json.loads(r.text)
    #print(message)


if __name__ == '__main__':
    main()
