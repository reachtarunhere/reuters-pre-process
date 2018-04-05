import glob

def get_all_files(root): return glob.glob(root + "/*/*/*.copr")

def process_single_file(path, output_file):
    with open(path, 'r') as f:
        lines = f.readlines()
    lines = lines[1:]
    output_file.writelines(lines)

if __name__ == '__main__':

    crawled_folder = sys.argv[1]  # Lazy hack. Could use argparse instead.
    output_file_path = sys.argv[2]
    all_files = get_all_files(crawled_folder)

    output_file = open(output_file_path, 'a', encoding='utf-8')
    output_file.writelines(['-DOCSTART-\n'])

    for load_path in all_files:

        print("Processing", load_path)
        process_single_file(load_path, output_file)

