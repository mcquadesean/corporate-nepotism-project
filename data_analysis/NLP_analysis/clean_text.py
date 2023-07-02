#######################################################################################
# DESCRIPTION
# This script is a first pass at parsing individual names and familial ties from a dataset containing 
# cases of nepotism reported in SEC filings
# SM June 2023
######################################################################################
# IMPORT LIBRARIES
from bs4 import BeautifulSoup
import re
import pandas as pd
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm") # Load the spaCy English model
#######################################################################################
# DATA PREP
# Load in main dataframe
main_data = pd.read_excel("C:/Users/user/Documents/Honors Thesis/Part 2- Background Analysis/Data/Name Data Collection.xlsx")

# Clean up html formatting to help in NLP model
def remove_html_tags(text):
    if isinstance(text, str):
        soup = BeautifulSoup(text, "lxml")
        cleaned_text = soup.get_text(separator=" ")
        return cleaned_text
    else:
        return text
html_column = "Sentence"
main_data[html_column] = main_data[html_column].apply(remove_html_tags)

# Specify the column containing the sentences
sentence_column = "Sentence"

# Create new columns for extracted familial relationships
max_names = 4  # Maximum number of names in a sentence
for i in range(max_names):
    main_data[f"extracted_name_{i+1}"] = ""
    main_data[f"familial_relationship_{i+1}"] = ""
#######################################################################################
# NLP MODEL FOR IDENTIFYING NAMES AND RELATIONSHIPS

# Define the pattern for matching familial relationships
pattern = [[{"LOWER": "wife"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}], 
[{"LOWER": "husband"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "son"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}], 
[{"LOWER": "daughter"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}], 
[{"LOWER": "stepson"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "stepdaughter"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "step-son-in-law"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "son-in-law"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "sons"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "stepfather"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "step-father"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "step-fatherin-law"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "father-in-law"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "stepmother"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "step-mother"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "step-mother-in-law"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "mother-in-law"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "mother"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "sister-in-law"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "sister"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "stepdaughter"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "step-daughter"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "step-daughter-in-law"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "daughter-in-law"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "daughters"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "cousin"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "cousins"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "brother-in-law"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "stepbrother"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "stepbrothers"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "brother"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "brothers"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "sibling"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "uncle"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "niece"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "ex-husband"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "ex-wife"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "grandfather"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "grandson"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "grandmother"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "gradaughter"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}],
[{"LOWER": "nephew"}, {"POS": "ADP"}, {"ENT_TYPE": "PERSON"}]]

# Load in NLP matcher
matcher = Matcher(nlp.vocab)
matcher.add("FamilialRelationships", pattern)

# Process each sentence and extract familial relationships
for index, row in main_data.iterrows():
    sentence = row[sentence_column]
    
    if isinstance(sentence, str):
        doc = nlp(sentence)
        
        matches = matcher(doc)
        extracted_names = []
        familial_relationships = []
        
        for match_id, start, end in matches:
            relation = doc[start:end+1].text
            person = doc[start-1].text
            extracted_names.append(person)
            familial_relationships.append(relation.capitalize())
        
        for i in range(max_names):
            if i < len(extracted_names):
                main_data.at[index, f"extracted_name_{i+1}"] = extracted_names[i]
                main_data.at[index, f"familial_relationship_{i+1}"] = familial_relationships[i]


output_file = "C:/Users/user/Documents/Honors Thesis/Part 2- Background Analysis/Data/name_data_collection_cleaned_text.xlsx"

main_data.to_excel(output_file, index=False)

