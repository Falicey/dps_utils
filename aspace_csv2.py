from asnake.aspace import ASpace
import os
import re
import csv
import json
import argparse

SOUND_REGEX = r"(.wav)|(.mp3)\Z"
COMP_ID_REGEX = r"([a-zA-Z]\d+(?:\.\d+)+)"
comp_id_reg = re.compile(COMP_ID_REGEX)
CATEGORY = "MediaSpace>site>channels>University Libraries Archival Audiovisual Collection"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("search_directory")
    parser.add_argument("parent_folder_name")
    parser.add_argument("-u", '--user')
    parser.add_argument('-pw', '--password')
    args = parser.parse_args()
    search_directory = args.search_directory
    parent_folder = args.parent_folder_name
    username = args.user
    password = args.password
    aspace = ASpace(baseurl="http://as02.coalliance.org:8080",
                    username=username,
                    password=password)
    folder_list = get_file_names(search_directory)
    entries = get_as_data(folder_list, aspace, parent_folder)
    write_csv(entries)


def get_file_names(search_directory):
    sound_regex_obj = re.compile(SOUND_REGEX)
    file_list = [(sound_regex_obj.sub('', f.name), f.name) for f in os.scandir(search_directory)]
    return file_list


def get_as_data(file_list, aspace, parent_folder):
    repo = aspace.repositories(2)
    entries = list()
    num_missing = 0
    for f, f_path in file_list:
        aspace_file_name = f + ".wav"
        resource = repo.search.with_params(q="title:{}".format(aspace_file_name))
        found = False
        for r in resource:
            found = True
            j = r.json()
            #print(json.dumps(j, indent=2))
            title = j['digital_object']['_resolved']['title'].replace("\n", "").replace(",", "")
            reference_id = j['uri']
            dig_obj_type = j['digital_object']['_resolved']['digital_object_type'].replace("\n", "")
            if dig_obj_type.count("sound") > 0:
                dig_obj_type = 'sound'
            elif dig_obj_type.count("video") > 0:
                dig_obj_type = 'video'
            else:
                dig_obj_type = "image"
            archival_obj_uri = j['digital_object']['_resolved']['linked_instances'][0]['ref']
            archival_obj = aspace.client.get(archival_obj_uri).json()
            notes = archival_obj['notes']
            description = ""
            for note in notes:
                if note["type"] == "abstract":
                    description = note['content'][0].replace("\n", "").replace(",", "")
                    break
            entries.append([title, description, '', r"sftp://sftp2357732:aZIV8uf0@ftp.kaltura.com/University-Libraries/"
                            + parent_folder + "/" + f_path, dig_obj_type, reference_id, CATEGORY])
            break
        if not found:
            num_missing += 1
        print("File Name: {}{}".format(f_path, "" if found else "\t\tNOT FOUND"))
    print("{} files succesfully found. ({} failures)".format(len(entries), num_missing))
    return entries


def write_csv(entries):
    with open("kaltura_bulk_upload.csv", 'w', newline='') as csv_file:
        w = csv.writer(csv_file, delimiter=',')
        w.writerow(['* title', 'description', "tags", "url", "contentType", "referenceID", "category"])
        for entry in entries:
            w.writerow(entry)


if __name__ == '__main__':
    main()
