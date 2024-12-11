from __future__ import annotations


def main():
    disk = read_disk()
    new_partition = reorg_disk(disk)
    print_results(new_partition)


def reorg_disk(disk: list[int]) -> list[tuple[int, int]]:
    result = []
    maxfile = (len(disk) - 1) // 2
    start = 0
    end = maxfile
    moved_end = 0
    while start < end:
        regular = (disk[2 * start], start)
        result.append(regular)
        empty_space = disk[2 * start + 1]
        while empty_space > 0:
            remaining_end = disk[2 * end] - moved_end
            if remaining_end > empty_space:
                # Fill all empty_space with the current end
                move_from_end = (empty_space, end)
                result.append(move_from_end)
                moved_end += empty_space
                empty_space = 0
            else:
                move_from_end = (remaining_end, end)
                result.append(move_from_end)
                empty_space -= remaining_end
                moved_end = 0
                end -= 1
        start += 1
    if start == end:
        result.append((disk[2 * start] - moved_end, start))
    return result


def print_results(new_partition: list[tuple[int, int]]):
    total = 0
    pos = 0
    for size, filenum in new_partition:
        start = pos
        end = pos + size - 1
        gauss = (start + end) * (end - start + 1) // 2
        total += gauss * filenum
        pos += size
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
