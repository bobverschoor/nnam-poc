import os
from time import sleep

from airflow.decorators import task

os.environ["no_proxy"] = "*"


@task
def wait_for_prediction(ktp_task):
    sleep(1)


@task
def retrieve_invoedingprognose_from_ktp(prognosedata):
    return []


@task
def calculate_transportverbruiknetverlies_volume(predicted_invoeding, transportverbruik_percentages):
    return predicted_invoeding * transportverbruik_percentages


@task
def retrieve_transportverbruik_percentages():
    return 0
