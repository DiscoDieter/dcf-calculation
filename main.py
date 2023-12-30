import pathlib

from data_warehouse import CFCollectorandStorage
from DCFCalculator import DCFCalculator
from flow_handler import FlowHandler

path = pathlib.WindowsPath(__file__).parent.resolve()

def main():
    while True:
        CFCollectorandStorage(path).init_or_import_cf_storage()
        FlowHandler(path).control_main_flow()
        print(CFCollectorandStorage(path).cf_storage)
        dcf_calc = DCFCalculator(path, CFCollectorandStorage(path).data_to_calc)
        print(f"irr of the cashflows/investments: {dcf_calc.internal_return_rate*100:.2f} %")
        print(f'estimation of irr after tax: {dcf_calc.irr_after_tax()*100:.2f} %')

if __name__ == '__main__':
    main()