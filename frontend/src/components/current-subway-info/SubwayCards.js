import * as React from 'react';
import { Cards, Box, ColumnLayout, Header, SpaceBetween } from '@cloudscape-design/components';

import { TrainLogos } from '../../utility/SubwayLogos';

const getTextColor = (time) => {
    return time === 0 ? 'gold' : 'green';
};

const CreateRouteText = (item) => {
    return (
        <Header variant="h4" style={{ color: getTextColor(item.train_time), alignItems: 'center' }}>
            {item.train_direction}
        </Header>
    );
};

const CreateTimeText = (item) => {
    return (
        item.train_time != 0 && (
            <Header variant="h4" style={{ color: 'green', alignItems: 'center' }}>
                {item.train_time}
            </Header>
        )
    );
};

export const SubwayCards = ({ trainItems, isMobileDevice }) => {
    return (
        <Cards
            cardDefinition={{
                header: (item) => (
                    <Header
                        variant="h4"
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
                                    src={TrainLogos[`${item.train}`] || ''}
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
