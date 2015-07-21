from unittest import TestCase
import time
from buildall import Task, Path

class CreateItem(Task):
    def __init__(self, num):
        self._output_path = Path('item_%d_price.txt' % num)

    def target(self):
        return self._output_path

    def build(self):
        with self._output_path.open('w', encoding='UTF-8') as f:
            f.write('100')

class AddTaxToItem(Task):
    def __init__(self, num):
        self._output_path = Path('item_%d_tax.txt' % num)

    def target(self):
        return self._output_path

    def build(self, input_path):
        with input_path.open(encoding='UTF-8') as f:
            price = int(f.read())
        with self._output_path.open('w', encoding='UTF-8') as f:
            f.write('%d' % int(price * 1.3))

class ComputeSum(Task):

    def target(self):
        return Path('total.txt')

    def build(self, *tax_files):
        sum_ = 0
        for file in tax_files:
            with file.open(encoding='UTF-8') as f:
                sum_ += int(f.read())

        with Path('total.txt').open('w', encoding='UTF-8') as f:
            f.write('%d' % sum_)

class TestPipelineWithPath(TestCase):
    def test_happy_path(self):
        compute_sum = ComputeSum() << [AddTaxToItem(i) << CreateItem(i) for i in range(10)]
        compute_sum.make()
        with open('total.txt', encoding='UTF-8') as f:
            self.assertEqual('1300', f.read())

    def tearDown(self):
        for f in Path('.').glob('*.txt'):
            f.unlink()

class DTestPipelineWithPath():
    def setUp(self):
        CreateItem.build_call_count = 0
        AddTaxToItem.build_call_count = 0
        ComputeSum.build_call_count = 0

    def tearDown(self):
        for item in range(2):
            for f in Path('.').glob('*.txt'):
                f.unlink()

    def test_happy_path(self):
        ComputeSum().make()
        with open('total.txt', encoding='UTF-8') as f:
            self.assertEqual('1300', f.read())

    def test_already_up_to_date(self):
        ComputeSum().make()
        ComputeSum().make()
        self.assertEqual(1, CreateItem.build_call_count)
        self.assertEqual(1, AddTaxToItem.build_call_count)
        self.assertEqual(1, ComputeSum.build_call_count)

    def test_1_price_file_modified(self):
        ComputeSum().make()
        time.sleep(1)
        with open('item_5_price.txt', 'w', encoding='UTF-8') as f:
            f.write('150')
        ComputeSum().make()
        self.assertEqual(1, CreateItem.build_call_count)
        self.assertEqual(2, AddTaxToItem.build_call_count)
        self.assertEqual(2, ComputeSum.build_call_count)
        with open('total.txt', encoding='UTF-8') as f:
            self.assertEqual('1365', f.read())

    def test_1_tax_file_modified(self):
        ComputeSum().make()
        time.sleep(1)
        with open('item_5_tax.txt', 'w', encoding='UTF-8') as f:
            f.write('150')
        ComputeSum().make()
        self.assertEqual(1, CreateItem.build_call_count)
        self.assertEqual(1, AddTaxToItem.build_call_count)
        self.assertEqual(2, ComputeSum.build_call_count)
        with open('total.txt', encoding='UTF-8') as f:
            self.assertEqual('1320', f.read())

    def test_mod_times(self):
        ComputeSum().make()
        file = 'item_5_price.txt'
        mod_time1 = Path(file).stat().st_mtime_ns
        time.sleep(1)
        with open(file, 'w', encoding='UTF-8') as f:
            f.write('150')
        mod_time2 = Path(file).stat().st_mtime_ns
        self.assertGreater(mod_time2, mod_time1)

