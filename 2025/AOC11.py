from functools import cache

device_outputs = {
    line.split(": ")[0]: line.split(": ")[1].split(" ")
    for line in open("11").read().splitlines()
}


@cache
def count_paths(device_name: str, dac_reqd: bool, fft_reqd: bool) -> int:
    if device_name == "out":
        return 0 if dac_reqd or fft_reqd else 1
    if device_name == "dac":
        dac_reqd = False
    if device_name == "fft":
        fft_reqd = False
    if len(device_outputs[device_name]) == 0:
        return 0
    return sum(
        count_paths(output, dac_reqd, fft_reqd)
        for output in device_outputs[device_name]
    )


print(f"Part 1: {count_paths("you", dac_reqd=False, fft_reqd=False)}")
print(f"Part 1: {count_paths("svr", dac_reqd=True, fft_reqd=True)}")
