#!/usr/bin/env python3

depths = [int(x) for x in open('input.txt')]

depth_count = 0
for i in range(len(depths)):
	if (i >= 1) and (depths[i] > depths[i-1]):
		depth_count += 1

print(f'{depth_count} increasing depths')

window_count = 0
for i in range(len(depths)):
        if (i >= 3) and (depths[i] > depths[i-3]):
                window_count += 1

print(f'{window_count} increasing depth windows')
