import json
import sys
from typing import Any
from typing import Dict
from typing import List
from typing import MutableSet


def main(filename: str) -> int:
    """Super powerful doc string"""
    if not filename:
        return 1

    with open(filename, "r") as in_file:
        struct = json.load(in_file)

    tree = KeyTree(struct)
    with open("out.txt", "w") as out_file:
        out_file.write("\n".join(tree.tree))

    return 0


class KeyTree:

    INDENT = "    "

    def __init__(self, struct: Dict[str, Any]) -> None:
        self.tree: List[str] = []
        self.treeread(struct)

    def treeread(self, struct: Dict[str, Any], indent: int = 0) -> None:
        """Super powerful doc string"""
        for key, value in struct.items():
            self.tree.append(f"{self.INDENT * indent}{key}: {type(value).__name__}")
            if isinstance(value, dict):
                self.treeread(value, indent + 1)
            if isinstance(value, list):
                self.treeread_list(value, indent + 1)

    def treeread_list(self, values: List[Any], indent: int = 0) -> None:
        """Super powerful doc string"""
        contains: MutableSet[str] = set()
        for value in values:
            contains.add(type(value).__name__)

        for typename in contains:
            self.tree.append(f"{self.INDENT * indent}> {typename}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = ""

    sys.exit(main(filename))
