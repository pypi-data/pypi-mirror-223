
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def ink(string, mode, index=None, mode_item=None, decimal_points=None):
    operating_modes = ['Metric', 'Warning', 'Debug']
    if mode not in operating_modes:
        raise ValueError(f"Mode should be one of {operating_modes}")
    if not index == None:
        raise NotImplemented
    if not decimal_points == None:
        raise NotImplemented
    else:
        
        if mode == None:
            print(string)

        if mode == "Metric":
            # if tpye == float
            print(f"{bcolors.OKGREEN}{bcolors.BOLD}Metric:{bcolors.ENDC} {string}{bcolors.ENDC}")
        if mode == "Warning":
            print(f"{bcolors.FAIL}{bcolors.BOLD}Warning:{bcolors.ENDC} {string}{bcolors.ENDC}")
        if mode == "Debug":
            print(f"{bcolors.WARNING}{bcolors.BOLD}Debug:{bcolors.ENDC} {string}{bcolors.ENDC}")
