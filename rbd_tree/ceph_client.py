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

try:
    import rados
    import rbd
except ImportError:
    rados = None
    rbd = None


class RadosClient:
    def __enter__(self):
        self.client = rados.Rados(rados_id=RadosClient.user,
                                  clustername=RadosClient.cluster,
                                  conffile=RadosClient.conffile)
        self.client.connect()
        self.ioctx = self.client.open_ioctx(RadosClient.pool)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ioctx.close()
        self.client.shutdown()

    @classmethod
    def initialize(cls, pool, conffile='/etc/ceph/ceph.conf',
                   user='admin', cluster='ceph'):
        cls.pool = pool
        cls.conffile = conffile
        cls.cluster = cluster
        cls.user = user
        if user.startswith('client.'):
            cls.user = cls.user.replace('client.', '')


ioctx = None


def get_root(vol, passed_vols=set()):
    '''Get the root volumes those don't have parent'''
    volq = [vol]
    while volq:
        current_vol = volq.pop()
        passed_vols.add(current_vol)
        with rbd.Image(ioctx, current_vol) as image:
            try:
                _pool, _vol, _snap = image.parent_info()
            except rbd.ImageNotFound:
                return current_vol
            volq.append(_vol)


def get_root_vols():
    '''Get all the root volumes'''
    passed_vols = set()
    root_vols = set()
    vols = rbd.RBD().list(ioctx)
    for vol in vols:
        if vol not in passed_vols:
            root_vol = get_root(vol, passed_vols)
            root_vols.add(root_vol)
    return root_vols


def get_snaps(vol):
    '''Get all snapshots of the volume'''
    with rbd.Image(ioctx, vol) as image:
        snaps = image.list_snaps()
    return [snap['name'] for snap in snaps]


def get_children_vols(vol, snap):
    '''Get the children volumes of the snapshot'''
    with rbd.Image(ioctx, vol) as image:
        image.set_snap(snap)
        children = image.list_children()
    return [child[1] for child in children]
