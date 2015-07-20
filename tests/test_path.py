from unittest import TestCase
import time
from buildall import Task, Path


class CreateItems(Task):
	command_call_count = 0

	def targets(self):
		return [Path('item_%d_price.txt' % i) for i in range(10)]

	def command(self):
		CreateItems.command_call_count += 1
		for file in self.targets():
			with file.open('w', encoding='UTF-8') as f:
				f.write('100')


class AddTaxToItems(Task):
	command_call_count = 0

	def inputs(self):
		return CreateItems(),

	def targets(self):
		return [Path('item_%d_tax.txt' % i) for i in range(10)]

	def command(self):
		AddTaxToItems.command_call_count += 1
		for i in range(10):
			with self.inputs()[0].targets()[i].open(encoding='UTF-8') as f:
				price = int(f.read())
			with self.targets()[i].open('w', encoding='UTF-8') as f:
				f.write('%d' % int(price * 1.3))


class ComputeSum(Task):
	command_call_count = 0

	def inputs(self):
		return AddTaxToItems(),

	def targets(self):
		return Path('total.txt'),

	def command(self):
		ComputeSum.command_call_count += 1
		sum_ = 0
		for file in self.inputs()[0].targets():
			with file.open(encoding='UTF-8') as f:
				sum_ += int(f.read())

		with self.targets()[0].open('w', encoding='UTF-8') as f:
			f.write('%d' % sum_)


class TestPipelineWithPath(TestCase):
	def setUp(self):
		CreateItems.command_call_count = 0
		AddTaxToItems.command_call_count = 0
		ComputeSum.command_call_count = 0

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
		self.assertEqual(1, CreateItems.command_call_count)
		self.assertEqual(1, AddTaxToItems.command_call_count)
		self.assertEqual(1, ComputeSum.command_call_count)

	def test_1_price_file_modified(self):
		ComputeSum().make()
		time.sleep(1)
		with open('item_5_price.txt', 'w', encoding='UTF-8') as f:
			f.write('150')
		ComputeSum().make()
		self.assertEqual(1, CreateItems.command_call_count)
		self.assertEqual(2, AddTaxToItems.command_call_count)
		self.assertEqual(2, ComputeSum.command_call_count)
		with open('total.txt', encoding='UTF-8') as f:
			self.assertEqual('1365', f.read())

	def test_1_tax_file_modified(self):
		ComputeSum().make()
		time.sleep(1)
		with open('item_5_tax.txt', 'w', encoding='UTF-8') as f:
			f.write('150')
		ComputeSum().make()
		self.assertEqual(1, CreateItems.command_call_count)
		self.assertEqual(1, AddTaxToItems.command_call_count)
		self.assertEqual(2, ComputeSum.command_call_count)
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