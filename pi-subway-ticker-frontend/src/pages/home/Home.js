import React, { useEffect } from 'react';
import { ContentLayout, Flashbar, Header, SpaceBetween } from '@cloudscape-design/components';
import { CurrentSubwayInfo } from '../../components/current-subway-info/CurrentSubwayInfo';

export const Home = () => {
    return (
        <ContentLayout header={<Header variant="h1">Pi Subway Ticker</Header>}>
            <SpaceBetween>
                <CurrentSubwayInfo />
            </SpaceBetween>
        </ContentLayout>
    );
};
