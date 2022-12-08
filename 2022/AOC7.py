import shutil
from pathlib import Path

root = Path.cwd() / "7_tmp"
root.mkdir()
cwd = root

for line in open("7").readlines():
    match line.split():
        case ["$", "cd", "/"]:
            cwd = root
        case ["$", "cd", ".."]:
            cwd = cwd.parent
        case ["$", "cd", dest]:
            cwd = cwd / dest
        case ["$", "ls"]:
            # Assume anything not preceded by "$" is output from `ls`.
            pass
        case ["dir", name]:
            (cwd / name).mkdir()
        case [size, name]:
            # As cute as it'd be to write loremipsum to the file until
            # it is actually the size listed, i don't trust the input data.
            (cwd / name).write_text(size)

dir_sizes = {
    dir: sum(int(p.read_text()) for p in dir.glob("**/*") if p.is_file())
    for dir in root.glob("**")
}
unused_space = 70_000_000 - dir_sizes[root]

print(f"Part 1: {sum(size for size in dir_sizes.values() if size <= 100_000)}")
print(
    f"Part 2: {min(size for size in dir_sizes.values() if size >= 30_000_000 - unused_space)}"
)

shutil.rmtree(root)
