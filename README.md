# rbd-tree

rbd-tree is used to print the tree struct of rbd volumes and snapshots.
It shows the relationship of volumes and snapshots

## Installation

```bash
git clone git://github.com/chengtcli/rbd-tree.git && cd rbd-tree
python setup.py install
```

## Uninstallation

pip uninstall rbd-tree

## Usage

rbd-tree should be run on nodes where `ceph` command works.
It uses librados/librbd to communicate with ceph cluster

```
root@ceph1:~# ceph health
root@ceph1:~# rbd-tree -h
usage: rbd-tree [-h] [--verbose] [--user USER] [--cluster CLUSTER]
                [--conffile CONFFILE] [--parents] [--pool POOL]
                [vol]

Print rbd volumes/snapshot in tree

positional arguments:
  vol                   the volume id or rbd image id, print the all volumes
                        if vol is not specified (default: )

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v
  --user USER, -u USER  the ceph user (default: admin)
  --cluster CLUSTER, -c CLUSTER
                        the ceph cluster name (default: ceph)
  --conffile CONFFILE, -C CONFFILE
                        the ceph config file (default: /etc/ceph/ceph.conf)
  --parents, -P         show parents or not (default: False)
  --pool POOL, -p POOL  the pool name (default: rbd_ssd)
```

## Example

```
root@ceph1:~# rbd-tree -p rbd_ssd
ROOT
├──── volume-fcca95bd-8f08-405e-8fc3-0bc9ea66ad54
│     └──── snapshot-efe1cee8-4391-4da8-89ce-52cce093a4a9
│           └──── volume-82f84010-71ea-43f7-a690-95299e5730ea
│                 └──── volume-e81c8b94-c546-4e01-a1e1-7f6077e711db.clone_snap
│                       └──── volume-e81c8b94-c546-4e01-a1e1-7f6077e711db
├──── 252b5916-5da6-493a-b423-451f92ef4ed9
│     └──── snap
└──── volume-05d66570-290a-4642-b0d1-a93c67119e0b

root@ceph1:~# rbd-tree -p rbd_ssd volume-82f84010-71ea-43f7-a690-95299e5730ea
volume-82f84010-71ea-43f7-a690-95299e5730ea
└──── volume-e81c8b94-c546-4e01-a1e1-7f6077e711db.clone_snap
      └──── volume-e81c8b94-c546-4e01-a1e1-7f6077e711db

root@ceph1:~/rbd-tree# rbd-tree -P -p rbd_ssd volume-82f84010-71ea-43f7-a690-95299e5730ea
volume-fcca95bd-8f08-405e-8fc3-0bc9ea66ad54
└──── snapshot-efe1cee8-4391-4da8-89ce-52cce093a4a9
      └──── volume-82f84010-71ea-43f7-a690-95299e5730ea
            └──── volume-e81c8b94-c546-4e01-a1e1-7f6077e711db.clone_snap
                  └──── volume-e81c8b94-c546-4e01-a1e1-7f6077e711db
```
