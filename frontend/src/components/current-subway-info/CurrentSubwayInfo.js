import React, { useEffect } from 'react';
import { Button, Container, Grid, Header, SpaceBetween } from '@cloudscape-design/components';
import { useQuery } from '@tanstack/react-query';

import { SubwayCards } from './SubwayCards';
import { SubwayMap } from './SubwayMap';
import { getNextFourTrains } from '../../services/API';
import { TrainLogos } from '../../utility/SubwayLogos';
import { getRandomTrainLogos } from '../loading/TrainsLoading';
import { useApiCheck, INCREMENT_RETRIES, RESET_RETRIES } from '../../providers/APICheckProvider';

const LOADING_INFO = {
    timestamp: 'Loading',
    loading: false,
    current_station: { stop_name: 'Loading', train_lines: [] },
    next_four: [
        {
            train: '',
            train_time: '',
            train_direction: 'Loading...',
        },
        {
            train: '',
            train_time: '',
            train_direction: 'Loading...',
        },
        {
            train: '',
            train_time: '',
            train_direction: 'Loading...',
        },
        {
            train: '',
            train_time: '',
            train_direction: 'Loading...',
        },
    ],
};

export const CurrentSubwayInfo = () => {
    const [loadingTrains, setLoadingTrains] = React.useState([]);
    const { apiCheckState, dispatch } = useApiCheck(); // Accessing API check state and dispatch function
    const [currentCenterMap, setCurrentCenterMap] = React.useState({ lat: 40.7831, lon: -73.9712 });
    const [mapInitialized, setMapInitialized] = React.useState(false);

    const isMobileDevice = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    const {
        data: trainItems,
        isLoading,
        isError,
        error,
    } = useQuery({
        queryKey: ['getNextFourTrains'],
        queryFn: getNextFourTrains,
        onSuccess: () => dispatch({ type: RESET_RETRIES }),
        onError: () => dispatch({ type: INCREMENT_RETRIES }),
        retry: 10,
        retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
        refetchInterval: apiCheckState.apiRetries < 10 ? 6000 : false,
        initialData: LOADING_INFO,
    });
    console.log(trainItems);

    useEffect(() => {
        const intervalId = setInterval(() => {
            const randomLogos = getRandomTrainLogos();
            setLoadingTrains(randomLogos);
        }, 1000);

        return () => clearInterval(intervalId);
    }, []);

    React.useMemo(() => {
        trainItems.current_station.stop_lat != undefined &&
            setCurrentCenterMap({ lat: trainItems.current_station.stop_lat, lon: trainItems.current_station.stop_lon });
    }, [trainItems.current_station]);

    return isMobileDevice ? (
        <SpaceBetween direction="vertical" size="m">
            <Container
                header={
                    <Header
                        variant="h2"
                        actions={
                            <Button
                                disabled={trainItems.current_station.stop_name == 'Loading' ? true : false}
                                onClick={() => setMapInitialized(false)}
                            >
                                Center Map
                            </Button>
                            
                        }
                    >
                        {trainItems.current_station.stop_name || 'Loading'}
                    </Header>
                }
            >
                <SpaceBetween direction="vertical" size="l">
                    <SpaceBetween direction="horizontal" size="m">
                        {trainItems.current_station.train_lines.map((train) => (
                            <img
                                width={isMobileDevice ? '15' : '25'}
                                height={isMobileDevice ? '15' : '25'}
                                src={TrainLogos[`${train}`] || ''}
                                key={train}
                                alt={`${train} logo`}
                            />
                        ))}
                    </SpaceBetween>
                </SpaceBetween>
            </Container>
            {trainItems.next_four.some((train) => train.train_direction === 'Loading...') ? (
                <Container>
                    <SpaceBetween direction="horizontal" size="m">
                        {loadingTrains.map(
                            (
                                train,
                                index, // Add key prop to each image
                            ) => (
                                <img
                                    width={isMobileDevice ? '15' : '25'}
                                    height={isMobileDevice ? '15' : '25'}
                                    src={train || ''}
                                    key={index} // Use index as key
                                    alt={`Loading train ${index}`}
                                />
                            ),
                        )}
                    </SpaceBetween>
                </Container>
            ) : (
                <SubwayCards trainItems={trainItems.next_four} isMobileDevice={isMobileDevice} />
            )}
            <SubwayMap
                currentStation={trainItems.current_station}
                currentCenterMap={currentCenterMap}
                mapInitialized={mapInitialized}
                setMapInitialized={setMapInitialized}
            />
        </SpaceBetween>
    ) : (
        <Grid gridDefinition={[{ colspan: 3 }, { colspan: 9 }]}>
            <SpaceBetween direction="vertical" size="m">
                <Container
                    header={
                        <Header
                            variant="h2"
                            actions={
                                <Button
                                    disabled={trainItems.current_station.stop_name == 'Loading' ? true : false}
                                    onClick={() => setMapInitialized(false)}
                                >
                                    Center Map
                                </Button>
                            }
                        >
                            {trainItems.current_station.stop_name || 'Loading'}
                        </Header>
                    }
                >
                    <SpaceBetween direction="vertical" size="l">
                        <SpaceBetween direction="horizontal" size="m">
                            {trainItems.current_station.train_lines.map((train) => (
                                <img
                                    width={isMobileDevice ? '15' : '25'}
                                    height={isMobileDevice ? '15' : '25'}
                                    src={TrainLogos[`${train}`] || ''}
                                    key={train}
                                    alt={`${train} logo`}
                                />
                            ))}
                        </SpaceBetween>
                    </SpaceBetween>
                </Container>
                {trainItems.next_four.some((train) => train.train_direction === 'Loading...') ? (
                    <Container>
                        <SpaceBetween direction="horizontal" size="m">
                            {loadingTrains.map(
                                (
                                    train,
                                    index, // Add key prop to each image
                                ) => (
                                    <img
                                        width={isMobileDevice ? '15' : '25'}
                                        height={isMobileDevice ? '15' : '25'}
                                        src={train || ''}
                                        key={index} // Use index as key
                                        alt={`Loading train ${index}`}
                                    />
                                ),
                            )}
                        </SpaceBetween>
                    </Container>
                ) : (
                    <SubwayCards trainItems={trainItems.next_four} isMobileDevice={isMobileDevice} />
                )}
            </SpaceBetween>
            <SubwayMap
                currentStation={trainItems.current_station}
                currentCenterMap={currentCenterMap}
                mapInitialized={mapInitialized}
                setMapInitialized={setMapInitialized}
            />
        </Grid>
    );
};
