import os
import requests
from tqdm import tqdm
import math

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

min_lat, max_lat = 35.68, 35.81
min_lon, max_lon = 51.24, 51.53
zoom_levels = [18]

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
    return xtile, ytile

tile_server = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"

for zoom in zoom_levels:
    x_start, y_start = deg2num(max_lat, min_lon, zoom)
    x_end, y_end = deg2num(min_lat, max_lon, zoom)

    print(f"⬇ Downloading zoom {zoom}...")

    for x in tqdm(range(x_start, x_end + 1)):
        for y in range(y_start, y_end + 1):
            url = tile_server.format(z=zoom, x=x, y=y)
            folder = f"tiles/{zoom}/{x}"
            os.makedirs(folder, exist_ok=True)
            filepath = f"{folder}/{y}.png"
            if not os.path.exists(filepath):
                try:
                    r = requests.get(url, headers=headers, timeout=10)
                    if r.status_code == 200:
                        with open(filepath, "wb") as f:
                            f.write(r.content)
                    else:
                        print(f"⚠️ tile missed: {r.status_code} @ {url}")
                except Exception as e:
                    print(f"failed to download {url} -- {e}")