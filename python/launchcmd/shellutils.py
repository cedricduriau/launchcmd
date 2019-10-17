# stdlib modules
import os
import subprocess


def run_check_output(cmd):
    """Runs a command and returns its output.

    :param cmd: Command to run.
    :type cmd: str

    :rtype: list[str]
    """
    # check output
    output = subprocess.check_output(cmd, shell=True)

    # cast to string, remove surrounding whitespaces and traing line separator
    output_str = output.decode("utf-8")
    output_str = output_str.strip()
    output_str = output_str.rstrip(os.linesep)

    # split by line separator
    lines = [] if not output_str else output_str.split(os.linesep)

    return lines
