import React, { createContext, useContext, useReducer, useEffect } from 'react';

export const INCREMENT_RETRIES = 'INCREMENT_RETRIES';
export const RESET_RETRIES = 'RESET_RETRIES';

const initialState = {
    apiRetries: 2,
};

const apiCheckReducer = (state, action) => {
    switch (action.type) {
        case INCREMENT_RETRIES:
            return { ...state, apiRetries: state.apiRetries + 1 };
        case RESET_RETRIES:
            return { ...state, apiRetries: 0 };
        default:
            return state;
    }
};

const APICheckContext = createContext();

export const APICheckProvider = ({ children }) => {
    const [apiCheckState, dispatch] = useReducer(apiCheckReducer, initialState);

    useEffect(() => {
        sessionStorage.setItem('apiCheckState', JSON.stringify(apiCheckState));
    }, [apiCheckState]);

    return <APICheckContext.Provider value={{ apiCheckState, dispatch }}>{children}</APICheckContext.Provider>;
};

export const useApiCheck = () => {
    const context = useContext(APICheckContext);
    if (!context) {
        throw new Error('useApiCheck must be used within a APICheckProvider');
    }
    return context;
};
