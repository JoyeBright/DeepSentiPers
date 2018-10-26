from xml.etree import ElementTree
import os
import pandas as pd

main_review_sentences = {}  # A dictionary that contains sentences of main review
all_general_review = {}     # A dictionary that contains all general reviews and their sentences
all_critical_review = {}   # A dictionary that contains all critical reviews and their sentences
post_counter = 1
last_target = None
all_sentences = []


def parser(file_name):
    full_path = os.path.abspath(os.path.join('Data', file_name))
    tree = ElementTree.parse(full_path)

    # Find main review and remember it's sentences in a dictionary
    review_sentences = tree.findall('Review/Sentence')
    for sentence in review_sentences:
        main_review_sentences[str(post_counter) + sentence.attrib.get('ID')] = \
            {'Value': sentence.attrib.get('Value'),
             'Text': sentence.text, 'Targets': {}, 'Keywords': []}
        # print(sentence.attrib, sentence.text)
    # print_dictionary(main_review_sentences)

    # Find all general review and remember their sentences in a dictionary
    general_reviews = tree.findall('General_Reviews/General_Review')
    for review in general_reviews:
        # Find every senteces in this review
        sentences_in_review = review.findall('Sentence')
        inner_counter = 1
        senteces = {}
        for sentence in sentences_in_review:
            senteces[str(post_counter) + sentence.attrib.get('ID')] = \
                {'Value': sentence.attrib.get('Value'),
                 'Text': sentence.text, 'Targets': {}, 'Keywords': []}
            inner_counter += 1
        # Add this review and it's senteces to our dictionary
        all_general_review[str(post_counter) + review.attrib.get('ID')] = \
            {'Post': file_name, 'Value': review.attrib.get('Value'),
             'Sentences': senteces}
    # print_dictionary(all_general_review)

    # Find all critical review and remember their sentences in a dictionary
    critical_reviews = tree.findall('Critical_Reviews/Critical_Review')
    for review in critical_reviews:
        # Find every senteces in this review
        sentences_in_review = review.findall('Sentence')
        inner_counter = 1
        senteces = {}
        for sentence in sentences_in_review:
            senteces[str(post_counter) + sentence.attrib.get('ID')] = \
                {'Value': sentence.attrib.get('Value'),
                 'Text': sentence.text, 'Targets': {}, 'Keywords': []}
            inner_counter += 1
        # Add this review and it's senteces to our dictionary
            all_critical_review[str(post_counter) + review.attrib.get('ID')] = \
                {'Post': file_name, 'Value': review.attrib.get('Value'), 'Sentences': senteces}
    # print_dictionary(all_critical_review)

    # Find keywords and set them to sentences
    add_keywords(tree)
    set_tags(tree)


