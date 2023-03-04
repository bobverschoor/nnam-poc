import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator

with DAG(
        "netverlies_berekenen", schedule="@daily", catchup=False, start_date=pendulum.datetime(2016, 1, 1, tz="UTC")
) as dag:
    retrieve_invoeding_prognose = EmptyOperator(task_id="retrieve_InvoedingPrognose_from_ktp")
    retrieve_transportverbruik_percentages = EmptyOperator(task_id="retrieve_TransportVerbruik_percentages")
    retrieve_netverbruik_volumes = EmptyOperator(task_id="retrieve_NetVerbruik_volume")
    retrieve_onbetaaldverbruik_volumes = EmptyOperator(task_id="retrieve_OnbetaaldVerbruik_volume")
    calc_transportverbruiknetverlies_volume = EmptyOperator(task_id="calculate_TransportverbruikNetverlies_volume")
    calc_nominatie_netverlies = EmptyOperator(task_id="calculate_NominatieNetverlies")
    store_nominatie_netverlies = EmptyOperator(task_id="store_NominatieNetverlies")

    [retrieve_invoeding_prognose,  retrieve_transportverbruik_percentages] >> calc_transportverbruiknetverlies_volume
    [calc_transportverbruiknetverlies_volume,
     retrieve_onbetaaldverbruik_volumes,
     retrieve_netverbruik_volumes] >> calc_nominatie_netverlies
    calc_nominatie_netverlies >> store_nominatie_netverlies
