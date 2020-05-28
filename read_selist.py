from pprint import pprint
import re
uuids = [];
append = 0;
#f = open("selist.txt", "r")
with open("selist.txt") as f:
    line = f.readline()
    while line:
        if "SE_ASSIGNMENT" in line or "status" in line:
            append = 1
            if len(uuids) != len(set(uuids)):
                pprint(line1)
                pprint(uuids)
                print "XXXX"
                break
            del uuids[:]
            line1 = line
        elif "se_uuid" in line:
            #        print line
            if append == 1:
                uuids.append(line)
        else:
            append = 0
            del uuids[:]

        line = f.readline()
