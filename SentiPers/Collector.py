from SentiPers import Parser
import pandas as pd

all_sentences = []


def collect_all_sentences():
    main_review_sentences = Parser.get_main_review_sentences()  # Get all main review sentences
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


data_frame = pd.DataFrame.from_dict(all_sentences)

# Save data frame as csv file
data_frame.to_csv('Data.csv', sep='\t', encoding='utf-8', index=False)



