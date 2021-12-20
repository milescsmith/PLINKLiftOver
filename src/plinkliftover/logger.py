# stolen wholesale from `anndata <https://github.com/theislab/anndata/blob/master/anndata/_core/anndata.py>`_
# BSD 3-Clause License

# Copyright (c) 2017-2018 P. Angerer, F. Alexander Wolf, Theis Lab
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import logging
import os

_previous_memory_usage = None

plo_logger = logging.getLogger("plinkliftover")
# Don’t pass log messages on to logging.root and its handler
plo_logger.propagate = False
plo_logger.setLevel("ERROR")
plo_logger.addHandler(logging.StreamHandler())  # Logs go to stderr
plo_logger.handlers[-1].setFormatter(logging.Formatter("%(message)s"))
plo_logger.handlers[-1].setLevel("ERROR")


def get_logger(name):
    """\
    Creates a child logger that delegates to plo_logger
    instead to logging.root
    """
    return plo_logger.manager.getLogger(name)


def get_memory_usage():
    import psutil

    process = psutil.Process(os.getpid())
    try:
        meminfo = process.memory_info()
    except AttributeError:
        meminfo = process.get_memory_info()
    mem = meminfo[0] / 2 ** 30  # output in GB
    mem_diff = mem
    global _previous_memory_usage
    if _previous_memory_usage is not None:
        mem_diff = mem - _previous_memory_usage
    _previous_memory_usage = mem
    return mem, mem_diff


def format_memory_usage(mem_usage, msg="", newline=False):
    newline = "\n" if newline else ""
    more = " \n... " if msg != "" else ""
    mem, diff = mem_usage
    return (
        f"{newline}{msg}{more}"
        f"Memory usage: current {mem:.2f} GB, difference {diff:+.2f} GB"
    )


def print_memory_usage(msg="", newline=False):
    print(format_memory_usage(get_memory_usage(), msg, newline))
