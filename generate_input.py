import glob
import json
import spacy
import itertools
import sys

# Load Model (Useful even if helpers are imported to some other files)

nlp = spacy.load('en', disable=['ner', 'tagger'])

# Helper Functions


def get_all_files(root): return glob.glob(root + "/*/*/*.json")


def make_save_path(load_path):
    """Hacky placeholder. Modify if need custom directory etc"""
    return load_path.replace('.copr', '.sents') # conll input format


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
    """ Processing together for multiple sentences."""
    pass

def process_single_file(load_path, save_path):

    articles = get_articles_from_file(load_path)
    valid_articles = filter_out_invalid(articles)
    all_paras = [a['text'] for a in valid_articles]
    all_paras = itertools.chain.from_iterable(all_paras)
    all_paras = filter_out_header(all_paras)
    sentences = get_sents_from_text(all_paras)
    sentences = filter_out_sents(sentences)

    with open(save_path, mode='wt', encoding='utf-8') as w_file:
        w_file.write('\n'.join(sentences))


if __name__ == '__main__':

    crawled_folder = sys.argv[1]  # Lazy hack. Could use argparse instead.
    all_files = get_all_files(crawled_folder)

    for load_path in all_files:

        print("Processing", load_path)
        process_single_file(load_path, make_save_path(load_path))
