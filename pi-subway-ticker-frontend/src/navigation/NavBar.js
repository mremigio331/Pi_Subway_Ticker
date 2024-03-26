import * as React from 'react';
import { StatusIndicator, TopNavigation } from '@cloudscape-design/components';
import { useNavigate } from 'react-router-dom';
import { useApiCheck } from '../providers/APICheckProvider';

export default () => {
    const navigate = useNavigate();
    const { apiCheckState } = useApiCheck();
    const [currentAPIRetryCount, setCurrentAPIRetryCount] = React.useState(apiCheckState.apiRetries);

    // React.useMemo(() => {
    //   setCurrentAPIRetryCount(apiCheckState.apiRetries);
    //   console.log("apiCheckState", apiCheckState.apiRetries);
    // }, [apiCheckState]); // Dependency array with apiCheckState

    const handleClick = (event) => {
        event.preventDefault();
        navigate(event.detail.href);
    };

    return (
        <TopNavigation
            identity={{
                href: '/',
                title: 'Pi Subway Ticker',
            }}
            utilities={[
                {
                    type: 'menu-dropdown',
                    iconName: 'settings',
                    ariaLabel: 'Settings',
                    title: 'Status',
                    items: [
                        {
                            id: 'apiErrorCount',
                            text: <ApiStatusIndicator currentAPIRetryCount={currentAPIRetryCount} />,
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
            return ''; // Handle any other cases (optional)
    }
};
