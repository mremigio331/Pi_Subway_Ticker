import React, { createContext, useContext, useEffect, useReducer } from 'react';
import { useLocation } from 'react-router-dom';
import { v4 as uuidv4 } from 'uuid';

const NotificationsContext = createContext();

export const NotificationConstants = {
    INFO: 'info',
    SUCCESS: 'success',
    ERROR: 'error',
    WARNING: 'warning',
    PUSH_NOTIFICATION: 'push-notification',
    DISMISS_NOTIFICATION: 'dismiss-notification',
    UPDATE_NOTIFICATION: 'update-notification',
    CLEAR_NOTIFICATIONS: 'clear-notifications',
    CLEAR_PREVIOUS_NOTIFICATIONS: 'clear-previous-notifications',
    CLEAR_ALL_NOTIFICATIONS: 'clear-all-notifications',
    DISMISS_LABEL: 'Dismiss message',
};

const notificationsReducer = (state, action) => {
    const { type, payload } = action;
    switch (type) {
        case NotificationConstants.PUSH_NOTIFICATION:
            return [
                ...state,
                {
                    ...payload,
                    id: payload.id || uuidv4(),
                    dismissLabel: NotificationConstants.DISMISS_LABEL,
                },
            ];
        case NotificationConstants.DISMISS_NOTIFICATION:
            return state.filter((notification) => notification.id !== payload);
        case NotificationConstants.UPDATE_NOTIFICATION:
            return state.map((notification) =>
                notification.id === payload.id ? { ...notification, ...payload.updatedContent } : notification,
            );
        case NotificationConstants.CLEAR_NOTIFICATIONS:
            return state.filter((notification) => notification.persistent);
        case NotificationConstants.CLEAR_PREVIOUS_NOTIFICATIONS:
            return state.filter((notification) => notification.persistent || notification.pathKey === payload.pathKey);
        case NotificationConstants.CLEAR_ALL_NOTIFICATIONS:
            return [];
        default:
            throw new Error(`Missing Reducer Action: ${type}`);
    }
};

export const enhanceMessagesWithDismissAction = (messages, dispatch) => {
    return messages.map((message) => {
        message.onDismiss = () => {
            dispatch({
                type: NotificationConstants.DISMISS_NOTIFICATION,
                payload: message.id,
            });
        };
        return message;
    });
};

export const getNotificationsContext = () => {
    const [notifications, dispatchNotification] = useContext(NotificationsContext);
    const location = useLocation();

    const pushNotification = (message) => {
        dispatchNotification({
            type: NotificationConstants.PUSH_NOTIFICATION,
            payload: {
                ...message,
                pathKey: location.key,
            },
        });
    };

    const dismissNotification = (id) => {
        dispatchNotification({
            type: NotificationConstants.DISMISS_NOTIFICATION,
            payload: id,
        });
    };

    const modifyNotificationContent = (id, updatedContent) => {
        dispatchNotification({
            type: NotificationConstants.UPDATE_NOTIFICATION,
            payload: {
                id,
                updatedContent,
            },
        });
    };

    return {
        notifications,
        dispatchNotification,
        pushNotification,
        dismissNotification,
        modifyNotificationContent,
    };
};

export const NotificationsProvider = ({ children }) => {
    const location = useLocation();
    const [notifications, dispatchNotification] = useReducer(notificationsReducer, []);

    useEffect(() => {
        dispatchNotification({
            type: NotificationConstants.CLEAR_PREVIOUS_NOTIFICATIONS,
            payload: {
                pathKey: location.key,
            },
        });
    }, [location]);

    return (
        <NotificationsContext.Provider value={[notifications, dispatchNotification]}>
            {children}
        </NotificationsContext.Provider>
    );
};
