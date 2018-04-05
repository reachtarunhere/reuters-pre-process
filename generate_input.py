import glob
import json
import spacy
import itertools
import sys

# Load Model (Useful even if helpers are imported to some other files)

nlp = spacy.load('en', disable=['ner', 'tagger'])

# Helper Functions


def get_all_files(root): return glob.glob(root + "/*/*/*.sents")


def make_save_path(load_path):
    """Hacky placeholder. Modify if need custom directory etc"""
    return load_path.replace('.sents', '.copr') # conll input format


def get_sentences_from_file(path):
    with open(path, 'r') as f:
        sentences = f.readlines()
    return sentences


def filter_out_sents(sent_list):

    def include_sent(s):
        bad_sents = ['”', ]  # Add more if discovered.
        if s in bad_sents:
            return False
        elif len(s) < 35: # Min chars in a sentence.
            return False
        return True
    return [s for s in sent_list if include_sent(s)]


def break_sentences(sent_list):
    """ Processing together for multiple sentences.
        Might consider writing sentences one at a time to avoid memory problems."""
    sentences_tokenized = []

    for sent in nlp.pipe(sent_list, batch_size=100, n_threads=3):
        sentences_tokenized.extend([w.string.strip() for w in sent])

    return sentences_tokenized


def process_single_file(load_path, save_path):

    sentences = get_sentences_from_file(load_path)
    valid_sentences = filter_out_sents(sentences)
    sentences_tokenized = break_sentences(valid_sentences)

    with open(save_path, mode='wt', encoding='utf-8') as w_file:
        w_file.write('-DOCSTART-\n\n' + '\n'.join(sentences_tokenized))


if __name__ == '__main__':

    crawled_folder = sys.argv[1]  # Lazy hack. Could use argparse instead.
    all_files = get_all_files(crawled_folder)

    for load_path in all_files:

        print("Processing", load_path)
        process_single_file(load_path, make_save_path(load_path))
