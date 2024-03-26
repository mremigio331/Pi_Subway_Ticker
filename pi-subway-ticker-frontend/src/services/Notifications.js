import React, { createContext, useContext, useEffect, useReducer } from 'react';
import { useLocation } from 'react-router-dom';
import { v4 as uuidv4 } from 'uuid';

const AllNotificationsContext = createContext();

export const NotificationConstants = {
    INFO: 'info',
    SUCCESS: 'success',
    ERROR: 'error',
    WARNING: 'warning',
    PUSH_NOTIFICATION: 'push-notification',
    DISMISS_NOTIFICATION: 'dismiss-notification',
    CLEAR_NOTIFICATIONS: 'clear-notifications',
    CLEAR_PREVIOUS_NOTIFICATIONS: 'clear-previous-notifications',
    CLEAR_ALL_NOTIFICATIONS: 'clear-all-notifications',
    DISMISS_LABEL: 'Dismiss message',
};

const notificationsReducer = (state, action) => {
    switch (action.type) {
        case NotificationConstants.PUSH_NOTIFICATION:
            return [
                ...state,
                {
                    ...action.payload,
                    id: action.payload.id ? action.payload.id : uuidv4(),
                    dismissLabel: NotificationConstants.DISMISS_LABEL,
                },
            ];
        case NotificationConstants.DISMISS_NOTIFICATION:
            return state.filter((m) => m.id !== action.payload);
        case NotificationConstants.CLEAR_NOTIFICATIONS:
            return state.filter((m) => m.persistent);
        case NotificationConstants.CLEAR_PREVIOUS_NOTIFICATIONS:
            return state.filter((m) => m.persistent || m.pathKey === action.payload.pathKey);
        case NotificationConstants.CLEAR_ALL_NOTIFICATIONS:
            return [];
        default:
            // Handle any unknown action types
            return state;
    }
};

export const useAllNotifications = () => {
    return useContext(AllNotificationsContext);
};

export const AllNotificationsProvider = ({ children }) => {
    const [flashbarNotifications, dispatchFlashbarNotification] = useReducer(notificationsReducer, []);

    return (
        <AllNotificationsContext.Provider value={[flashbarNotifications, dispatchFlashbarNotification]}>
            {children}
        </AllNotificationsContext.Provider>
    );
};
