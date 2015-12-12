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
#points = [(37.779779, -122.430325), (37.780715, -122.430494), (37.781661, -122.430562), (37.781845, -122.429042), (37.782316, -122.429137), (37.785588, -122.429761), (37.786498, -122.429948), (37.786714, -122.428356), (37.786935, -122.426719), (37.787875, -122.426913), (37.788341, -122.427006), (37.788781, -122.4271), (37.78899, -122.425461), (37.789954, -122.425634), (37.790185, -122.423998), (37.791087, -122.424168), (37.791969, -122.424358), (37.792165, -122.422766), (37.793069, -122.422827), (37.793944, -122.423008), (37.794818, -122.423179), (37.795758, -122.423347), (37.795985, -122.421792), (37.796233, -122.420169), (37.797128, -122.420333), (37.797246, -122.419515), (37.79735, -122.418718), (37.797559, -122.417049), (37.798512, -122.417248), (37.798961, -122.41734), (37.799417, -122.417433), (37.799541, -122.416565), (37.799634, -122.415784), (37.800561, -122.415964), (37.801035, -122.416054), (37.801192, -122.414955), (37.801646, -122.414974), (37.801702, -122.414516), (37.801813, -122.413685), (37.801925, -122.412892), (37.802165, -122.412932), (37.80286, -122.413054), (37.803786, -122.413252), (37.803833, -122.412888)]
#map = Map(points)

#with open("output.html", "w") as out:
#    print(map, file=out)


