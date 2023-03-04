import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator

with DAG (
    "Invoeding", schedule="@daily", catchup=False, start_date=pendulum.datetime(2016, 1, 1, tz="UTC")
) as dag:
    ingest_invoeding = EmptyOperator(task_id="ingest_invoeding_from_EDSN")
    transform_invoeding = EmptyOperator(task_id="transform_invoeding")
    store_invoeding = EmptyOperator(task_id="store_invoeding")
    send_invoeding_to_ktp = EmptyOperator(task_id="send_invoeding_to_KTP")

    ingest_invoeding >> transform_invoeding >> store_invoeding >> send_invoeding_to_ktp