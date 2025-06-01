# calculator.py
def calculate_price(weight: float, width: float, height: float, length: float) -> float:
    base = 100
    volume = width * height * length / 1_000_000  # м³
    volume_cost = volume * 20000
    weight_cost = weight * 150
    return round(base + volume_cost + weight_cost, 2)
