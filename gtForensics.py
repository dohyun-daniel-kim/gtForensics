
import sys
import argparse
import logging
import time
from modules.utils.takeout_case import Case
from modules.preprocessor.takeout_data_parser import DataParser

# from modules.scanner.takeout_input_info_extractor import InputDataInfo


logger = logging.getLogger('gtForensics')

# ANDROID_DEVICE_CONFIGURATION_SERVICE_PATH = 'Take' + os.sep + 'Android Device Configuration Service'

def main(args):
    logging.basicConfig(format = '[%(asctime)s] [%(levelname)s] %(message)s', stream = sys.stdout)
    logger.setLevel(logging.DEBUG if args.v else logging.INFO)
    
    logger.info('Start...')
    t1 = time.perf_counter()
    start_time = time.ctime()

    logger.info('[1/3] Scanning...')
    case = Case(args)
    case.set_file_path()
    case.create_analysis_db()

    # InputDataInfo.find_takeout_file_path(case)
    logger.info('[2/3] Pre-processing...')
    DataParser.parse_takeout_data(case)



    # print("device paht.. ", case.takeout_android_device_configuration_service_path)

    # case.find_takeout_file_path()
    # AndroidDeviceConfigurationService.parse_device_info(case)
    logger.info('[3/3] Analyzing...')

    logger.info('End...')
    end_time = time.ctime()
    t2 = time.perf_counter()
    logger.info('elapsed time : %0.2f min (%0.2f sec)' %  ((t2-t1)/60, t2-t1))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'gtForensics - Google Takeout Forensic Tool \nsimple usage example: python3 andForensics.py -i <INPUT_DIR> -o <OUTPUT_DIR> -proc <NUMBER OF PROCESS FOR MULTIPROCESSING>', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', action = "store", dest = "input_dir",
                            help = "Input directory containing the Android image file with EXT4 file system. \nIt can have multiple image files.")
    parser.add_argument('-o', action = "store", dest = "output_dir",
                            help = "Output directory to store analysis result files.")
    parser.add_argument('-p', action = "store", dest = "phase",
                            help = "Select a single investigation phase. (default: all phases) \n - [1/3] Scanning: \"scan\"\n - [2/3] Pre-processing: \"preproc\" (only after \"Scanning\" phase) \n - [3/3] Analyzing: \"analysis\" (only after \"Pre-processing\" phase) \n e.g., andForensics.py -i <INPUT_DIR> -o <OUTPUT_DIR> -p preproc")
    parser.add_argument('-d', action = "store", dest = "decompile_apk", default = 0,
                            help = "Select whether to decompile the APK file. This operation is time-consuming and requires a large capacity. \n(1:enable, 0:disable, default:disable)")
    parser.add_argument('-proc', action = "store", dest = "number_process",
                            help = "Input the number of processes for multiprocessing. (default: single processing)")
    parser.add_argument('-v', action = "store_true",
                            help = "Show verbose (debug) output.")
    args = parser.parse_args()

    print('''

    ________________________________________________________________________________________

            888    8888888888                                         d8b                   
            888    888                                                Y8P                   
            888    888                                                                      
    .d88b.  888888 8888888  .d88b.  888d888 .d88b.  88888b.  .d8888b  888  .d8888b .d8888b  
    d88P"88b 888    888     d88""88b 888P"  d8P  Y8b 888 "88b 88K      888 d88P"    88K     
    888  888 888    888     888  888 888    88888888 888  888 "Y8888b. 888 888      "Y8888b.
    Y88b 888 Y88b.  888     Y88..88P 888    Y8b.     888  888      X88 888 Y88b.         X88
    "Y88888  "Y888 888      "Y88P"  888     "Y8888  888  888  88888P' 888  "Y8888P  88888P' 
        888                                                                                 
    Y8b d88P                                                                                
    "Y88P"                                                                                  

    ___________________________________________________ Google Takeout Forensic Tool _______


    ''')
    if (args.input_dir == None) | (args.output_dir == None):
    	parser.print_help()
    	exit(0)
    # if (args.phase != None) & ((args.phase != "scan") & (args.phase != "preproc") & (args.phase != "analysis")):
    #     parser.print_help()
    #     exit(0)

main(args)