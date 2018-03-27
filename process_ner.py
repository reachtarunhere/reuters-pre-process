import glob
import json
import spacy

# Load Model (Useful even if helpers are imported to some other files)

nlp = spacy.load('en', disable=['ner', 'tagger'])

# Helper Functions


def get_all_files(root): return glob.glob(root + "/*/*/*.json")


def get_articles_from_file(path):
    with open(path, 'r') as f:
        articles = [json.loads(article) for article in f.readlines()]
    return articles


def filter_out_invalid(articles):
    """ For < 2 paras only agency info and date are present."""
    return [a for a in articles if len(a['text']) > 2]


def filter_out_header(para_list):

    def not_x_min_read(para):
        return False if para.endswith('Min Read') and len(para.split()) == 3 else True

    return [p for p in para_list if not_x_min_read(p) and p != 'Reuters Staff']


def get_sents_from_text(para_list):

    sentences = []

    for para in nlp.pipe(para_list, batch_size=100, n_threads=3):
        sentences.extend([s.text for s in para.sents])

    return sentences


def filter_out_sents(sent_list):
    bad_sents = ['”', ]  # Add more if discovered.
    return [s for s in sent_list if s not in bad_sents]
