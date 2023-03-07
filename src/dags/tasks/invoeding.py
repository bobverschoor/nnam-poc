import os
from time import sleep

import requests
from airflow.decorators import task

os.environ["no_proxy"] = "*"


@task
def retrieve_invoeding():
    catfacts = []

    while len(catfacts) <= 10:
        result = requests.get("https://catfact.ninja/fact")
        if result.status_code == requests.codes.OK:
            result = result.json()
            fact = result["fact"]
            print(fact)
            catfacts.append(fact)
        else:
            return 1

    return catfacts


@task
def transform_invoeding(invoedingsdata):
    invoeding_new = []
    for item in invoedingsdata:
        item = item.replace("cat", "dog")
        invoeding_new.append(item)
    print(invoeding_new)
    return invoeding_new


@task
def store_invoeding(invoedingsdata):
    sleep(1)


@task
def send_invoeding_to_ktp(invoedingsdata):
    sleep(1)


@task
def store_predicted_invoeding(predicted_invoedingsdata):
    sleep(1)
