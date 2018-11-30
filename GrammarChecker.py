import nltk
import re
import csv
from sklearn.externals import joblib


class GrammarChecker:

    def __init__(self):
        self.classifier = joblib.load('POStagger.joblib')
        self.rules_A = {}
        self.rules_B = {}
        self.error_count = 0
        self.error_list = []
        self.__LoadRules__('grammarRules.csv')

    def __LoadRules__(self, file_name):
        with open(file_name, mode='r') as infile:
            reader = csv.reader(infile)
            for rows in reader:
                if rows[0][0] == 'A':
                    self.rules_A[rows[0]] = [rows[1], rows[2]]
                else:
                    self.rules_B[rows[0]] = [rows[1], rows[2]]
            del self.rules_B['Index']

    # _______ assign_tag _________
    # input: list of raw sentences
    # output: list of tagged sentences
    # description:  the function assign POS tags to the given sentences. Return list of tagged sentences
    def assign_tag(self, sents):
        # tokenize sentences
        sents = [nltk.word_tokenize(sent) for sent in sents]
        sent2features = [[pos_features(sent, i) for i in range(len(sent))] for sent in sents]

        # predict labels using trained model
        labels = self.classifier.predict(sent2features)
        # combining words and their assigned labels
        tagged_sents = []
        for i in range(len(sents)):
            tagged_sent = list(zip(sents[i], labels[i]))
            tagged_sents.append(tagged_sent)
        return tagged_sents

    # _____________ find_errors ________________
    # input: 'sents' - list of raw sentences
    # output:
    #       'error_list' - list of error list for each sentence, each error list
    #                      contains tuples in form of (error_substring, error name, error message)
    #       'error_count' - number of errors found
    # description:  the function performs two-level grammar checking using regular expression
    #               loaded from 'GrammarRules.csv'. Only acknowledging 'group B' errors if
    #               they are not a part of errors found in 'group A' errors
    def find_errors(self, sents):
        tagged_sents = self.assign_tag(sents)
        # create tagged strings for REGEX lookup
        formatted_sents = list2str(tagged_sents)
        # perform grammar checking
        error_list = []
        error_count = 0
        for sent in formatted_sents:
            temp_pos_list = []  # store start+end position of a grammar error
            temp_error_list = []  # store sub-string containing error & error type
            # check Rules A: Complex Grammar Structure
            for rule in self.rules_A.items():
                pattern = re.compile(rule[1][0]) # compile a regular expression
                result = pattern.search(sent)
                if result is not None:
                    temp_pos_list.append((result.start(), result.end()))
                    error_count += 1
                    temp_error_list.append((result.group(), rule[0], rule[1][1]))
            # check Rules B: Basic Grammar Structure
            for rule in self.rules_B.items():
                pattern = re.compile(rule[1][0]) # compile a regular expression
                result = pattern.search(sent)
                if result is not None:
                    if overlap_test((result.start(), result.end()), temp_pos_list) == 0:
                        error_count += 1
                        temp_error_list.append((result.group(), rule[0], rule[1][1]))
            error_list.append(temp_error_list if len(temp_error_list) != 0 else None)
        if error_count == 0:
            return None
        else:
            return error_list, error_count


# ____________UTILITY FUNCTIONS____________

def pos_features(sentence, i):
    current = sentence[i]

    # previous word
    if (i>0):
        prev_w = sentence[i-1]
    else:
        prev_w = "<START>"

    # next word
    if (i<len(sentence)-1):
        next_w = sentence[i+1]
    else:
        next_w = "<END>"

    # generate feature sets
    features = {
        "word": current,
        "next_word": next_w,
        "prev_word": prev_w,
        "suffix(1)": current[-1:],
        "suffix(2)": current[-2:],
        "suffix(3)": current[-3:],
        "prefix(1)": current[0],
        "prefix(2)": current[:2],
        "prefix(3)": current[:3],
        "prev_suffix(1)": prev_w[-1:],
        "prev_suffix(2)": prev_w[-2:],
        "prev_suffix(3)": prev_w[-3:],
        "prev_prefix(1)": prev_w[0],
        "prev_prefix(2)": prev_w[:2],
        "prev_prefix(3)": prev_w[:3],
        "next_suffix(1)": next_w[-1:],
        "next_suffix(2)": next_w[-2:],
        "next_suffix(3)": next_w[-3:],
        "next_prefix(1)": next_w[0],
        "next_prefix(2)": next_w[:2],
        "next_prefix(3)": next_w[:3],
        'is_first': i == 0,
        'is_last': i == len(sentence) - 1,
        'curr_is_title': current.istitle(),
        'prev_is_title': prev_w.istitle(),
        'next_is_title': next_w.istitle(),
        'curr_is_lower': current.islower(),
        'prev_is_lower': prev_w.islower(),
        'next_is_lower': next_w.islower(),
        'curr_is_upper': current.isupper(),
        'prev_is_upper': prev_w.isupper(),
        'next_is_upper': next_w.isupper(),
        'curr_is_digit': current.isdigit(),
        'prev_is_digit': prev_w.isdigit(),
        'next_is_digit': next_w.isdigit()
    }
    return features


def list2str(tagged_sents):
    formatted_sents = [['/'.join([a,b]) for (a,b) in sent] for sent in tagged_sents]
    formatted_sents = [' '.join(sent) for sent in formatted_sents]
    return formatted_sents


def overlap_test(a, bs):
    for b in bs:
        if b[0] < a[0] and a[1] < b[1]:
            return 1
    return 0


def display_errors(sents, error_lists):
    total = 0
    for i in range(len(sents)):
        if error_lists[i] is not None:
            total += len(error_lists[i])
            print('\nFOUND {0} ERROR IN: {1}'.format(len(error_lists[i]), sents[i]))
            for error in error_lists[i]:
                print("\t {0}: {1} -> {2}".format(error[1], error[0], error[2]))
    print("TOTAL ERRORS FOUND: {0}".format(total))
