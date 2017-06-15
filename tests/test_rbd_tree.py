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
import subprocess
from rbd_tree.ab_tree import ShellTree


class TestRbdTree(unittest.TestCase):

    @patch('rbd_tree.rbd_tree.run_cmd')
    def test_search_children(self, mock_cmd):
        mock_cmd.side_effect = [
            # two snapshots of root volume
            '''
            SNAPID NAME                                             SIZE
            5 snapshot-00000000-0000-0000-0000-000000000000 1024 MB 
            6 snapshot-00000000-0000-0000-0000-000000000001 1024 MB 
            '''
        ]
        cmd_args = ['rbd', '-p', 'pool_name', 'snap', 'ls', 'vid']
        root = rbd_tree.RbdItem('vid', 'pool_name')
        root.search_children()
        mock_cmd.assert_called_once_with(cmd_args)
        self.assertEqual(len(root.children), 2)
        self.assertEqual(root.children[0].vid, 'vid')
        self.assertEqual(root.children[0].sid,
                         'snapshot-00000000-0000-0000-0000-000000000000')
        self.assertEqual(root.children[1].vid, 'vid')
        self.assertEqual(root.children[1].sid,
                         'snapshot-00000000-0000-0000-0000-000000000001')

    @patch('rbd_tree.rbd_tree.run_cmd')
    def test_search_children_no_children(self, mock_cmd):
        mock_cmd.side_effect = ['']
        cmd_args = ['rbd', '-p', 'pool_name', 'snap', 'ls', 'vid']
        root = rbd_tree.RbdItem('vid', 'pool_name')
        root.search_children()
        mock_cmd.assert_called_once_with(cmd_args)
        self.assertEqual(len(root.children), 0)

    @patch('rbd_tree.rbd_tree.run_cmd')
    def test_search_children_no_root(self, mock_cmd):
        cmd_args = ['rbd', '-p', 'pool_name', 'snap', 'ls', 'vid']
        mock_cmd.side_effect = subprocess.CalledProcessError(2, cmd_args)
        root = rbd_tree.RbdItem('vid', 'pool_name')
        self.assertRaises(subprocess.CalledProcessError, root.search_children)

    @patch('rbd_tree.rbd_tree.run_cmd')
    def test_construct(self, mock_cmd):
        mock_cmd.side_effect = [
            # two snapshots of root volume
            '''
            SNAPID NAME                                             SIZE
            5 snapshot-00000000-0000-0000-0000-000000000000 1024 MB 
            6 snapshot-00000000-0000-0000-0000-000000000001 1024 MB 
            ''',
            # one child volume of the first
            'rbd_ssd/volume-00000000-0000-0000-0000-000000000000',
            # no snapshot of volume-00000000-0000-0000-0000-000000000000
            '',
            # no child volume of the second volume
            '']
        calls = [call(['rbd', '-p', 'pool_name', 'snap', 'ls', 'vid']),
                 call(['rbd', '-p', 'pool_name', 'children',
                       'vid@snapshot-00000000-0000-0000-0000-000000000000']),
                 call(['rbd', '-p', 'pool_name', 'snap', 'ls',
                       'volume-00000000-0000-0000-0000-000000000000']),
                 call(['rbd', '-p', 'pool_name', 'children',
                       'vid@snapshot-00000000-0000-0000-0000-000000000001']),
                 ]
        root = rbd_tree.RbdItem('vid', 'pool_name')
        ShellTree(root)
        self.assertEqual(mock_cmd.call_count, 4)
        mock_cmd.assert_has_calls(calls)
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
