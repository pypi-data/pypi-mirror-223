import os

def del_head(path):
    """
    Removes the directory part of a path, returning only the filename.

    :param path: A string representing a path, or a list of strings representing multiple paths.
    :return: If a string was given as input, returns a string representing the filename.
             If a list was given as input, returns a list of strings representing the filenames.
    :raises TypeError: If the input is not a string or a list.
    """
    if isinstance(path, str):
        re_path = os.path.basename(path)
        return re_path
    elif isinstance(path, list):
        re_path = [os.path.basename(_path) for _path in path]
        return re_path
    else:
        raise TypeError(f"Unexpected type {type(path)}. Expected 'list' or 'str'.")

def replace_split_mark(path, mark="/"):
    """
    Replaces the directory separators in a path with a specified character.

    :param path: A string representing a path, or a list of strings representing multiple paths.
    :param mark: The character to use as the new directory separator.
    :return: If a string was given as input, returns a string representing the path with the new directory separators.
             If a list was given as input, returns a list of strings representing the paths with the new directory separators.
    :raises TypeError: If the input is not a string or a list.
    """
    if isinstance(path, str):
        re_path = path.replace("\\\\", "\\").replace("\\", "/").replace("/", mark)
        return re_path
    elif isinstance(path, list):
        re_path = [filepath.replace("\\\\", "\\").replace("\\", "/").replace("/", mark) for filepath in path]
        return re_path
    else:
        raise TypeError(f"Unexpected type {type(path)}. Expected 'list' or 'str'.")

def get_file_list(path, is_dir=True, is_file=True, abs_path=None, all_files=False, extension="", contain="", mark="/"):
    """
    Get a list of files and/or directories from the specified path.
    
    :param path: The directory path from where to get the list.
    :param is_dir: If True, include directories in the list.
    :param is_file: If True, include files in the list.
    :param abs_path: If True, include absolute path. If False, include only file/directory names.
    :param all_files: If True, include all files/directories recursively from the path.
    :param extension: If specified, include only files with this extension.
    :param contain: If specified, include only files/directories containing this string.
    :param mark: The character to use as directory separator. Default is "/".
    :return: A list of files and/or directories.
    """
    onlyfiles = []
    onlydirs = []
    if extension and extension[0]!=".":
        extension='.'+extension
    if all_files:
        if abs_path is None:
            abs_path=True
        if is_file:
            onlyfiles = [os.path.join(cur_dir, file) for cur_dir, dirs, files in os.walk(path) 
                         for file in files if file.endswith(extension) and contain in file]
        if is_dir and not extension:
            onlydirs = [os.path.join(cur_dir, dir) for cur_dir, dirs, files in os.walk(path) 
                        for dir in dirs if contain in dir]
    else:
        if abs_path is None:
            abs_path=False
        if is_file:
            onlyfiles = [os.path.join(path, f) for f in os.listdir(path) 
                         if os.path.isfile(os.path.join(path, f)) and f.endswith(extension) and contain in f]
        if is_dir and not extension:
            onlydirs = [os.path.join(path, f) for f in os.listdir(path) 
                        if os.path.isdir(os.path.join(path, f)) and contain in f]
    file_list = onlyfiles + onlydirs
    file_list = replace_split_mark(file_list, mark=mark)
    if not abs_path:
        file_list = [os.path.basename(_path) for _path in file_list]
    file_list.sort()
    return file_list
