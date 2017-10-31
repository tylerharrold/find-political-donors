import find_political_donors as fpd
import sys

sys.argv.append("../input/itcont.txt")
sys.argv.append("../test_zip_out.txt")
sys.argv.append("./test_date_out.txt")

df = fpd.process_date_data()