def add_keywords(tree):
    keywords = tree.findall('Keywords/Keyword')
    for keyword in keywords:
        coordinate = keyword.attrib.get('Coordinate')
        coordinate = coordinate[1:-1]
        splitted = coordinate.split(',')
        sentence_id = splitted[0]
        pos = splitted[1:3]

        # If it relates to a sentence of main review
        if sentence_id[0] == 'r':
            index = str(post_counter) + sentence_id
            keyword_str = main_review_sentences.get(index).get('Text')
            keyword_str = keyword_str[int(pos[0]):int(pos[1])]
            k = {'Position': pos, 'Value': keyword.attrib.get('Value'), 'Text': keyword_str}
            k_list = main_review_sentences.get(index).get('Keywords')    # Load keywords list for this sentence
            k_list.append(k)     # Add new keyword
            main_review_sentences.get(index).update({'Keywords': k_list})     # Update senetence dictionary
            # print(keyword_str)
            # print(main_review_sentences.get(index))

        # If it relates to a sentence of general review
        elif sentence_id[0] == 'g':
            splitted_id = sentence_id.split('-')
            review_id = splitted_id[0] + "-" + splitted_id[1]
            review_index = str(post_counter) + review_id
            sentence_index = str(post_counter) + sentence_id
            keyword_str = all_general_review.get(review_index).get('Sentences').get(sentence_index).get('Text')
            keyword_str = keyword_str[int(pos[0]):int(pos[1])]
            k = {'Position': pos, 'Value': keyword.attrib.get('Value'), 'Text': keyword_str}
            k_list = all_general_review.get(review_index).get('Sentences').get(sentence_index).get('Keywords')
            k_list.append(k)  # Add new keyword
            all_general_review.get(review_index).get('Sentences').get(sentence_index).update({'Keywords': k_list})
            # print(keyword_str)
            # print(all_general_review.get(review_index).get('Sentences').get(sentence_index))

        # If it relates to a sentence of critical review
        elif sentence_id[0] == 'c':
            splitted_id = sentence_id.split('-')
            review_id = splitted_id[0] + "-" + splitted_id[1]
            review_index = str(post_counter) + review_id
            sentence_index = str(post_counter) + sentence_id
            keyword_str = all_critical_review.get(review_index).get('Sentences').get(sentence_index).get('Text')
            keyword_str = keyword_str[int(pos[0]):int(pos[1])]
            k = {'Position': pos, 'Value': keyword.attrib.get('Value'), 'Text': keyword_str}
            k_list = all_critical_review.get(review_index).get('Sentences').get(sentence_index).get('Keywords')
            k_list.append(k)  # Add new keyword
            all_critical_review.get(review_index).get('Sentences').get(sentence_index).update({'Keywords': k_list})
            # print(keyword_str)
            # print(all_critical_review.get(review_index).get('Sentences').get(sentence_index))


