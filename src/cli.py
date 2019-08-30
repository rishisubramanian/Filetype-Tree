#!/usr/bin/env python3

import click
from os import walk
from os.path import ismount, getsize, join
from identify.identify import tags_from_path
from collections import defaultdict


@click.command()
@click.option("-x", "--same-filesystem", is_flag=True, help="Same filesystem")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, file_okay=False, dir_okay=True))
def filesystem_tree(same_filesystem, paths):
    if len(paths) == 0:
        paths = ["."]

    type_sizes = defaultdict(int)

    for path in paths:
        for root, dirs, files in walk(path):
            if same_filesystem:
                dirs[:] = [dir for dir in dirs if not ismount(join(root, dir))]
            file_types = [tags_from_path(join(root, f)) for f in files]
            file_sizes = [getsize(join(root, f)) for f in files]

            for filetype, size in zip(file_types, file_sizes):
                type_sizes[filetype] += size

    for filetype, size in type_sizes.items():
        click.echo(f"{filetype}: {size}")


if __name__ == "__main__":
    filesystem_tree()