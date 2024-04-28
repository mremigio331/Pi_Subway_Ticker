import * as React from 'react';
import { StatusIndicator, TopNavigation } from '@cloudscape-design/components';
import { useNavigate } from 'react-router-dom';
import { useApiCheck, RESET_RETRIES } from '../providers/APICheckProvider';
import { getNotificationsContext } from '../services/Notifications';
import { v4 as uuidv4 } from 'uuid';

export default () => {
    const navigate = useNavigate();
    const { dismissNotification, pushNotification, modifyNotificationContent } = getNotificationsContext();

    const { apiCheckState, dispatch } = useApiCheck();
    console.log(apiCheckState);

    const handlePageClick = (event) => {
        event.preventDefault();
        navigate(event.detail.href);
    };

    const handleHomeClick = (event) => {
        event.preventDefault();
        navigate('/');
    };

    const handleAPIReset = (event) => {
        console.log('CLICKED ME');
        dispatch({ type: RESET_RETRIES });
        const message_id = uuidv4();
        const message = {
            content: 'Attempting to Reconnect To API',
            type: NotificationConstants.INFO,
            id: message_id,
            onDismiss: () => dismissNotification(message_id),
            dismissible: false,
            dismissLabel: 'Dismiss',
            loading: true,
        };
        pushNotification(message);
        if (apiCheckState.apiRetries == 0) {
            message.content = 'API Successfully Reconnected';
            message.type = NotificationConstants.SUCCESS;
            message.dismissible = true;
            message.loading = false;
            modifyNotificationContent(message_id, message);
        } else if (apiCheckState.apiRetries < 10) {
            message.content = `Failed to reconnect to the API`;
            message.type = NotificationConstants.ERROR;
            message.dismissible = true;
            message.loading = false;
            modifyNotificationContent(message_id, message);
        }
    };

    return (
        <TopNavigation
            identity={{
                href: '/',
                title: 'Pi Subway Ticker',
                onFollow: handleHomeClick,
            }}
            utilities={[
                {
                    type: 'button',
                    text: 'Settings',
                    href: '/settings',
                    onClick: handlePageClick,
                },

                {
                    type: 'menu-dropdown',
                    iconName: 'settings',
                    ariaLabel: 'Settings',
                    title: 'Status',
                    items: [
                        {
                            id: 'apiErrorCount',
                            text: <ApiStatusIndicator currentAPIRetryCount={apiCheckState.apiRetries} />,
                        },
                    ],
                },
            ]}
        />
    );
};

const ApiStatusIndicator = ({ currentAPIRetryCount }) => {
    switch (true) {
        case currentAPIRetryCount < 1:
            return <StatusIndicator>Local API</StatusIndicator>;
        case currentAPIRetryCount >= 1 && currentAPIRetryCount <= 4:
            return <StatusIndicator type="warning">Local API</StatusIndicator>;
        case currentAPIRetryCount >= 5:
            return <StatusIndicator type="error">Local API</StatusIndicator>;
        default:
            return '';
    }
};
