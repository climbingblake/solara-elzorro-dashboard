import math

class Tank:
    def __init__(self, dia, height):
        self.dia = dia
        self.height = height

    def tank_gallons_full(self):
        return round((math.pi * (float(self.dia) / 2) ** 2 * float(self.height) / 3785.41),1)


    def gallons_remaining(self, distance):
        if self.dia is None or self.height is None:
            raise Exception("Tank dimensions not set")
            return

        remaining_cm = float(self.dia) - distance
        gallons = (math.pi * (float(self.dia) / 2) ** 2 * remaining_cm / 3785.41)
        return round(gallons)


    def percentage_remaining(self, centimeters):
        return 100 - round((centimeters / float(self.height) * 100))
