# Task: Write a script that can be run automatically each time such a quality file is generated, and look
# at how many samples from each origin fail the set quality cut-off (< 95 % covered bases of the
# reference genome or ‘FALSE’ in column 6).
# As this script should run automatically once a week, the script should also serve as a warning system,
# sending warnings if there are certain origins producing more than 10% failed samples. Therefore, you
# need to implement a system that notifies its user in some way, telling them the latest results. 

import csv
import sys
from collections import Counter

def check_qc_by_origin(input_file):

    failed_by_origin = Counter() # Creating a counter to store the number of failed samples for each origin.
    total_by_origin = Counter() # Creating a counter to store the total number of samples for each origin.

    with open(input_file, newline="") as f:
        reader = csv.DictReader(f) # Read the input CSV file so each row can be accessed using the column names.

        for row in reader:
            #print(row)
            sample = row["sample"] # get the sample name from the "sample" column
            origin = sample[1] # takes the second character of the sample name as the origin.
            #print(origin)

            total_by_origin[origin] += 1 # adds one to the total number of samples for this origin.

            # A sample fails if either QC criterion is not met
            fails_coverage = float(row["pct_covered_bases"]) < 95
            fails_qc = row["qc_pass"].upper() == "FALSE"

            if fails_coverage or fails_qc: # a sample fails if either QC criterion above is failed.
                failed_by_origin[origin] += 1 # adds one to the failed sample count for this origin.

    # Print results
    #print("Origin\tTotal\tFailed")
    results = {}

    for origin in sorted(total_by_origin):
        total = total_by_origin[origin]
        failed = failed_by_origin[origin]
        failed_percent = (failed / total) * 100

        results[origin] = { 
            "total" : total,
            "failed" : failed,
            "failed_percent": failed_percent,
            "warning": failed_percent > 10 # warning is true when more than 10% of samples failed.
        }

    return results # the function returns "results" which is a dictionary as the output.

if __name__ == "__main__": 

    input_file = sys.argv[1] # get the input file from the command line. Example: python filter_samples.py samples.csv

    results = check_qc_by_origin(input_file) # run the function, returning the "results" dictionary.

    for origin, result in results.items(): # goes through each origin and its corresponding results. origin is the key and result is the value.

        warning = " WARNING" if result["warning"] else ""
        print(
            f"{origin}: "
            f"{result['failed']}/{result['total']} failed "
            f"({result['failed_percent']:.1f}%){warning}"
        )


