import unittest

import dags.tasks.invoeding


class TestTransformInvoeding(unittest.TestCase):

    def test_transform(self):
        transform_invoeding = dags.tasks.invoeding.transform_invoeding
        nieuwe_data = transform_invoeding.function(["iets met een cat"])
        self.assertEqual(["iets met een dog"], nieuwe_data)


if __name__ == '__main__':
    unittest.main()
