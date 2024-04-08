import * as React from 'react';
import { Container, Header, SpaceBetween } from '@cloudscape-design/components';
import { SubwayCards } from './SubwayCards';
import { SubwayMap } from './SubwayMap';
import { getNextFourTrains } from '../../services/API';
import { TrainLogos } from './SubwayLogos';
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
    const [trainItems, setTrainItems] = React.useState(LOADING_INFO);
    const [loadingTrains, setLoadingTrains] = React.useState([]);
    const { apiCheckState, dispatch } = useApiCheck();

    const incrementRetries = () => {
        dispatch({ type: INCREMENT_RETRIES });
    };

    const resetRetries = () => {
        dispatch({ type: RESET_RETRIES });
    };

    const isMobileDevice = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

    React.useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await getNextFourTrains();
                data !== undefined && setTrainItems(data);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        const fetchDataAfterDelay = () => {
            setTimeout(() => {
                fetchData(); // Call fetchData after 7 seconds
                const intervalId = setInterval(fetchData, 11000); // Set interval to call fetchData every 7 seconds
                return () => clearInterval(intervalId);
            }, 7000);
        };

        const intervalId = fetchDataAfterDelay(); // Call fetchDataAfterDelay when component mounts

        // Clear interval when component unmounts
        return () => clearInterval(intervalId);
    }, []);

    React.useEffect(() => {
        const intervalId = setInterval(() => {
            const randomLogos = getRandomTrainLogos();
            setLoadingTrains(randomLogos);
        }, 1000);

        return () => clearInterval(intervalId);
    }, []);

    return (
        <Container
            header={
                <Header variant="h2">
                    <SpaceBetween direction="vertical" size="l">
                        {trainItems.current_station.stop_name || 'Loading'}
                        <SpaceBetween direction="horizontal" size="m">
                            {trainItems.current_station.train_lines.map((train) => (
                                <img
                                    width={isMobileDevice ? '15' : '25'}
                                    height={isMobileDevice ? '15' : '25'}
                                    src={TrainLogos[`${train.toLowerCase()}`] || ''}
                                    key={train} // Ensure each image has a unique key
                                    alt={`${train} logo`}
                                />
                            ))}
                        </SpaceBetween>
                    </SpaceBetween>
                </Header>
            }
        >
            {trainItems.next_four.some((train) => train.train_direction === 'Loading...') ? (
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
            ) : (
                <SubwayCards trainItems={trainItems.next_four} isMobileDevice={isMobileDevice} />
            )}

            <SubwayMap />
        </Container>
    );
};
