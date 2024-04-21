import axios from 'axios';

export const ServiceRunningCheck = async ({ dispatchFlashbarNotification, NotificationConstants }) => {
    const requestURL = `http://localhost:5000/`;
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
    const requestURL = `http://localhost:5000/trains/next_four`;
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

export const getCurrentStation = async (apiCheckState, resetRetries, incrementRetries) => {
    const requestURL = `http://localhost:5000/trains/current_station`;
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

export const getCurrentSettings = async (apiCheckState, resetRetries, incrementRetries) => {
    const requestURL = `http://localhost:5000/config`;
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

export const getAllStations = async (apiCheckState, resetRetries, incrementRetries) => {
    const requestURL = `http://localhost:5000/trains/stations/full_info`;
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
    const requestURL = `http://localhost:5000/config/${configType}`;

    try {
        const response = await axios.put(requestURL, {}, {
            headers: {
                value: value.toString() // Convert value to string if it's not already
            }
        });
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
}

export const updateEnabledStation = async (station, enabled) => {
    console.log('station', station);
    const requestURL = `http://localhost:5000/trains/stations/specific_station`;
    
    try {
        const response = await axios.put(requestURL, {}, {
            headers: {
                'station': station.label, // Use single quotes for header names
                'enabled': enabled.toString() // Convert enabled to string if it's not already
            }
        });
        console.log(response);
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

export const updateCurrentStation = async (station, forceChange, cycle) => {
    const requestURL = `http://localhost:5000/trains/current_station/update`;

    let headers = {};
    // curl -i -X PUT -H "station: Times Sq-42 St - R16" -H "cycle: false" http://localhost:5000/trains/current_station
    // curl -i -X PUT -H "force_change_station: 103 St - 119" -H "cycle: true" http://localhost:5000/trains/current_station



    forceChange == true ? headers['station'] = station.label : headers['force_change_station'] = station.label
    headers['cycle'] = cycle.toString()
    
    try {
        const response = await axios.put(requestURL, {}, { headers });
        console.log(response);
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
