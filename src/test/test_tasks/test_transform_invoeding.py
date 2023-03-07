import unittest

from dags.tasks.invoeding import transform_invoeding


class TestTransformInvoeding(unittest.TestCase):
    def test_transform(self):
        nieuwe_data = transform_invoeding(["iets met een cat"])
        self.assertEqual(["iets met een dog"], nieuwe_data.output)


if __name__ == '__main__':
    unittest.main()
