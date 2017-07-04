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

from rbd_tree import RbdItem, RbdRootItem
from ab_tree import ShellTree
import ceph_client
import re


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
        description='Print rbd volumes/snapshot in tree',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--user', '-u', default='admin',
                        help='the ceph user')
    parser.add_argument('--cluster', '-c', default='ceph',
                        help='the ceph cluster name')
    parser.add_argument('--conffile', '-C', default='/etc/ceph/ceph.conf',
                        help='the ceph config file')
    parser.add_argument('--parents', '-P', action='store_true',
                        help='show parents or not')
    parser.add_argument('--pool', '-p', default='rbd_ssd',
                        help='the pool name')
    parser.add_argument('vol', nargs='?', default='',
                        help='the volume id or rbd image id, '
                        'print the all volumes if vol is not specified')
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    _setup_logger(level=log_level)

    ceph_client.RadosClient.initialize(
        args.pool, args.conffile, args.user, args.cluster)
    with ceph_client.RadosClient() as client:
        ceph_client.ioctx = client.ioctx
        if args.vol:
            image_id = args.vol
            # replace cinder volume id with rbd image name
            if re.match(r'^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$', image_id):
                image_id = 'volume-{}'.format(image_id)
            if args.parents:
                image_id = ceph_client.get_root(image_id)
            root = RbdItem(image_id)
        else:
            root_vols = ceph_client.get_root_vols()
            root = RbdRootItem(root_vols)
        tree = ShellTree(root)
    tree.draw()


if __name__ == '__main__':
    main()
