import ssl
import elasticsearch
import os
import time

from pymongo import MongoClient
from elasticsearch import helpers
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.environ.get('MONGO_DOMAIN'), ssl_cert_reqs=ssl.CERT_NONE)

def start():
    file = open("standard.txt", "r")

    topics = []

    current_topic = ''

    for line in file:

        # Sleep for one second before each iteration to
        # avoid AWS Elasticsearch service rate limiting
        time.sleep(1)

        # Check for an empty line
        if not len(line.strip()) == 0:
        
            if "TOPIC" in line:
                # Remove new line characters from the line containing the topic name
                line = line.replace('\n', '')

                # Take the text after the "TOPIC" label and use it as the topic name
                topic_name = line.split(':')[1]

                # Remove leading and trailing white space from the topic name
                topic_name = topic_name.strip()

                # We know that the text file does not list any topic more than once
                # So we don't check for duplicates here
                topics.append(topic_name)

                # We encountered a new topic. All Learning Objects names encountered will
                # be assigned to the current topic
                current_topic = topic_name

            # If the line is not empty and it does not include
            # the word "TOPIC", then it must be a Learning Object name
            else:

                learning_object_name = line

                # Leaning Object names maked with ||| are duplucicates
                # Their unique _ids follow the |||
                if "|||" in learning_object_name:
                    learning_object_id = learning_object_name.split(" ||| ")[1]
                else:
                    learning_object_id = get_learning_object_id(learning_object_name)

                es_insert(learning_object_id, current_topic)

    # When the iteration is complete,
    # save all of the topic names into MongoDB
    mongo_insert(topics)


def get_learning_object_id(learning_object_name):

    learning_objects_collection = client.onion.objects

    result = list(learning_objects_collection.find({ 'name':  learning_object_name.strip(), 'status': 'released' }))
    
    return result[0].get('_id')


def es_insert(learning_object_id, topic_name):
    es = elasticsearch.Elasticsearch()

    query_body = {
        "query": {
            "match": {
                "id": learning_object_id
            }
        }
    }
    doc = es.search(index="learning-objects", body=query_body)
    res = es.update(index="learning-objects", doc_type="_doc", id=doc['hits']['hits'][0]['_id'], body={ 'doc': { 'topic': topic_name }})
                

def mongo_insert(topics):

    topics_collection = client.onion.topics

    topics_collection.insert_one({ 'topics': topics })


if __name__ == '__main__':
    start()