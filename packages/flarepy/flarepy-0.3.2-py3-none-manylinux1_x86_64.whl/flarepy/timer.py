# Copyright 2023 Titan-search author.
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
Functions to time flarepy.
"""

from .library import *
from .device import (sync, eval)
from time import time
import math

def timeit(flare_func, *args):
    """
    Function to time flare functions.

    Parameters
    ----------

    flare_func    : flare function

    *args      : arguments to `flare_func`

    Returns
    --------

    t   : Time in seconds
    """

    sample_trials = 3

    sample_time = 1E20

    for i in range(sample_trials):
        start = time()
        res = flare_func(*args)
        eval(res)
        sync()
        sample_time = min(sample_time, time() - start)

    if (sample_time >= 0.5):
        return sample_time

    num_iters = max(math.ceil(1.0 / sample_time), 3.0)

    start = time()
    for i in range(int(num_iters)):
        res = flare_func(*args)
        eval(res)
    sync()
    sample_time = (time() - start) / num_iters
    return sample_time
