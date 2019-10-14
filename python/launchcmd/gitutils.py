# stdlib modules
import os
import subprocess


def _run_check_output(cmd):
    # check output
    output = subprocess.check_output(cmd, shell=True)

    # cast to string, remove surrounding whitespaces and traing line separator
    output_str = output.decode("utf-8")
    output_str = output_str.strip()
    output_str = output_str.rstrip(os.linesep)

    # split by line separator
    lines = [] if not output_str else output_str.split(os.linesep)

    return lines


def validate_repository_dir(repository_dir):
    contents = os.listdir(repository_dir)
    if ".git" not in contents:
        msg = "following directory is not a git repository, no .git directory found: {}"
        raise IOError(msg.format(repository_dir))


def get_tags(repository_dir):
    cmd = "cd {} && git tag".format(repository_dir)
    tags = _run_check_output(cmd)
    return tags


def get_status(repository_dir):
    cmd = "cd {} && git status --porcelain".format(repository_dir)
    status = _run_check_output(cmd)
    return status


def create_tag(repository_dir, tag_name):
    cmd = "cd {} && git tag {}".format(repository_dir, tag_name)
    _run_check_output(cmd)


def clone_repository(repository_dir, clone_dir):
    # ensure the cmd looks like cp -R $repository_dir/* $clone_dir/
    if not repository_dir.endswith(os.sep):
        repository_dir += os.sep
    repository_dir += "*"

    if not clone_dir.endswith(os.sep):
        clone_dir += os.sep

    cmd = "cp -R {} {}".format(repository_dir, clone_dir)
    _run_check_output(cmd)
