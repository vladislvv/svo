def calculate_price(weight, width, height, length):
    base = 100
    volume = width * height * length / 1_000_000
    return round(base + (volume * 20000) + (weight * 150), 2)
