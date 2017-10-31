import find_political_donors as fpd
import sys

sys.argv.append("../input/itcont.txt")

df = fpd.process_date_data()
