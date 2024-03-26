import React from 'react';
import {
    AppLayout,
    BreadcrumbGroup,
    Container,
    ContentLayout,
    Flashbar,
    Header,
    HelpPanel,
    Link,
    SideNavigation,
    SplitPanel,
} from '@cloudscape-design/components';
import { useNavigate } from 'react-router-dom';

export default () => {
    const navigate = useNavigate(); // Use navigate hook from react-router-dom

    const handleFollow = (event) => {
        event.preventDefault();
        navigate(event.detail.href); // Use navigate to handle navigation
    };

    return (
        <SideNavigation
            header={{ href: '/', text: 'Home' }}
            items={[{ type: 'link', text: 'Settings', href: '/settings' }]}
            onFollow={handleFollow}
        />
    );
};
