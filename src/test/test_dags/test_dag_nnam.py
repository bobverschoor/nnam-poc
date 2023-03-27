import unittest
from airflow.models import DagBag


class TestNNAM_DAG(unittest.TestCase):
    def test_dag_loaded(self):
        dagbag = DagBag()
        nnam = dagbag.get_dag(dag_id="NNAM_app")
        assert dagbag.import_errors == {}
        assert nnam is not None
        assert len(nnam.tasks) == 1


if __name__ == '__main__':
    unittest.main()
