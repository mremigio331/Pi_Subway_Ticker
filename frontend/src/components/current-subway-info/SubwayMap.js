import React, { useEffect, useRef } from 'react';
import { createRoot } from 'react-dom/client';
import { Button, Container, Header, SpaceBetween } from '@cloudscape-design/components';
import L from 'leaflet';
import selectedMarker from '../../assests/MapMarkers/MTA_Selected.png';
import notSelectedMarker from '../../assests/MapMarkers/MTA_Not_Selected.png';
import { TrainLogos } from '../../utility/SubwayLogos';
import { AllStations } from '../../constants/SubwayStations';
import { forceUpdateCurrentStation } from '../../services/API';
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
        const response = await forceUpdateCurrentStation(station);
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
            currentStation.stop_name === 'Loading' ? 12 : 18,
        );

        L.tileLayer('https://{s}.google.com/vt/lyrs={type}&x={x}&y={y}&z={z}', {
            attribution: 'Map data &copy; <a href="https://www.google.com/maps">Google Maps</a>',
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
            type: 'r',
        }).addTo(newMap);

        const addMarkers = (markersArray, currentStation) => {
            markersArray.forEach((markerData) => {
                const isCurrentCenter =
                    markerData.complexId === currentStation.complex_id &&
                    markerData.stationName === currentStation.stop_name;

                const icon = L.icon({
                    iconUrl: isCurrentCenter ? selectedMarker : notSelectedMarker,
                    iconSize: [45, 45],
                    iconAnchor: [22.5, 45],
                    popupAnchor: [1, -34],
                });

                const marker = L.marker(markerData.coordinates, { icon }).addTo(newMap);
                const popupContainer = document.createElement('div');
                popupContainer.style.display = 'inline-block';
                popupContainer.style.width = '300px';

                const popupRoot = createRoot(popupContainer);
                const popupContent = (
                    <SpaceBetween direction="vertical" size="m">
                        <Header>{markerData.stationName}</Header>
                        <Button onClick={() => handleButtonClick(markerData.fullStationName)}>Change to Station</Button>
                        <SpaceBetween direction="horizontal" size="s">
                            {markerData.trainLines.map((line) => (
                                <img
                                    width={'25'}
                                    height={'25'}
                                    src={TrainLogos[line] || ''}
                                    key={line}
                                    alt={`${line} logo`}
                                />
                            ))}
                        </SpaceBetween>
                    </SpaceBetween>
                );

                popupRoot.render(popupContent);

                marker.bindPopup(popupContainer, {
                    autoClose: true,
                    closeOnClick: true,
                });

                marker.on('popupclose', () => {
                    popupRoot.unmount();
                });
            });
        };

        addMarkers(AllStations, currentStation);
        setMapInitialized(true);
        mapRef.current = newMap;
    };

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
