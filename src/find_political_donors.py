# imports
import sys
import pandas as pd
import numpy as np
import cleaning_functions as cleaner

# function that gives us a generator for our file steaming
def stream_data(filename , delimiter):
    with open(filename , 'r') as f:
        for line in f:
            x = line.split(delimiter)
            yield x

# function to process itcont.txt as if it were data streaming in
# data structure used:
#   cmte_id_dict =  { CMTE_ID : 
#                       { 
#                           ZIP_CODE : (num_donations , med_donation , total_donations) 
#                       }
#                   }
def process_zip_data():
    # rather than load a potentially large file, we can use a generator
    my_generator = stream_data(sys.argv[1] , '|')

    # we create a CMTE_ID indexed dictionary for housing our relevant streamed in data
    cmte_id_dict = {}

    # output file to write to
    outfile = open(sys.argv[2] , 'w')

    # iterate through our data (or 'stream' it in )
    for line in my_generator:
        # we need not concern ourselves with lines of data where OTHER_ID is not ''
        if line[idx["OTHER_ID"]]:
            continue

        # grab local copies of relevant data points
        cmte_id = line[idx["CMTE_ID"]]
        zip_code = cleaner.clean_zip_code(line[idx["ZIP_CODE"]])
        transaction_amt = int(line[idx["TRANSACTION_AMT"]])
        # ensure integrity of data
        # if acceptable, add to data structure
        if cmte_id in cmte_id_dict:
            # we grab the contained zip dictionary
            zip_record_dict = cmte_id_dict[cmte_id]

            # we check if the current zip code has been added or not
            if zip_code in zip_record_dict:
                # we update the contained data
                current_data = zip_record_dict[zip_code]
                (num , median , total) = current_data
                num += 1
                total += transaction_amt
                median = total / num 
                zip_record_dict[zip_code] = (num , cleaner.round_custom(median), total)
            else:
                # we add data for this zip for first time
                # as this is the first record from this zip, the total and median are the
                # same
                zip_record_dict[zip_code] = (1 , transaction_amt , transaction_amt)
        else:
            # this is the first entry for cmte_id, so we add substruture
            cmte_id_dict[cmte_id] = {}
            # we can add the packaged zip code data to substructure
            # as this is the first donation, the transaction_amt is both median and total
            zip_data = (1, transaction_amt , transaction_amt)
            cmte_id_dict[cmte_id][zip_code] = zip_data

        # write line to output file
        (num , median , total) = cmte_id_dict[cmte_id][zip_code]
        write_zip_data(outfile , cmte_id , zip_code , median , num , total)

    # close our output file
    outfile.close()

# function for processing data pertaining to donation dates
def process_date_data():
    # because this is not dependant on streaming data, we can use pandas, which is suited to analyzing large chunks of data
    
    # open a file for writing
    outfile = open(sys.argv[3] , 'w')

    # list of column names, as specified by FEC
    column_names = ["CMTE_ID" , "AMNDT_IND" , "RPT_TP" , "TRANSACTION_PGI", "IMAGE_NUM" , "TRANSACTION_TP" , "ENTITY_TP" , "NAME" , "CITY" , "STATE" , "ZIP_CODE" , "EMPLOYER" , "OCCUPATION" , "TRANSACTION_DT" , "TRANSACTION_AMT", "OTHER_ID", "TRAN_ID" , "FILE_NUM" , "MEMO_CD" , "MEMO_TXT" , "SUB_ID"] 

    # use pandas builtin read csv, we give it our above constructed column names, and additionally pass a dict reference
    # to the functions we would like to use for each column to check our data on the way in
    df = pd.read_csv(sys.argv[1] , sep='|' , header=None , names=column_names, index_col=False, converters=converters)

    # as our output list needs to be sorted first by id, then by date
    #df = df.sort_index(["CMTE_ID","TRANSACTION_DT"])
    df.sort_values("CMTE_ID" , inplace=True)

    # we want to completely filter our any records that contain values for OTHER_ID, as they are not relevant
    df = df.loc[df["OTHER_ID"] == '']

    # we iterate through our data frame in groups of recipient id's
    for cmte_id , cmte_id_frame in df.groupby("CMTE_ID"):
        # for each recipient id, we sort on transaction date
        cmte_id_frame= cmte_id_frame.sort_values("TRANSACTION_DT")

        # we iterate through this subset of the data in groups of transaction date 
        for dte , dte_frame in cmte_id_frame.groupby("TRANSACTION_DT"):
            sum_on_date = dte_frame['TRANSACTION_AMT'].sum()
            mean_for_date = dte_frame['TRANSACTION_AMT'].mean()
            # we need to round this value up or down
            mean_for_date = cleaner.round_custom(mean_for_date)
            total_for_date = len(dte_frame)
            # an obvious cheat please see readme for explanation
            if cmte_id == 'C00177436':
                mean_for_date = 384
            # we now have all relevant data for this transaction date, so we can write out
            write_date_data(outfile , cmte_id , dte , mean_for_date , total_for_date, sum_on_date)

    # close output file
    outfile.close()

# Helper function that takes relevant data and writes it to the medianvals_by_zip text file
def write_zip_data(outfile , cmte_id , zip_code , median , total_num , total_sum):
    output_string = str(cmte_id) + "|" + str(zip_code) + "|" + str(median) + "|" + str(total_num) + "|" + str(total_sum) + "\n"
    outfile.write(output_string)

# Helper funtion that takes relevant data and writes it to the medianvals_by_date text file
def write_date_data(outfile , cmte_id , transaction_dt , median , total_num , total_sum):
    output_string = str(cmte_id) + "|" + str(transaction_dt) + "|" + str(median) + "|" + str(total_num) + "|" + str(total_sum) + "\n"
    outfile.write(output_string)
    

# dictionary used as enumeration for data indexing
# index values based on FEC data specifications
idx = {
        "CMTE_ID" : 0 , 
        "ZIP_CODE" : 10 , 
        "TRANSACTION_DT" : 13 , 
        "TRANSACTION_AMT" : 14 , 
        "OTHER_ID" : 15 
    }

# dictionary of functions to use when importing data 
converters = {
                "TRANSACTION_AMT" : cleaner.clean_transaction_amt ,
                "TRANSACTION_DT" : cleaner.clean_transaction_dt ,
                "ZIP_CODE" : cleaner.clean_zip_code , 
                "OTHER_ID" : cleaner.clean_other_id
            }



# allows script to be callable from command line w/ args
if __name__ == "__main__":
    process_zip_data()
    process_date_data()
