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

import logging

import ceph_client
from ab_tree import TreeItem

LOG = logging.getLogger(__name__)


class RbdRootItem(TreeItem):
    '''
    To present a node in the tree

    The node could be either a volume or a snapshot
    '''

    def __init__(self, root_vols, name="ROOT"):
        '''
        :param name: the root name of the tree
        :param root_vols: the volumes whose don't have parent
        '''
        TreeItem.__init__(self, name)
        self.name = name
        self.root_vols = root_vols

    def search_children(self):
        '''Find the children by ceph command'''
        LOG.debug('find children of {}'.format(self))
        for vol in self.root_vols:
            self.children.append(RbdItem(vol))

    def __str__(self):
        return self.name or str(self.sid or self.vid)


class RbdItem(TreeItem):
    '''
    To present a node in the tree

    The node could be either a volume or a snapshot
    '''

    def __init__(self, vid, sid=None, name=""):
        '''
        :param vid: the rbd image id
        :param sid: the snapshot id
        :param name: the cinder volume name
        '''
        self.vid = vid
        self.name = name
        self.sid = sid
        TreeItem.__init__(self, name)

    def search_children(self):
        '''Find the children by librbd'''
        LOG.debug('find children of {}'.format(self))
        if not self.sid:
            children_ids = ceph_client.get_snaps(self.vid)
        else:
            children_ids = ceph_client.get_children_vols(self.vid, self.sid)
        for child_id in children_ids:
            if self.sid:
                self.children.append(RbdItem(child_id, name=self.name))
            else:
                self.children.append(RbdItem(self.vid, sid=child_id,
                                             name=self.name))

    def __str__(self):
        return self.name or str(self.sid or self.vid)
