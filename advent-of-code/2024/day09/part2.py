from __future__ import annotations


def main():
    disk = read_disk()
    new_partition = reorg_disk(disk)
    print_results(new_partition)


def reorg_disk(disk: list[int]) -> dict[int, tuple[int, int]]:
    result = {}
    empty_blocks = []
    maxfile = (len(disk) - 1) // 2
    start = 0
    position = 0
    while start <= maxfile:
        regular_size = disk[2 * start]
        result[start] = (regular_size, position)
        position += regular_size
        if 2 * start + 1 < len(disk):
            empty_space = disk[2 * start + 1]
            block = (empty_space, position)
            empty_blocks.append(block)
            position += empty_space
        start += 1
    for filenum in reversed(result.keys()):
        file_space, file_pos = result[filenum]
        for i, block in enumerate(empty_blocks):
            space, pos = block
            if pos > file_pos:
                continue
            if space < file_space:
                continue
            # the empty block has a better slot and some empty space
            result[filenum] = (file_space, pos)
            empty_blocks[i] = (space - file_space, pos + file_space)
            break  # We already placed the file

    return result


def print_results(new_partition: dict[int, tuple[int, int]]):
    total = 0
    for filenum, data in new_partition.items():
        size, start = data
        end = start + size - 1
        gauss = (start + end) * (end - start + 1) // 2
        total += gauss * filenum
    print("Result:", total)


def read_disk() -> list[int]:
    disk = []
    finished = False
    while not finished:
        try:
            line = input()
        except Exception:
            break
        if line == "":
            finished = True
        else:
            for ch in line:
                disk.append(int(ch))
    return disk


if __name__ == "__main__":
    main()
