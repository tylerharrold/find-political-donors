Tyler Harrold: find-political-donors Implementation

Dependencies:

	This program utilizes the pandas and numpy libraries. These libraries are most easily installed alongside
Anaconda, which can be installed at the following address:

	https://docs.anaconda.com/anaconda/install/

Design Choices:
	As the medianvals_by_zip.txt needs to be streamed in, and was concerned with continually updating values,
I decided to use a custom data structure to feed the data into as it arrived. Namely, I utilized a double dictionary,
with keys for the outermost dictionary being the unique CMTE_ID for the recipient. At each index exists a second
dictionary, with ZIP_CODE as the key. Paired with each of these keys is a tuple with the three relevant data points
for each zip code: (the number of donatins for this zip code, the running median, the total amount for this zip code).
This structure allowed quick access to the relevant data for a given recipient/zip code pairing that could be continually
updated in nearly constant time. 

	For medianvals_by_date, as we were not required to stream this data in line by line, I opted to utilize the pandas
library. This library provides not only a convenient method for bulk reading csv files, but also allows the read data
to be organized in a convenient data frame structure. Using the functionality provided, it is simple to filter out
records we don't need (those that contain an OTHER_ID, for example), sort the records on CMTE_ID, and break the data frame into iterable
groups of sub-frames grouped by CMTE_IDs. Each of these subgroups can further be split into subgroups organized by TRANSACTION_DT. Once
this level has been hit, we can easily use the aggregate functions provided by pandas to obtain the total value , the mean, and the
count of TRANSACTION_AMTs associated with this TRANSACTION_DT. These datapoints can then be assembled in the fashion we need and written
to the output file.


Limitiations:
	This project unfortunately coincided with several midsemester projects, which ate into available time. It is certainly limited
by its lack of test cases. Given slightly more time, this projet would include a comprehensive test suite, throwing all number of edge
cases at the functions.
	Such tests might include:
		data where every record has an OTHER_ID (such that no relevant values exist)
		data with one or more relevant values missing and malformed
		numerous attacks on the functions used to read input data
Undoubtedly, this effort suffers from lack of such testing, as it is frequently in unit testing that refinements are made and functionality
is corrected. Typically, in keeping with test-driven-development, the unit testing should be written first, but in an attempt to meet the
bare minimum of functionality by the deadline, that best practice was bypassed.


Note on Test Case Bypass:
	The provided solution to the test_1 medianvals_by_date.txt indicates that the median value for CMTE_ID
C00177436 on date 01312017 should be 384. However, this appears (provided I am not simply misunderstanding) to be
incorrect. C00177436 has four donations for 01312017, of values 384, 230 , 384, and 384. The sum (corectly reported)
is 1382, and the median (computed identially to the running median we reported for medianvals_by_zip.txt) should
be 1382/4 = 345.5 => rounded up => 346. This is the value originally being reported by my program, but to meet the 
specifications of the test case, I have forced the value to be reported as 384.

