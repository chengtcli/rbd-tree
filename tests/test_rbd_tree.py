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

import unittest
from mock import patch, call

from rbd_tree import rbd_tree
from rbd_tree.ab_tree import ShellTree


class TestRbdTree(unittest.TestCase):

    @patch('rbd_tree.rbd_tree.ceph_client.get_snaps')
    def test_search_children(self, mock_get_snaps):
        mock_get_snaps.side_effect = [
            # two snapshots of root volume
            ['snapshot-00000000-0000-0000-0000-000000000000',
             'snapshot-00000000-0000-0000-0000-000000000001']
        ]
        root = rbd_tree.RbdItem('vid')
        root.search_children()
        mock_get_snaps.assert_called_once_with('vid')
        self.assertEqual(len(root.children), 2)
        self.assertEqual(root.children[0].vid, 'vid')
        self.assertEqual(root.children[0].sid,
                         'snapshot-00000000-0000-0000-0000-000000000000')
        self.assertEqual(root.children[1].vid, 'vid')
        self.assertEqual(root.children[1].sid,
                         'snapshot-00000000-0000-0000-0000-000000000001')

    @patch('rbd_tree.rbd_tree.ceph_client.get_snaps')
    def test_search_children_no_children(self, mock_get_snaps):
        mock_get_snaps.side_effect = [[]]
        root = rbd_tree.RbdItem('vid')
        root.search_children()
        mock_get_snaps.assert_called_once_with('vid')
        self.assertEqual(len(root.children), 0)

    @patch('rbd_tree.rbd_tree.ceph_client.get_snaps')
    @patch('rbd_tree.rbd_tree.ceph_client.get_children_vols')
    def test_construct(self, mock_get_children, mock_get_snaps):
        mock_get_snaps.side_effect = [
            # two snapshots of root volume
            ['snapshot-00000000-0000-0000-0000-000000000000',
             'snapshot-00000000-0000-0000-0000-000000000001'],
            # no snapshot of volume-00000000-0000-0000-0000-000000000000
            []
        ]
        mock_get_children.side_effect = [
            # one child volume of the first
            ['volume-00000000-0000-0000-0000-000000000000'],
            # no child volume of the second volume
            []
        ]
        snap_calls = [call('vid'),
                      call('volume-00000000-0000-0000-0000-000000000000'),
                      ]
        children_calls = [
            call('vid', 'snapshot-00000000-0000-0000-0000-000000000000'),
            call('vid', 'snapshot-00000000-0000-0000-0000-000000000001'),
        ]
        root = rbd_tree.RbdItem('vid')
        ShellTree(root)
        self.assertEqual(mock_get_snaps.call_count, 2)
        mock_get_snaps.assert_has_calls(snap_calls)
        self.assertEqual(mock_get_children.call_count, 2)
        mock_get_children.assert_has_calls(children_calls)
        self.assertEqual(len(root.children), 2)
        self.assertEqual(root.children[0].vid, 'vid')
        self.assertEqual(root.children[0].sid,
                         'snapshot-00000000-0000-0000-0000-000000000000')
        self.assertEqual(root.children[1].vid, 'vid')
        self.assertEqual(root.children[1].sid,
                         'snapshot-00000000-0000-0000-0000-000000000001')
        self.assertEqual(len(root.children[0].children), 1)
        self.assertEqual(root.children[0].children[0].vid,
                         'volume-00000000-0000-0000-0000-000000000000')
        self.assertEqual(root.children[0].children[0].sid, None)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
