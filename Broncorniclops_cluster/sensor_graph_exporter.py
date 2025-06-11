import csv
import os
from datetime import datetime
from kivy.graphics import Fbo, ClearBuffers, ClearColor, Scale, Translate
from kivy.core.image import Image as CoreImage

EXPORT_DIR = "/home/pi/digital_cluster/exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

class SensorGraphExporter:
    def __init__(self, panel):
        self.panel = panel  # the sensor graph panel instance

    def export_csv(self):
        filename = f"graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        path = os.path.join(EXPORT_DIR, filename)
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Time", "Sensor", "Value"])
            for name, points in self.panel.series.items():
                for t, v in points:
                    writer.writerow([t, name, v])
        return path

    def export_image(self):
        filename = f"graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join(EXPORT_DIR, filename)

        # Render widget to texture
        fbo = Fbo(size=self.panel.size)
        with fbo:
            ClearColor(1, 1, 1, 1)
            ClearBuffers()
            Scale(1, -1, 1)
            Translate(0, -self.panel.height, 0)
            self.panel.canvas.export_to_png(path)
        return path