import noise #Import the perlin noise library

array = []
for x in range(50):
    height = int(noise.pnoise1(x * 0.1, base = 6) * 8)
    if height < 0:
        height *= -1
    height *= 32
    array.append(height)

print(array)
