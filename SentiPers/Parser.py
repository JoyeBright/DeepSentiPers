from xml.etree import ElementTree
import os

main_review_sentences = {}  # A dictionary that contains sentences of main review
all_general_review = {}     # A dictionary that contains all general reviews and their sentences
all_critical_review = {}   # A dictionary that contains all critical reviews and their sentences
post_counter = 1
last_target = None
display = {'vmr': 0,  # Total Value of Main Review
           'mrs': 0,   # Main Review Sentences
           'agr': 0,   # All General Review
           'acr': 0    # All Critical Review
           }


def parser(file_name):
    full_path = os.path.abspath(os.path.join('Data', file_name))
    tree = ElementTree.parse(full_path)

    # Find the total value of main review
    if display['vmr']:
        review = tree.findall('Review')
        review_attributes = review[0].attrib
        review_total_value = review_attributes["Value"]
        print("\n", review_total_value, "****")

    # Find main review and remember it's sentences in a dictionary
    review_sentences = tree.findall('Review/Sentence')
    for sentence in review_sentences:
        main_review_sentences[str(post_counter) + sentence.attrib.get('ID')] = \
            {'Value': sentence.attrib.get('Value'), 'Text': sentence.text, 'Targets': {}, 'Negative-Keywords': [],
             'Neutral-Keywords': [], 'Positive-Keywords': []}
    if display['mrs']:
        print_dictionary(main_review_sentences)

    # Find all general review and remember their sentences in a dictionary
    general_reviews = tree.findall('General_Reviews/General_Review')
    for review in general_reviews:
        # Find every sentences in this review
        sentences_in_review = review.findall('Sentence')
        inner_counter = 1
        sentences = {}
        for sentence in sentences_in_review:
            sentences[str(post_counter) + sentence.attrib.get('ID')] = \
                {'Value': sentence.attrib.get('Value'),  'Text': sentence.text, 'Targets': {},
                 'Negative-Keywords': [], 'Neutral-Keywords': [], 'Positive-Keywords': []}
            inner_counter += 1
        # Add this review and it's sentences to our dictionary
        all_general_review[str(post_counter) + review.attrib.get('ID')] = \
            {'Post': file_name, 'Value': review.attrib.get('Value'),
             'Sentences': sentences}

    # Find all critical review and remember their sentences in a dictionary
    critical_reviews = tree.findall('Critical_Reviews/Critical_Review')
    for review in critical_reviews:
        # Find every sentences in this review
        sentences_in_review = review.findall('Sentence')
        inner_counter = 1
        sentences = {}
        for sentence in sentences_in_review:
            sentences[str(post_counter) + sentence.attrib.get('ID')] = \
                {'Value': sentence.attrib.get('Value'), 'Text': sentence.text, 'Targets': {},
                 'Negative-Keywords': [], 'Neutral-Keywords': [], 'Positive-Keywords': []}
            inner_counter += 1
        # Add this review and it's sentences to our dictionary
            all_critical_review[str(post_counter) + review.attrib.get('ID')] = \
                {'Post': file_name, 'Value': review.attrib.get('Value'), 'Sentences': sentences}

    # Find keywords and set them to sentences
    set_keywords(tree)
    set_tags(tree)


def add_keyword(dictionary, index, text, value):
    if value == '+':    # Check keyword type
        k_list = dictionary.get(index).get('Positive-Keywords')     # Get current list
        k_list.append(text)     # Add new keyword
        dictionary.get(index).update({'Positive-Keywords': k_list})     # Update
    elif value == '-':
        k_list = dictionary.get(index).get('Negative-Keywords')
        k_list.append(text)
        dictionary.get(index).update({'Negative-Keywords': k_list})
    else:
        k_list = dictionary.get(index).get('Neutral-Keywords')
        k_list.append(text)
        dictionary.get(index).update({'Neutral-Keywords': k_list})


def set_keywords(tree):
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
            value = keyword.attrib.get('Value')
            add_keyword(main_review_sentences, index, keyword_str, value)

        # If it relates to a sentence of general review
        elif sentence_id[0] == 'g':
            splitted_id = sentence_id.split('-')
            review_id = splitted_id[0] + "-" + splitted_id[1]
            review_index = str(post_counter) + review_id
            sentence_index = str(post_counter) + sentence_id
            keyword_str = all_general_review.get(review_index).get('Sentences').get(sentence_index).get('Text')
            keyword_str = keyword_str[int(pos[0]):int(pos[1])]
            value = keyword.attrib.get('Value')
            add_keyword(all_general_review.get(review_index).get('Sentences'), sentence_index, keyword_str, value)

        # If it relates to a sentence of critical review
        elif sentence_id[0] == 'c':
            splitted_id = sentence_id.split('-')
            review_id = splitted_id[0] + "-" + splitted_id[1]
            review_index = str(post_counter) + review_id
            sentence_index = str(post_counter) + sentence_id
            keyword_str = all_critical_review.get(review_index).get('Sentences').get(sentence_index).get('Text')
            keyword_str = keyword_str[int(pos[0]):int(pos[1])]
            value = keyword.attrib.get('Value')
            add_keyword(all_critical_review.get(review_index).get('Sentences'), sentence_index, keyword_str, value)


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


def get_main_review_sentences():
    return main_review_sentences


def get_general_reviews():
    return all_general_review


def get_critical_reviews():
    return all_critical_review