def set_tags(tree):
    main_targets = {}
    tags = tree.findall('Tags/Tag')
    for tag in tags:
        if tag.attrib.get('Type') == 'Target(M)':
            main_targets[tag.attrib.get('ID')] = tag.attrib.get('Root')
        else:
            coordinate = tag.attrib.get('Coordinate')
            coordinate = coordinate[1:-1]
            splitted = coordinate.split(',')
            sentence_id = splitted[0]
            pos = splitted[1:3]
            global last_target
            if sentence_id[0] == 'r':
                index = str(post_counter) + sentence_id
                word = main_review_sentences.get(index).get('Text')
                word = word[int(pos[0]):int(pos[1])]
                if tag.attrib.get('Type') == 'Target(I)':
                    last_target = index
                    related_target_m = main_targets[tag.attrib.get('Relation')]
                    target = {'Position': pos, 'Value': tag.attrib.get('Value'), 'Text': word,
                              'RelationText': related_target_m, 'Opinions': []}
                    main_review_sentences.get(index).get('Targets').update({tag.attrib.get('ID'): target})
                elif tag.attrib.get('Type') == 'Opinion':
                    target_i_id = tag.attrib.get('Relation')
                    opinion = {'Position': pos, 'Value': tag.attrib.get('Value'), 'Text': word}
                    if index == last_target:
                        opinions = main_review_sentences.get(index).get('Targets').get(target_i_id).get('Opinions')
                        opinions.append(opinion)
                        main_review_sentences.get(index).get('Targets').get(target_i_id).update({'Opinions': opinions})
                    else:
                        target = main_review_sentences.get(last_target).get('Targets').get(target_i_id)
                        target.update({'Opinions': [].append(opinion)})
                        main_review_sentences.get(index).update({'Targets': target})

                    # print(main_review_sentences.get(index).get('Targets'))
            elif sentence_id[0] == 'g':
                splitted_id = sentence_id.split('-')
                review_id = splitted_id[0] + "-" + splitted_id[1]
                review_index = str(post_counter) + review_id
                sentence_index = str(post_counter) + sentence_id
                word = all_general_review.get(review_index).get('Sentences').get(sentence_index).get('Text')
                word = word[int(pos[0]):int(pos[1])]
                if tag.attrib.get('Type') == 'Target(I)':
                    last_target = sentence_index
                    related_target_m = main_targets[tag.attrib.get('Relation')]
                    target = {'Position': pos, 'Value': tag.attrib.get('Value'), 'Text': word,
                              'RelationText': related_target_m, 'Opinions': []}
                    all_general_review.get(review_index).get('Sentences').get(sentence_index).get('Targets')\
                        .update({tag.attrib.get('ID'): target})
                elif tag.attrib.get('Type') == 'Opinion':
                    target_i_id = tag.attrib.get('Relation')
                    opinion = {'Position': pos, 'Value': tag.attrib.get('Value'), 'Text': word}
                    if sentence_index == last_target:
                        opinions = all_general_review.get(review_index).get('Sentences').get(sentence_index)\
                            .get('Targets').get(target_i_id).get('Opinions')
                        opinions.append(opinion)
                        all_general_review.get(review_index).get('Sentences').get(sentence_index).get('Targets')\
                            .get(target_i_id).update({'Opinions': opinions})
                        # print(all_general_review.get(review_index).get('Sentences').get(sentence_index).get('Targets'))
                    else:
                        target = all_general_review.get(review_index).get('Sentences').get(last_target)\
                            .get('Targets').get(target_i_id)
                        target.update({'Opinions': []})
                        opinions = target.get('Opinions')
                        opinions.append(opinion)
                        target.update({'Opinions': opinions})
                        target = {target_i_id: target}
                        all_general_review.get(review_index).get('Sentences').get(sentence_index)\
                            .update({'Targets': target})
            elif sentence_id[0] == 'c':
                splitted_id = sentence_id.split('-')
                review_id = splitted_id[0] + "-" + splitted_id[1]
                review_index = str(post_counter) + review_id
                sentence_index = str(post_counter) + sentence_id
                word = all_critical_review.get(review_index).get('Sentences').get(sentence_index).get('Text')
                word = word[int(pos[0]):int(pos[1])]
                if tag.attrib.get('Type') == 'Target(I)':
                    last_target = sentence_index
                    related_target_m = main_targets[tag.attrib.get('Relation')]
                    target = {'Position': pos, 'Value': tag.attrib.get('Value'), 'Text': word,
                              'RelationText': related_target_m, 'Opinions': []}
                    all_critical_review.get(review_index).get('Sentences').get(sentence_index).get('Targets') \
                        .update({tag.attrib.get('ID'): target})
                elif tag.attrib.get('Type') == 'Opinion':
                    target_i_id = tag.attrib.get('Relation')
                    opinion = {'Position': pos, 'Value': tag.attrib.get('Value'), 'Text': word}
                    if sentence_index == last_target:
                        opinions = all_critical_review.get(review_index).get('Sentences').get(sentence_index) \
                            .get('Targets').get(target_i_id).get('Opinions')
                        opinions.append(opinion)
                        all_critical_review.get(review_index).get('Sentences').get(sentence_index).get('Targets') \
                            .get(target_i_id).update({'Opinions': opinions})
                        # print(all_general_review.get(review_index).get('Sentences').get(sentence_index)
                        # .get('Targets'))
                    else:
                        target = all_critical_review.get(review_index).get('Sentences').get(last_target).get(
                            'Targets').get(target_i_id)
                        target.update({'Opinions': []})
                        opinions = target.get('Opinions')
                        opinions.append(opinion)
                        target.update({'Opinions': opinions})
                        target = {target_i_id: target}
                        all_critical_review.get(review_index).get('Sentences').get(sentence_index).update(
                            {'Targets': target})


def print_dictionary(dic):
    for item in dic:
        print(item, dic[item])


def main():
    files = os.listdir(os.path.join('Data'))
    for file in files:
        parser(file)
        global post_counter
        post_counter += 1


def collect_all_sentences():
    for sen in main_review_sentences:   # Add all main review sentences
        all_sentences.append(main_review_sentences.get(sen))
    for r in all_general_review:    # Add all general review sentences
        for sen in all_general_review.get(r).get('Sentences'):
            all_sentences.append(all_general_review.get(r).get('Sentences').get(sen))
    for r in all_critical_review:   # Add all critical review sentences
        for sen in all_critical_review.get(r).get('Sentences'):
            all_sentences.append(all_critical_review.get(r).get('Sentences').get(sen))
    for sentence in all_sentences:  # Converting every target dictionary to a list
        target_list = list(sentence.get('Targets').values())
        sentence['Targets'] = target_list


main()
collect_all_sentences()

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
