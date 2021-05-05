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
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            try:
                uri = row[URI_INDEX]
                kaltura_id = row[KALTURA_ID_INDEX]
                update_as(aspace, uri, kaltura_id)
            except IndexError:
                print("ERROR!  It looks like the some of the fields in Kaltura are in the wrong spot.  This happens "
                      "from time to time.  Consult documentation on fix.")
                break


def update_as(aspace, uri, kaltura_id):
    comp = aspace.client.get(uri)
    comp_json = comp.json()
    #print(json.dumps(comp_json, indent=2))
    comp_json['component_id'] = kaltura_id
    r = aspace.client.post(uri, json=comp_json)
    message = json.loads(r.text)
    #print(message)
    if r.status_code == 200:
        print(uri + "\t\tSUCCESS")
    else:
        print(uri + "\t\tFAILURE")


if __name__ == '__main__':
    main()
