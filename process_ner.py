import glob
import json

# Helper Functions


def get_all_files(root): return glob.glob(root + "/*/*/*.json")


def get_articles_from_file(path):
    with open(path, 'r') as f:
        articles = [json.loads(article) for article in f.readlines()]
    return articles
