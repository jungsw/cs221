from __future__ import print_function

class Map(object):
    def __init__(self, pts):
        if len(pts) > 0:
            self._points = pts
        else:
            self._points = []
    def add_point(self, coordinates):
        self._points.append(coordinates)
    def __str__(self):
        centerLat = sum(( x[0] for x in self._points )) / len(self._points)
        centerLon = sum(( x[1] for x in self._points )) / len(self._points)
        markersCode = "\n".join(
            [ """new google.maps.Marker({{
                position: new google.maps.LatLng({lat}, {lon}),
                map: map
                }});""".format(lat=x[0], lon=x[1]) for x in self._points
            ])
        return """
            <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false"></script>
            <div id="map-canvas" style="height: 100%; width: 100%"></div>
            <script type="text/javascript">
                var map;
                function show_map() {{
                    map = new google.maps.Map(document.getElementById("map-canvas"), {{
                        zoom: 17,
                        center: new google.maps.LatLng({centerLat}, {centerLon})
                    }});
                    {markersCode}
                }}
                google.maps.event.addDomListener(window, 'load', show_map);
            </script>
        """.format(centerLat=centerLat, centerLon=centerLon,
                   markersCode=markersCode)


###### Main
points = [(37.783098, -122.419225), (37.782916, -122.420759), (37.783422, -122.420857), (37.784315, -122.42104), (37.785255, -122.421384), (37.785038, -122.422936), (37.785486, -122.423043), (37.785699, -122.421469), (37.785929, -122.419752), (37.786119, -122.418118), (37.786337, -122.416476), (37.786543, -122.414801), (37.78675, -122.413173), (37.786854, -122.412357), (37.786948, -122.411538)]
map = Map(points)

with open("output.html", "w") as out:
    print(map, file=out)


