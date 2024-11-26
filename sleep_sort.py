import asyncio
from typing import List
import sys


async def sleep_sort(nums: List[int] = None):
    async def sort_num(i: int):
        await asyncio.sleep(i / 10000)
        print(i, end=" ")

    print(f"Going to sort {nums}:")
    print("Start")
    await asyncio.gather(*(sort_num(i) for i in nums))
    print("\nEnd")


def _get_params(args):
    if len(args) == 1:
        import random

        len_nums = 1 + int(100 * random.random())
        return [int(1000 * random.random()) for _ in range(len_nums)]
    return [int(i) for i in args[1:]]


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    nums = _get_params(sys.argv)
    loop.run_until_complete(sleep_sort(nums))
