# -*- coding: utf-8 -*-
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
import re
import logging

from utils import run_cmd
from ab_tree import TreeItem

LOG = logging.getLogger(__name__)


class RbdItem(TreeItem):
    '''
    To present a node in the tree

    The node could be either a volume or a snapshot
    '''

    def __init__(self, vid, pool, sid=None, name=""):
        '''
        :param vid: the rbd image id
        :param pool: the ceph pool name
        :param sid: the snapshot id
        :param name: the cinder volume name
        '''
        self.vid = vid
        self.name = name
        self.sid = sid
        self.pool = pool
        TreeItem.__init__(self, name)

    def search_children(self):
        '''Find the children by ceph command'''
        LOG.debug('find children of {}'.format(self))
        if not self.sid:
            rbd_out = run_cmd(['rbd', '-p', self.pool,
                               'snap', 'ls', self.vid])
        else:
            rbd_out = run_cmd(['rbd', '-p', self.pool, 'children',
                               '{}@{}'.format(self.vid, self.sid)])
        for child_id in re.findall(r'volume[^\s]+|snapshot[^\s]+', rbd_out):
            if self.sid:
                self.children.append(RbdItem(child_id, pool=self.pool,
                                             name=self.name))
            else:
                self.children.append(RbdItem(self.vid, pool=self.pool,
                                             sid=child_id, name=self.name))

    def __str__(self):
        return self.name or str(self.sid or self.vid)
