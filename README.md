## Topic Standard

This repository contains the original standard list of topics used for Learning Object topic browse in Clark. The "standard.txt" file included in this repository contains all of the original topic names and a list of Learning Objects for each. The Learning Objects listed in "disregard.txt" under the "REMOVE" section are disregarded in the topic identification algorithm.

The insert-standard.py script will read the "standard.txt" file and insert the data into MongoDB and Elasticsearch.

This list is not meant to be maintained overtime. It is meant to be used as a record. The script can be run if the topics in Clark need to be reset for any reason.
