import React, { useState, useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import "../src/App.css";

mapboxgl.accessToken =
  "pk.eyJ1IjoidHVuZ2J1aSIsImEiOiJjbHR2NG1kYngxZmhxMnFvYjNybHIwdHd3In0.GWxkr4OrFlLAtcZCGBc9_Q";

interface MapboxProps {
    coordinates: number[][]
}

const MapboxComponent = ({ coordinates }: MapboxProps) => {
  const mapContainerRef: any = useRef(null);
  const map: any = useRef(null);

  // initialization with Aalto University coordinates
  const [lng] = useState(coordinates[0][0]);
  const [lat] = useState(coordinates[0][1]);
  const [zoom] = useState(15);

  useEffect(() => {
    map.current = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: "mapbox://styles/mapbox/streets-v11",
      center: [lng, lat],
      zoom: zoom,
    });

    map.current.addControl(new mapboxgl.NavigationControl(), "top-right");

    map.current.on("load", () => {
      map.current.resize();

      map.current.addSource("hiking", {
        type: "geojson",
        data: {
          type: "Feature",
          properties: {},
          geometry: {
            type: "LineString",
            coordinates,
          },
        },
      });
      map.current.addLayer({
        id: 'hiking-layer',
        type: 'line',
        source: 'hiking',
        paint: {
            'line-color': 'red',
            'line-width': 3
        },
        layout: {
          'line-join': 'round',
          'line-cap': 'round'
        },
      });
    });

    return () => map.current.remove();
  }, [lng, lat, zoom, coordinates]);

  return <div className="map-container" ref={mapContainerRef} />;
};

export default MapboxComponent;
