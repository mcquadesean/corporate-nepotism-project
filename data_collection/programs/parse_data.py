############################################################
# This script parses company filings for keywords indicating 
# familial ties. It writes the results to a .txt file along with
# company name, date of filing, and CIK identifier
#
# Sean McQuade
# May 2023
###########################################################



import os
surrounding_chars = 200
outfile = open(".../parsed_data.txt", 'w')
outfile.write("Date|Company Conformed Name|CIK|Keyword with sentence\n")
queries = ["stepson", "stepdaughter","step-son-in-law", "son-in-law", "son", "sons", "stepfather", "step-father", "step-fatherin-law", "father-in-law", "father", "stepmother", "step-mother", "step-mother-in-law", "mother-in-law","mother", "sister-in-law", "sister", "stepdaughter", "step-daughter", "step-daughter-in-law","daughter-in-law", "daughter", "daughters", "cousin", "cousins", "brother-in-law", "stepbrother", "stepbrothers","brother", "brothers", "sibling", "uncle", "niece", "husband", "ex-husband", "grandfather","grandson", "wife", "ex-wife", "nephew"]
working_dir = ".../sec-edgar-filings"
for company in os.listdir(working_dir):
    print("Working on company: " + company)
    for filing in os.listdir(working_dir+"//"+company+r"/DEF 14A"):
        file = open(working_dir+"/"+company+r"/DEF 14A/"+filing+r"/full-submission.txt", 'r')
        file_lines = file.readlines()
        company_data = ''
        for line in file_lines:
            if "FILED AS OF DATE:" in line:
                company_data+=(line[20:].strip('\n') +'|')
            elif "COMPANY CONFORMED NAME:" in line:
                company_data+=(line[28:].strip('\n') + '|')
            elif "CENTRAL INDEX KEY:" in line:
                company_data+=(line[23:].strip('\n') + '|')
                break
        file.close()
        file = open(working_dir+"/"+company+r"/DEF 14A/"+filing+r"/full-submission.txt", 'r')
        file_text = file.read()
        file.close()
        for q in queries:
            start_index = file_text.find(" " + q + " ")
            if start_index != -1:
                end_index = start_index + len(q)
                out_text = file_text[max(start_index - surrounding_chars, 0):min(end_index + surrounding_chars, len(file_text))]
                if "Sign exactly as your name(s) appear(s) on the stock certificate. If shares of stock stand of record in the names of two or more persons, or in the name of husband and wife, whether as joint tenants or otherwise, both or all of such persons should sign the proxy card. If shares of stock are held of record by a corporation, the proxy card should be executed by" in out_text:
                    continue
                writetext = company_data+out_text.replace('\n', '')
                outfile.write(writetext + ' \n')