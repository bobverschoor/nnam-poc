import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup

from dags.tasks.invoeding import *
from dags.tasks.netverlies import *


def collect_invoeding():
    with TaskGroup(group_id="Verzamelen_Invoedingsdata", tooltip="Verzamelen van Invoedingsdata uit EDSN") as invoeding:
        invoedingsdata = transform_invoeding(retrieve_invoeding())
        invoeding_stored = store_invoeding(invoedingsdata)
        invoeding_to_ktp = send_invoeding_to_ktp(invoedingsdata)
    return invoeding_to_ktp


with DAG(
        "NNAM_app", schedule="@daily", catchup=False, start_date=pendulum.datetime(2023, 1, 1, tz="UTC")
) as dag:

    invoeding = collect_invoeding()

    wait_prediction = wait_for_prediction(invoeding)

    with TaskGroup(group_id="Berekenen_Nominatie_Allocatie_Netverlies",
                   tooltip="Berekenen van de nominatie op basis van geprognostiseerde invoedingsdata en waardes van "
                           "inkoop") as calculation_loss:

        predicted_invoedingsdata = retrieve_invoedingprognose_from_ktp(wait_prediction)
        transportverbruik_percentages = retrieve_transportverbruik_percentages()
        retrieve_netverbruik_volumes = EmptyOperator(task_id="retrieve_NetVerbruik_volume")
        retrieve_onbetaaldverbruik_volumes = EmptyOperator(task_id="retrieve_OnbetaaldVerbruik_volume")
        calc_nominatie_netverlies = EmptyOperator(task_id="calculate_Nominatie_Netverlies")
        calc_allocatie_netverlies = EmptyOperator(task_id="calculate_Allocatie_Netverlies")
        store_nominatie_netverlies = EmptyOperator(task_id="store_Nominatie_Netverlies")
        store_allocatie_netverlies = EmptyOperator(task_id="store_Allocatie_Netverlies")

        store_predicted_invoeding(predicted_invoedingsdata)

        calc_transportverbruiknetverlies_volume = \
            calculate_transportverbruiknetverlies_volume(predicted_invoedingsdata, transportverbruik_percentages)

        [calc_transportverbruiknetverlies_volume,
            retrieve_onbetaaldverbruik_volumes,
            retrieve_netverbruik_volumes] >> calc_nominatie_netverlies
        calc_nominatie_netverlies >> store_nominatie_netverlies
        calc_allocatie_netverlies >> store_allocatie_netverlies

    with TaskGroup(group_id="Publicatie_Allocatie_Nominatie_Netverlies",
                   tooltip="Publiceren van de netverlies nominatie naar de BRP en de netverlies allocatie naar CARM") \
            as publish_netverlies:

        publish_allocatie_netverlies = EmptyOperator(task_id="Publicatie_Allocatie_netverlies")
        publish_nominatie_netverlies = EmptyOperator(task_id="Publicatie_Nominatie_netverlies")
        store_publications = EmptyOperator(task_id="Store_publications")
        [publish_allocatie_netverlies, publish_nominatie_netverlies] >> store_publications
        calc_nominatie_netverlies >> publish_allocatie_netverlies
        calc_nominatie_netverlies >> publish_nominatie_netverlies

