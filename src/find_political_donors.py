# imports
import sys

# function that gives us a generator for our file
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
def process_data():
    # rather than load a potentially large file, we can use a generator
    my_generator = stream_data(sys.argv[1] , '|')

    # we create a CMTE_ID indexed dictionary for housing our relevant streamed in data
    cmte_id_dict = {}

    # iterate through our data (or 'stream' it in )
    for line in my_generator:
        # grab local copies of relevant data points
        cmte_id = line[idx["CMTE_ID"]]
        zip_code = line[idx["ZIP_CODE"]]
        transaction_amt = line[idx["TRANSACTION_AMT"]]
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
                median = total / num # round here
                zip_record_dict[zip_code] = (num , total, median)
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

        # use data structure to get aggregate
            # dont forget rounding etc.
        # write line to output file


# dictionary used as enumeration for data indexing
# index values based on FEC data specifications
idx = {
        "CMTE_ID" : 0 , 
        "ZIP_CODE" : 10 , 
        "TRANSACTION_DT" : 13 , 
        "TRANSACTION_AMT" : 14 , 
        "OTHER_ID" : 15 
    }


if __name__ == "__main__":
    print(idx["ZIP_CODE"])
    #process_data()
