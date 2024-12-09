disk_map = list(map(int, open("9").read()))


def disk_pos_to_file_id(pos: int) -> int:
    return pos // 2


def defrag_disk(disk_map: list[int], whole_files: bool) -> int:
    disk_map_f = disk_map.copy()  # Track uncounted file positions
    disk_map_c = disk_map.copy()  # Track uncounted disk positions
    start = 0
    end = len(disk_map) - 1
    checksum = 0
    mem_pos = 0
    while start <= end:
        # Even positions: count directly (UNLESS a file has moved _out_ of this position!)
        if start % 2 == 0:
            file_id = disk_pos_to_file_id(start)
            while disk_map_c[start] > 0:
                if disk_map_f[start] > 0:
                    checksum += file_id * mem_pos
                    disk_map_f[start] -= 1
                mem_pos += 1
                disk_map_c[start] -= 1
        else:
            # Odd positions: first determine how to fill the space, then count.
            search = end
            while disk_map_c[start] > 0:
                if search > start:
                    if (
                        disk_map_f[search] > disk_map_f[start] and whole_files
                    ) or disk_map_f[search] == 0:
                        search -= 2
                    else:
                        file_id = disk_pos_to_file_id(search)
                        checksum += file_id * mem_pos
                        mem_pos += 1
                        disk_map_f[start] -= 1
                        disk_map_c[start] -= 1
                        disk_map_f[search] -= 1
                else:
                    mem_pos += 1
                    disk_map_c[start] -= 1
            # If not moving whole files, there's no need to re-scan from the end.
            if not whole_files:
                end = search
        start += 1
    return checksum


print(f"Part 1: {defrag_disk(disk_map, False)}")
print(f"Part 2: {defrag_disk(disk_map, True)}")
