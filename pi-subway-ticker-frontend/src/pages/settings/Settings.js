import React, { useEffect } from 'react';
import { ContentLayout, Flashbar, Header, SpaceBetween } from '@cloudscape-design/components';
import { CurrentSettings } from '../../components/settings/CurrentSettings';
import { useQuery } from '@tanstack/react-query';

export const Settings = () => {
    return (
        <ContentLayout header={<Header variant="h1">Settings</Header>}>
            <SpaceBetween>
                <CurrentSettings />
            </SpaceBetween>
        </ContentLayout>
    );
};
