import os


def walkpath_get_files(parent_path, extension=".pdf"):
    res = []
    files = None
    for (root,dirs,files) in os.walk(parent_path, topdown=True): 
        for file in files:
            res.append(os.path.join(parent_path, file))
    return res