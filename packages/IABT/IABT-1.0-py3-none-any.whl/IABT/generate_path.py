import os


def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        return


def create_paths(path_list):
    for i in path_list:
        create_path(i)


def create_file(file_path, file_name, write=""):
    pattern = ["\\", "/"][int("/" in file_path)]
    if file_path[-1] != pattern:
        file_path += pattern
    if not os.path.exists(file_path):
        create_path(file_path)
    if write == "":
        open(file_path + file_name, "w", encoding="utf-8").close()
    else:
        with open(file_path + file_name, "w", encoding="utf-8") as f:
            f.write(write)


def create_files(file_list):
    for i in file_list:
        create_file(*i)


if __name__ == '__main__':
    ...
