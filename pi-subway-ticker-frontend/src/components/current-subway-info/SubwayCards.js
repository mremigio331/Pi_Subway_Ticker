import * as React from 'react';
import { Cards, Box, ColumnLayout, Header, SpaceBetween } from '@cloudscape-design/components';

import { TrainLogos } from './SubwayLogos';

const getTextColor = (time) => {
    return time === 0 ? 'gold' : 'green';
};

const CreateRouteText = (item) => {
    return <div style={{ color: getTextColor(item.train_time), alignItems: 'center' }}>{item.train_direction}</div>;
};

const CreateTimeText = (item) => {
    return item.train_time != 0 && <div style={{ color: 'green', alignItems: 'center' }}>{item.train_time}</div>;
};

export const SubwayCards = ({ trainItems, isMobileDevice }) => {
    // Check if user is on a mobile device

    return (
        <Cards
            cardDefinition={{
                header: (item) => (
                    <Header
                        variant="h1"
                        actions={
                            <Box fontSize={isMobileDevice ? 'small' : 'heading-xl'} fontWeight="bold" float="right">
                                {CreateTimeText(item)}
                            </Box>
                        }
                    >
                        <Box fontSize={isMobileDevice ? 'small' : 'heading-xl'} fontWeight="bold">
                            <SpaceBetween direction="horizontal" size="m">
                                <img
                                    width={isMobileDevice ? '15' : '25'}
                                    height={isMobileDevice ? '15' : '25'}
                                    src={TrainLogos[`${item.train.toLowerCase()}`] || ''}
                                />
                                {CreateRouteText(item)}
                            </SpaceBetween>
                        </Box>
                    </Header>
                ),
            }}
            cardsPerRow={[{ cards: 1 }, { minWidth: 500, cards: 1 }]}
            items={trainItems}
        />
    );
};
