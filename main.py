import pathlib

from data_warehouse import CFCollectorandStorage
from DCFCalculator import DCFCalculator

path = pathlib.WindowsPath(__file__).parent.resolve()

def main():
    dwh = CFCollectorandStorage(path)
    dwh.init_or_import_cf_storage()
    dwh.add_tuple(dwh.input_cf())
    dwh.clean_duplicates()
    dwh.save_cf_storage()
    dwh.add_data_to_calc()
    print(dwh.cf_storage)
    dcf_calc = DCFCalculator(path, dwh.data_to_calc)
    print(f"irr of the cashflows/investments: {dcf_calc.internal_return_rate*100:.2f} %")
    print(f'estimation of irr after tax: {dcf_calc.irr_after_tax()*100:.2f} %')

if __name__ == '__main__':
    main()