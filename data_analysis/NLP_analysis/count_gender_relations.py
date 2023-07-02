import pandas as pd

def calculate_male_percentage(relationship_list):
    male_terms = ["stepson","step-son-in-law", "son-in-law", "son", "sons", "stepfather", "step-father", "step-fatherin-law", "father-in-law", "father", "brother-in-law", "stepbrother", "stepbrothers","brother", "brothers", "uncle", "husband", "ex-husband", "grandfather","grandson", "nephew"]
    male_count = 0
    total_count = 0

    for term in relationship_list:
        if term.lower() in male_terms:
            male_count += 1
        total_count += 1

    if total_count == 0:
        return 0

    male_percentage = (male_count / total_count) * 100
    return male_percentage

relationship_data = pd.read_excel(".../aggregate_relationship_list.xlsx")
relationship_list = relationship_data["Relationship"].tolist()

percentage = calculate_male_percentage(relationship_list)
print(f"Male Percentage: {percentage}%")
