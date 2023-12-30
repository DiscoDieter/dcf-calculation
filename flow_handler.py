from data_warehouse import CFCollectorandStorage

class FlowHandler:

    def __init__(self, main_path):
        self._main_path = main_path

    def control_main_flow(self):
        while True:
            inp = input("Press 1 or 2: \n1. See cash flows of the past\n2. Add new cash flow and then see all cash flows\n")
            if inp == "1":
                # call visualization of past data, no data update
                CFCollectorandStorage(self._main_path).add_data_to_calc()
                break
            elif inp == "2":
                # add new cash flow and then show updated irr
                CFCollectorandStorage(self._main_path).add_tuple(CFCollectorandStorage(self._main_path).input_cf())
                CFCollectorandStorage(self._main_path).clean_duplicates()
                CFCollectorandStorage(self._main_path).sort()
                CFCollectorandStorage(self._main_path).save_cf_storage()
                CFCollectorandStorage(self._main_path).add_data_to_calc()
                break
            else:
                print("not a valid option, choose between 1 and 2")

