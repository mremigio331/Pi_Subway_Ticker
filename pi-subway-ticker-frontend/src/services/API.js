import axios from 'axios';

export const ServiceRunningCheck = async ({ dispatchFlashbarNotification, NotificationConstants }) => {
    const requestURL = `http://devpi.local:5000/`;
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

export const getNextFourTrains = async (apiCheckState, resetRetries, incrementRetries) => {
    const requestURL = `http://devpi.local:5000/trains/next_four`;
    try {
        const response = await axios.get(requestURL);
        return response.data;
    } catch (error) {
        console.error(error);
        if (error.response && error.response.status >= 400 && error.response.status < 600) {
            // Return response data for any 4xx or 5xx status code
            return error.response.data;
        } else {
            // Re-throw the error for other types of errors
            throw error;
        }
    }
};

export const getCurrentStation = async (apiCheckState, resetRetries, incrementRetries) => {
    const requestURL = `http://devpi.local:5000/trains/current_station`;
    try {
        const response = await axios.get(requestURL);
        return response.data;
    } catch (error) {
        console.error(error);
        if (error.response && error.response.status >= 400 && error.response.status < 600) {
            // Return response data for any 4xx or 5xx status code
            return error.response.data;
        } else {
            // Re-throw the error for other types of errors
            throw error;
        }
    }
};

export const getCurrentSettings = async () => {
    const requestURL = `http://devpi.local:5000/configs`;
    try {
        const response = await axios.get(requestURL);
        return response.data;
    } catch (error) {
        console.error(error);
        if (error.response && error.response.status >= 400 && error.response.status < 600) {
            // Return response data for any 4xx or 5xx status code
            return error.response.data;
        } else {
            // Re-throw the error for other types of errors
            return error.message;
        }
    }
};

export const getAllStations = async (apiCheckState, resetRetries, incrementRetries) => {
    const requestURL = `http://devpi.local:5000/stations/full_info`;
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
    const requestURL = `http://devpi.local:5000/configs/${configType}`;

    try {
        const response = await axios.put(
            requestURL,
            {},
            {
                headers: {
                    value: value.toString(), // Convert value to string if it's not already
                },
            },
        );
        return response;
    } catch (error) {
        if (error.response && error.response.status >= 400 && error.response.status < 600) {
            // Return response data for any 4xx or 5xx status code
            return error.response.data;
        } else {
            // Re-throw the error for other types of errors
            throw error;
        }
    }
};

export const updateEnabledStation = async (station, enabled) => {
    const requestURL = `http://devpi.local:5000/stations/specific_station`;

    try {
        const response = await axios.put(
            requestURL,
            {},
            {
                headers: {
                    station: station.label, // Use single quotes for header names
                    enabled: enabled.toString(), // Convert enabled to string if it's not already
                },
            },
        );
        return response;
    } catch (error) {
        console.error(error);
        if (error.response && error.response.status >= 400 && error.response.status < 600) {
            // Return response data for any 4xx or 5xx status code
            return error.response.data;
        } else {
            // Re-throw the error for other types of errors
            throw error;
        }
    }
};

export const updateCurrentStation = async (station) => {
    const requestURL = `http://devpi.local:5000/trains/current_station/update`;

    let headers = {};
    // curl -i -X PUT -H "station: Times Sq-42 St - R16" -H "cycle: false" http://devpi.local:5000/trains/current_station
    // curl -i -X PUT -H "force_change_station: 103 St - 119" -H "cycle: true" http://devpi.local:5000/trains/current_station

    headers['force_change_station'] = station;
    headers['cycle'] = 'true';

    try {
        const response = await axios.put(requestURL, {}, { headers });
        return response;
    } catch (error) {
        console.error(error);
        if (error.response && error.response.status >= 400 && error.response.status < 600) {
            // Return response data for any 4xx or 5xx status code
            return error.response.data;
        } else {
            // Re-throw the error for other types of errors
            throw error;
        }
    }
};

export const updateCode = () => {};

export const updatePi = () => {
    return new Promise((resolve, reject) => {
        const eventSource = new EventSource('http://devpi.local:5000/system/update/pi');

        eventSource.onmessage = (event) => {
            resolve(event.data); // Resolve the Promise with each chunk of text data as it arrives
        };

        eventSource.onerror = (error) => {
            reject(error); // Reject the Promise if an error occurs
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
