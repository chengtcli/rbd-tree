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


class TreeItem(object):
    '''
    To present the tree node
    '''

    def __init__(self, name):
        '''
        :param name: the name to present the node
        :param children: the children of the node
        '''
        self.name = name
        self.children = []

    def search_children(self):
        '''The method to find children'''
        raise NotImplementedError('this function is not implemented')

    def __str__(self):
        return self.name


class ShellTree(object):
    def __init__(self, root_item):
        self.root = root_item
        self._constructe([self.root])

    def _constructe(self, items):
        '''Construct the tree from root node recursively'''
        for item in items:
            if not item:
                return
            item.search_children()
            if item.children:
                self._constructe(item.children)

    def draw(self):
        '''Draw the tree in command line'''
        self._draw_item(self.root, [])

    def _draw_item(self, item, prelevels):
        if not item:
            print item
            return
        for i, l in enumerate(prelevels):
            if i >= len(prelevels) - 1:
                print "├────" if l else "└────",
            else:
                print "{}    ".format("│" if l else " "),
        print item
        for i, child in enumerate(item.children):
            self._draw_item(child, prelevels +
                            [True if i < len(item.children) - 1 else False])
