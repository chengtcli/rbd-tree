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

import logging
import argparse

from rbd_tree import RbdItem
from ab_tree import ShellTree


def _setup_logger(level=logging.INFO):
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    handler = logging.StreamHandler()
    fmt = logging.Formatter(fmt='%(asctime)s %(threadName)s %(name)s '
                            '%(levelname)s: %(message)s',
                            datefmt='%F %H:%M:%S')
    handler.setFormatter(fmt)
    root_logger.addHandler(handler)


def main():
    parser = argparse.ArgumentParser(
        description='Print rbd volumes/snapshot in tree')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('pool', nargs='?', default='rbd_ssd',
                        help='the pool name, default: rbd_ssd')
    parser.add_argument('vol', help='the volume id or rbd image id')
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    _setup_logger(level=log_level)

    image_id = (args.vol if args.vol.startswith('volume') else
                'volume-{}'.format(args.vol))
    root = RbdItem(image_id, pool=args.pool)
    tree = ShellTree(root)
    tree.draw()


if __name__ == '__main__':
    main()
