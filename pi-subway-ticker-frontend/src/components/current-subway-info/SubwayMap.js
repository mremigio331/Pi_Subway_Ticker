import React, { useEffect, useRef } from 'react';
import ReactDOM from 'react-dom';
import { Button, Container, Header, SpaceBetween } from '@cloudscape-design/components';
import L from 'leaflet';
import blueMarker from '../../assests/MapMarkers/blue-marker.png';
import greenMarker from '../../assests/MapMarkers/green-marker.png';
import { TrainLogos } from './SubwayLogos';
import { AllStations } from './SubwayStations';
import { updateCurrentStation } from '../../services/API';
import { getNotificationsContext, NotificationConstants } from '../../services/Notifications';
import { v4 as uuidv4 } from 'uuid';

export const SubwayMap = ({ currentStation, currentCenterMap, mapInitialized, setMapInitialized }) => {
    const { dismissNotification, pushNotification, modifyNotificationContent } = getNotificationsContext();

    const mapRef = useRef(null);

    const handleButtonClick = async (station) => {
        const message_id = uuidv4();
        const message = {
            content: `Changing Station to ${station}`,
            type: NotificationConstants.INFO,
            id: message_id,
            onDismiss: () => dismissNotification(message_id),
            dismissible: false,
            dismissLabel: 'Dismiss',
            loading: true,
        };
        pushNotification(message);
        const response = await updateCurrentStation(station);
        console.log(response);
        if (response.status === 200 || response.status === 204) {
            message.content = response.data;
            message.type = NotificationConstants.SUCCESS;
            message.dismissible = true;
            message.loading = false;
            modifyNotificationContent(message_id, message);
        } else {
            message.content = `Failed to change station: ${response.error}`;
            message.type = NotificationConstants.ERROR;
            message.dismissible = true;
            message.loading = false;
            modifyNotificationContent(message_id, message);
        }
    };

    const initializeMap = () => {
        if (mapRef.current) {
            mapRef.current.remove();
        }

        const newMap = L.map('map').setView(
            [currentCenterMap.lat, currentCenterMap.lon],
            currentStation == 'Loading' ? 12 : 18,
        );

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
        }).addTo(newMap);

        const addMarkers = (markersArray, currentStation) => {
            markersArray.forEach((markerData) => {
                const isCurrentCenter = markerData.stationName == currentStation;

                const icon = L.icon({
                    iconUrl: isCurrentCenter ? blueMarker : greenMarker,
                    iconSize: [25, 41],
                    iconAnchor: [12, 41],
                    popupAnchor: [1, -34],
                });

                const marker = L.marker(markerData.coordinates, { icon }).addTo(newMap);

                // Create a container element for the popup content
                const popupContainer = document.createElement('div');
                popupContainer.style.display = 'inline-block'; // Set display to inline-block

                // Measure the width of the header after it has been rendered
                const headerWidth = ReactDOM.findDOMNode(headerRef.current)?.offsetWidth;
                if (headerWidth) {
                    popupContainer.style.width = `300px`; // Set width to the measured header width
                } else {
                    popupContainer.style.width = '300px'; // Set width to auto as fallback
                }

                const popupContent = (
                    <SpaceBetween direction="vertical" size="m">
                        <Header ref={headerRef}>{markerData.stationName}</Header>
                        <Button onClick={() => handleButtonClick(markerData.fullStationName)}>Change to Station</Button>
                        <SpaceBetween direction="horizontal" size="s">
                            {markerData.trainLines.map((line, index) => (
                                <img
                                    width={'25'}
                                    height={'25'}
                                    src={TrainLogos[`${line}`] || ''}
                                    key={line} // Ensure each image has a unique key
                                    alt={`${line} logo`}
                                />
                            ))}
                        </SpaceBetween>
                    </SpaceBetween>
                );

                // Render the JSX content to the popup container
                ReactDOM.render(popupContent, popupContainer);

                // Bind the popup using the container element
                marker.bindPopup(popupContainer);
            });
        };

        addMarkers(AllStations, currentStation);

        setMapInitialized(true);
        mapRef.current = newMap;
    };

    const headerRef = useRef(null); // Reference for the header element

    useEffect(() => {
        if (!mapInitialized) {
            initializeMap();
        }
    }, [mapInitialized]);

    useEffect(() => {
        return () => {
            if (mapRef.current) {
                mapRef.current.remove();
            }
        };
    }, []);

    return <div id="map" style={{ width: '100%', height: '800px' }} />;
};

export default SubwayMap;
