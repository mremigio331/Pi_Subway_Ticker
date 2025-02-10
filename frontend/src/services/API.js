import axios from 'axios';
import { apiEndpoint } from '../configs/apiConfig';

export const ServiceRunningCheck = async ({ dispatchFlashbarNotification, NotificationConstants }) => {
    const requestURL = `http://${apiEndpoint}:5000/`;
    try {
        const response = await axios.get(requestURL);

        if (response.status >= 200 && response.status < 300) {
            dispatchFlashbarNotification({
                type: NotificationConstants.PUSH_NOTIFICATION,
                payload: {
                    id: 'service-running-notification',
                    content: 'Service is running successfully!',
                },
            });
        }
    } catch (error) {
        dispatchFlashbarNotification({
            type: NotificationConstants.PUSH_NOTIFICATION,
            payload: {
                id: 'service-running-notification',
                content: 'Service is running unsuccessfully!',
            },
        });
    }
};

export const getNextFourTrains = async () => {
    const requestURL = `http://${apiEndpoint}:5000/trains/next_four`;
    try {
        const response = await axios.get(requestURL);
        return response.data;
    } catch (error) {
        console.error(error);
        if (error.response && error.response.status >= 400 && error.response.status < 600) {
            return error.response.data;
        } else {
            throw error;
        }
    }
};

export const getCurrentStation = async () => {
    const requestURL = `http://${apiEndpoint}:5000/trains/current_station`;
    try {
        const response = await axios.get(requestURL);
        return response.data;
    } catch (error) {
        console.error(error);
        if (error.response && error.response.status >= 400 && error.response.status < 600) {
            return error.response.data;
        } else {
            throw error;
        }
    }
};

export const getCurrentSettings = async () => {
    const requestURL = `http://${apiEndpoint}:5000/configs`;
    try {
        const response = await axios.get(requestURL);
        return response.data;
    } catch (error) {
        console.error(error);
        if (error.response && error.response.status >= 400 && error.response.status < 600) {
            return error.response.data;
        } else {
            return error.message;
        }
    }
};

export const getAllStations = async () => {
    const requestURL = `http://${apiEndpoint}:5000/stations/full_info`;
    const response = await axios
        .get(requestURL)
        .then((res) => {
            return res;
        })
        .catch((error) => {
            return error;
        });

    return response.data;
};

export const updateConfig = async (configType, value) => {
    const requestURL = `http://${apiEndpoint}:5000/configs/update_specific_config`;

    const data = {
        config: configType,
        value: value.toString()
    };

    try {
        const response = await axios.put(requestURL, data);
        return response;
    } catch (error) {
        if (error.response && error.response.status >= 400 && error.response.status < 600) {
            return error.response.data;
        } else {
            throw error;
        }
    }
};

export const updateEnabledStation = async (station, enabled) => {
    const requestURL = `http://${apiEndpoint}:5000/stations/specific_station`;

    try {
        const response = await axios.put(
            requestURL,
            {},
            {
                headers: {
                    station: station.label,
                    enabled: enabled.toString(),
                },
            },
        );
        return response;
    } catch (error) {
        console.error(error);
        if (error.response && error.response.status >= 400 && error.response.status < 600) {
            return error.response.data;
        } else {
            throw error;
        }
    }
};

export const forceUpdateCurrentStation = async (station) => {
    const requestURL = `http://${apiEndpoint}:5000/stations/force_change_station`;

    const data = {
        force_change_station: station,
        cycle: true
    };

    try {
        const response = await axios.put(requestURL, data);
        return response;
    } catch (error) {
        console.error(error);
        if (error.response && error.response.status >= 400 && error.response.status < 600) {
            return error.response.data;
        } else {
            throw error;
        }
    }
};

export const updateCode = () => {};

export const updatePi = () => {
    return new Promise((resolve, reject) => {
        const eventSource = new EventSource('http://${apiEndpoint}:5000/system/update/pi');

        eventSource.onmessage = (event) => {
            resolve(event.data);
        };

        eventSource.onerror = (error) => {
            reject(error);
        };
    });
};

export const restartPi = async () => {
    try {
        const response = await axios.put('/system/restart');
        return response.data.message;
    } catch (error) {
        throw new Error(error.response.data.error || 'Failed to restart Raspberry Pi');
    }
};
