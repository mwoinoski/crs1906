# pip install rich

from rich.tree import Tree
from rich import print as rprint


tree = Tree('Family Tree')
tree.add('Mom')
tree.add('Dad')
tree.add('Brother').add('Wife')
tree.add('[red]Sister').add('[green]Husband').add('[blue]Son')

rprint(tree)