import glob
import json

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
