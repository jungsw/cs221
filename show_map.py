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
points = [(37.783098, -122.419225), (37.783592, -122.419301), (37.784054, -122.419375), (37.784518, -122.419472), (37.784732, -122.417835), (37.785184, -122.417931), (37.785403, -122.41628), (37.785469, -122.41572), (37.785555, -122.415066), (37.785609, -122.414633), (37.785819, -122.412996), (37.785923, -122.412159), (37.78603, -122.411362), (37.786948, -122.411538)]
map = Map(points)

with open("output.html", "w") as out:
    print(map, file=out)


