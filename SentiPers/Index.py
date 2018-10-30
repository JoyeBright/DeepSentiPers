from xml.etree import ElementTree
import os

display = {'vmr': 0,  # Total Value of Main Review
           'mrs': 0,   # Main Review Sentences
           'agr': 0,   # All General Review
           'acr': 0    # All Critical Review
           }


main_review_sentences = {}  # A dictionary that contains sentences of main review
all_general_review = {}     # A dictionary that contains all general reviews and their sentences
all_critical_review = {}   # A dictionary that contains all critical reviews and their sentences
post_counter = 1
last_target = None


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
            {'Post': file_name, 'Value': sentence.attrib.get('Value'),
             'Text': sentence.text, 'Targets': {}, 'Keywords': []}
        # print(sentence.attrib, sentence.text)
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
                {'Value': sentence.attrib.get('Value'),
                 'Text': sentence.text, 'Targets': {}, 'Keywords': []}
            inner_counter += 1
        # Add this review and it's sentences to our dictionary
        all_general_review[str(post_counter) + review.attrib.get('ID')] = \
            {'Post': file_name, 'Value': review.attrib.get('Value'),
             'Sentences': sentences}
    if display['agr']:
        print_dictionary(all_general_review)

    # Find all critical review and remember their sentences in a dictionary
    critical_reviews = tree.findall('Critical_Reviews/Critical_Review')
    for review in critical_reviews:
        # Find every sentences in this review
        sentences_in_review = review.findall('Sentence')
        inner_counter = 1
        sentences = {}
        for sentence in sentences_in_review:
            sentences[str(post_counter) + sentence.attrib.get('ID')] = \
                {'Value': sentence.attrib.get('Value'),
                 'Text': sentence.text, 'Targets': {}, 'Keywords': []}
            inner_counter += 1
        # Add this review and it's sentences to our dictionary
            all_critical_review[str(post_counter) + review.attrib.get('ID')] = \
                {'Post': file_name, 'Value': review.attrib.get('Value'), 'Sentences': sentences}
    if display['acr']:
        print_dictionary(all_critical_review)

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
                    target = {'Position': pos, 'Value': tag.attrib.get('Value'), 'Text': word, 'Opinions': [],
                              'RelationID': tag.attrib.get('Relation'), 'RelationText': related_target_m}
                    main_review_sentences.get(index).get('Targets').update({tag.attrib.get('ID'): target})
                elif tag.attrib.get('Type') == 'Opinion':
                    target_i_id = tag.attrib.get('Relation')
                    related_target_i = main_review_sentences.get(last_target).get('Targets')\
                        .get(target_i_id).get('Text')
                    opinion = {'Position': pos, 'Value': tag.attrib.get('Value'), 'Text': word,
                               'RelationID': tag.attrib.get('Relation'), 'RelationText': related_target_i}
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
                    target = {'Position': pos, 'Value': tag.attrib.get('Value'), 'Text': word, 'Opinions': [],
                              'RelationID': tag.attrib.get('Relation'), 'RelationText': related_target_m}
                    all_general_review.get(review_index).get('Sentences').get(sentence_index).get('Targets')\
                        .update({tag.attrib.get('ID'): target})
                elif tag.attrib.get('Type') == 'Opinion':
                    target_i_id = tag.attrib.get('Relation')
                    related_target_i = all_general_review.get(review_index).get('Sentences').get(last_target)\
                        .get('Targets').get(target_i_id).get('Text')
                    opinion = {'Position': pos, 'Value': tag.attrib.get('Value'), 'Text': word,
                               'RelationID': tag.attrib.get('Relation'), 'RelationText': related_target_i}
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
                    target = {'Position': pos, 'Value': tag.attrib.get('Value'), 'Text': word, 'Opinions': [],
                              'RelationID': tag.attrib.get('Relation'), 'RelationText': related_target_m}
                    all_critical_review.get(review_index).get('Sentences').get(sentence_index).get('Targets') \
                        .update({tag.attrib.get('ID'): target})
                elif tag.attrib.get('Type') == 'Opinion':
                    target_i_id = tag.attrib.get('Relation')
                    related_target_i = all_critical_review.get(review_index).get('Sentences').get(last_target) \
                        .get('Targets').get(target_i_id).get('Text')
                    opinion = {'Position': pos, 'Value': tag.attrib.get('Value'), 'Text': word,
                               'RelationID': tag.attrib.get('Relation'), 'RelationText': related_target_i}
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


def print_results():
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("Main review sentences: ", len(main_review_sentences))
    print("Total general review number: ", len(all_general_review))
    total_g_reviews = 0
    for r in all_general_review:
        total_g_reviews += len(all_general_review.get(r).get('Sentences'))
    print("General review sentences: ", total_g_reviews)
    print("Total critical review number: ", len(all_critical_review))
    total_c_reviews = 0
    for r in all_critical_review:
        total_c_reviews += len(all_critical_review.get(r).get('Sentences'))
    print("Critical review sentences: ", total_c_reviews)
    print("Total number of sentences: ", (len(main_review_sentences)+total_c_reviews+total_g_reviews))
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")


main()
print_results()
