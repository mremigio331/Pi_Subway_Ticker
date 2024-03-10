import React, { useEffect } from "react";
import L from "leaflet";

import {AllStations} from './SubwayStations'

export const SubwayMap = () => {
  useEffect(() => {
    // Create a map instance
    const map = L.map("map").setView([40.827994, -73.925831], 13);

    // Add a tile layer
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution:
        'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    }).addTo(map);

    const addMarkers = (markersArray) => {
      markersArray.forEach(markerData => {
        const marker = L.marker(markerData.coordinates).addTo(map);
        marker.bindPopup(markerData.popupContent);
      });
    };

    // Call the addMarkers function with the array of marker data
    addMarkers(AllStations);
  }, []);

  return <div id="map" style={{ width: "100%", height: "400px" }} />;
};
