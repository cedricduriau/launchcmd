# stdlib modules
import os
import re
import shutil


def get_release_files(repository, manifest):
    regexes = list(map(re.compile, manifest["ignore"]))
    files = []
    for dirpath, dirnames, filenames in os.walk(repository):
        for filename in filenames:
            fpath = os.path.join(dirpath, filename)
            skip = False
            for regex in regexes:
                if regex.search(fpath):
                    skip = True
                    break
            if skip:
                continue
            files.append(fpath)
    return files


def copy_release_files(repository, release, files):
    for src_f in files:
        dst_f = src_f.replace(repository, release)
        dst_d = os.path.dirname(dst_f)
        if not os.path.exists(dst_d):
            os.makedirs(dst_d)
        shutil.copy2(src_f, dst_f)
