# Copyright 2017 IBM Corporation.
# Copyright 2017, Cheng Li <shcli@cn.ibm.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import subprocess
import logging

LOG = logging.getLogger(__name__)


def run_cmd(command, allow_error=False):
    '''
    Run the command and return stdout.

    By default, exiting the program if return code isn't zero.

    :param command: the command to run
    :param allow_error: if allow_error is True, not exiting program
    '''
    stdout = None
    try:
        LOG.debug('run command: {}'.format(' '.join(command)))
        stdout = subprocess.check_output([str(word) for word in command])
    except subprocess.CalledProcessError as err:
        LOG.error(err)
        if not allow_error:
            os._exit(1)
    return stdout
