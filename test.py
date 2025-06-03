import time

points = [
    (35.715, 51.41),
    (35.716, 51.411),
    (35.717, 51.412),
    (35.718, 51.413)
]

while True:
    for lat, lon in points:
        with open("location.txt", "w") as f:
            f.write(f"{lat},{lon}")
        time.sleep(1)