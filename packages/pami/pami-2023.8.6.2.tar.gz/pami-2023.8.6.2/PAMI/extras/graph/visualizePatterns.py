import plotly.express as px
import pandas as pd
import sys

class visualizePatterns():
    
    def __init__(self, file, topk):
        self.file = file
        self.topk = topk

    def visualize(self,markerSize=20,zoom=3,width=1500, height=1000):
        """
        Visualize points produced by pattern miner.
    
        :param file: String for file name
        :param top: visualize topk patterns
        :param markerSize: int
        :param zoom: int
        :param file: int
        :param file: int
        """
    
        long = []
        lat = []
        name = []
        color = []
        R = G = B = 0
    
        lines = {}
        with open(self.file, "r") as f:
            for line in f:
                lines[line] = len(line)
            
        lines = list(dict(sorted(lines.items(), key=lambda x:x[1])[-self.topk:]).keys())

        start = 1

        print("Number \t Pattern")
        for line in lines:

            start += 1
            if start % 3 == 0:
                R += 20
            if start % 3 == 1:
                G += 20
            if start % 3 == 2:
                B += 20
            if R > 255:
                R = 0
            if G > 255:
                G = 0
            if B > 255:
                B = 0
            RHex = hex(R)[2:]
            GHex = hex(G)[2:]
            BHex = hex(B)[2:]

            line = line.split(":")
            freq = line[-1]
            freq = "Frequency: " + freq.strip()
            line = line[:-1]
            print(str(start) + "\t" + line[0])
            points = line[0].split("\t")
            points = [x for x in points if x != ""]
            points = [x.strip("Point()") for x in points]
            for i in range(len(points)):
                temp = points[i].split()
                lat.append(float(temp[0]))
                long.append(float(temp[1]))
                name.append(freq)
                color.append("#" + RHex + GHex + BHex)
        df = pd.DataFrame({"lon": long, "lat": lat, "freq": name, "col": color})
    
        fig = px.scatter_mapbox(df, lat="lon", lon="lat", hover_name="freq", color="col", zoom=zoom, width=width, height=height)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_traces({'marker': {'size': markerSize}})
        fig.show()
        
if __name__ == "__main__":
    _ap = str()
    _ap = visualizePatterns(sys.argv[1], sys.argv[2])
    _ap.visualize()
