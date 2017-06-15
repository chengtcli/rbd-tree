# rbd-tree

rbd-tree is used to print the tree struct of rbd volumes and snapshots.
It shows the relationship of volumes and snapshots

## Installation

pip install -e git://github.com/chengtcli/rbd-tree.git@master#egg=rbd-tree

## Usage

rbd-tree should be run on nodes where `ceph` command works

```
root@ceph1:~# ceph health
root@ceph1:~# rbd-tree -h
usage: rbd-tree [-h] [--verbose] [pool] vol

Print rbd volumes/snapshot in tree

positional arguments:
  pool           the pool name, default: rbd_ssd
  vol            the volume id or rbd image id

optional arguments:
  -h, --help     show this help message and exit
  --verbose, -v
```

## Example

```
root@ceph1:~# rbd-tree rbd_ssd volume-6b139b7a-c93a-4007-833c-3475085b833b
volume-6b139b7a-c93a-4007-833c-3475085b833b
├──── snapshot-b0e96680-35f5-42d1-ae80-441869001ab5
│     └──── volume-9955b199-afff-4ccc-bed7-9022bf15f99c
└──── snapshot-8360d9f0-250f-44cd-82c3-93687a7af0c7
```
