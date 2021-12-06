#!/usr/bin/env python3

input_filename = "input.txt"
bits = 12

def parse_file(filename):
    reports = []
    with open(filename, 'r') as fp:
        for line in fp.readlines():
            report = line.strip("\n")
            reports.append(report)
    return reports

def calc_gamma(diagnostics):
    return int(''.join(most_common_bits(diagnostics)), 2)

# For a list of binary readings, calc the most common bits in each position.
# If 0 and 1 appear equally often in a position, set that position to 1.
# for each position, increment for a 1, decrement for a 0, if result is
# positive, there are more ones; if negative, more zeroes
def most_common_bits(diagnostics):
    common_bits = [0 for i in range(bits)]
    for report in diagnostics:
        for i in range(bits):
            common_bits[i] += 1 if report[i] == "1" else -1

    for i in range(bits):
        common_bits[i] = str(1) if common_bits[i] >= 0 else str(0)
    
    return common_bits

# iteratively filter a list of readings based on whether they
# match or differ from the most common bit pattern in the filtered
# list of readings.
def calc_match(diagnostics, most_common=True):
    filtered = diagnostics[:]
    for i in range(bits):
        mcb = most_common_bits(filtered)
        match = []
        differ = []
        for report in filtered:
            if report[i] == mcb[i] :
                match.append(report)
            else:
                differ.append(report)

        filtered = pick_filtered(match, differ, mcb[i], most_common)

        if len(filtered) == 1:
            return int(''.join(filtered[0]), 2)

    # if we didn't find a reading, we have a data problem
    return 0

# given lists of matching and differing readings on a specific bit
# return either the matching or differing list based on which readings
# we're trying to filter down.
def pick_filtered(matched, differed, matching_bit, most_common):
        if len(matched) == len(differed) and matching_bit == "0":
            return differed if most_common else matched

        return matched if most_common else differed

# o2 iteratively matches against _most_ common bits in the readings
def calc_o2(diagnostics):
    return calc_match(diagnostics, most_common=True)

# co2 iteratively matches against _least_ common bits in the readings
def calc_co2(diagnostics):
    return calc_match(diagnostics, most_common=False)

# main section - getting complex enough to use a bit of OO structure

diagnostics = parse_file(input_filename)

# part 1 - epsilon is all-ones value minus calculated gamma
max_power_reading = pow(2, bits) - 1
gamma = calc_gamma(diagnostics)
epsilon = max_power_reading - gamma
print(f'power consumption: {gamma * epsilon}. Gamma: {gamma}, Epsilon: {epsilon}')

# part 2 - iteratively match the readings to the most or least common bits
o2 = calc_o2(diagnostics)
co2 = calc_co2(diagnostics)
print(f'life support rating: {o2 * co2}. O2: {o2}, CO2: {co2}')
