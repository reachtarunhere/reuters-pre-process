import glob

# Helper Functions


def get_all_files(root): return glob.glob(root + "/*/*/*.json")
