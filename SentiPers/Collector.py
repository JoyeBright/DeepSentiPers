from SentiPers import Parser
import pandas as pd

all_sentences = []


def collect_all_sentences():
    main_review_sentences = Parser.get_main_review_sents()  # Get all main review senteces
    for sen in main_review_sentences:   # Add all of them
        all_sentences.append(main_review_sentences.get(sen))

    all_general_review = Parser.get_general_reviews()   # Get all general review
    for r in all_general_review:
        for sen in all_general_review.get(r).get('Sentences'):  # Get all sentence of every review
            all_sentences.append(all_general_review.get(r).get('Sentences').get(sen))   # Add all of them

    all_critical_review = Parser.get_critical_reviews()     # Get all critical review
    for r in all_critical_review:
        for sen in all_critical_review.get(r).get('Sentences'):     # Get all sentence of every review
            all_sentences.append(all_critical_review.get(r).get('Sentences').get(sen))  # Add all of them

    for sentence in all_sentences:  # Converting every target dictionary to a list
        target_list = list(sentence.get('Targets').values())
        sentence['Targets'] = target_list


Parser.main()               # Run parser
collect_all_sentences()     # Collect sentences from parser

# Print the number of sentences
print("The number of all sentences : ", len(all_sentences))

# Print some sentences as example
print("Example: ")
for i in all_sentences[0:10]:
    print(i)

# This is how you can access to each detail
print("Text of third sentence : ", all_sentences[2]['Text'])
print("Targets of third sentence : ", all_sentences[2]['Targets'])
print("Opinions of first target of third sentence : ", all_sentences[2]['Targets'][0]['Opinions'])
print("Keywords of third sentence : ", all_sentences[2]['Keywords'])

dataframe = pd.DataFrame.from_dict(all_sentences)
print("------------------ Data Frame ------------------")
print(dataframe.head())
print(dataframe.columns.values)

# Save dataframe as csv file
dataframe.to_csv('data.csv', sep='\t', encoding='utf-8', index=False)

# Read dataframe from csv file
print("------------------ Loading from CSV file ------------------")
df = pd.read_csv('data.csv', sep='\t', encoding='utf-8')
print(df.head())
print(df.loc[2])


