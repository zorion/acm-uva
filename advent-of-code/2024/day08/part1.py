from __future__ import annotations

type Pos = tuple[int, int]
type AntennaMap = dict[str, list[Pos]]


def main():
    antennas, maxi, maxj = read_antennamap()
    antinodes = get_antinodes(antennas, maxi, maxj)
    print_results(antinodes)


def get_antinodes(antennas: AntennaMap, maxi: int, maxj: int) -> set[Pos]:
    result = set()
    for val, positions in antennas.items():
        antinodes = _get_antinodes_aux(positions, maxi, maxj)
        result.update(antinodes)
    return result


def _get_antinodes_aux(positions: list[Pos], maxi: int, maxj: int) -> set[Pos]:
    result = set()
    for i, pos1 in enumerate(positions):
        for j, pos2 in enumerate(positions):
            if i == j:
                continue
            newpos = (
                2 * pos1[0] - pos2[0],
                2 * pos1[1] - pos2[1],
            )
            if _is_valid(newpos, maxi, maxj):
                result.add(newpos)
    return result


def _is_valid(pos: Pos, maxi: int, maxj: int) -> bool:
    return 0 <= pos[0] < maxi and 0 <= pos[1] < maxj


def print_results(antinodes: set[Pos]):
    print("Result:", len(antinodes))


def read_antennamap() -> tuple[AntennaMap, int, int]:
    rawmap: list[str] = []
    finished = False
    while not finished:
        try:
            line = input()
        except Exception:
            break
        if line == "":
            finished = True
        else:
            rawmap.append(line)
    return _parse_map(rawmap), len(rawmap), len(rawmap[0])


def _parse_map(rawmap: list[str]) -> AntennaMap:
    result = {}
    for i, line in enumerate(rawmap):
        for j, val in enumerate(line):
            if val != ".":
                if val not in result:
                    result[val] = []
                result[val].append((i, j))
    return result


if __name__ == "__main__":
    main()
