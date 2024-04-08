import React from 'react';
import {
    Cards,
    Container,
    Button,
    Box,
    Header,
    Link,
    Modal,
    Popover,
    Spinner,
    SpaceBetween,
} from '@cloudscape-design/components';
import { useQuery } from '@tanstack/react-query';

import { UpdateSettingsModal, INITIAL_SETTINGS_MODAL_STATE, settingsReducer } from './UpdateSettingsModal';

import { getCurrentSettings } from '../../services/API';

const ConfigsCards = ({ configs, isLoading }) => {
    const filteredConfigs = configs.filter((item) => item.type !== 'force_change_station');
    const [settingsState, settingsDispatch] = React.useReducer(settingsReducer, INITIAL_SETTINGS_MODAL_STATE);
    return (
        <span>
            {configs != undefined && (
                <UpdateSettingsModal
                    settingsState={settingsState}
                    settingsDispatch={settingsDispatch}
                    configs={filteredConfigs}
                />
            )}
            <Cards
                cardDefinition={{
                    header: (item) => (
                        <Header
                            variant="h3"
                            actions={
                                <Button
                                    onClick={() =>
                                        settingsDispatch({ action: { visible: true, selectedSetting: item.type } })
                                    }
                                >
                                    Update Setting
                                </Button>
                            }
                        >
                            {item.type}
                        </Header>
                    ),
                    sections: [
                        {
                            id: 'value',
                            content: (item) =>
                                item.type == 'api_key' ? item.value.replace(/./g, '*') : item.value.toString(),
                        },
                    ],
                }}
                cardsPerRow={[{ cards: 1 }, { minWidth: 500, cards: 2 }]}
                items={filteredConfigs}
                loading={isLoading}
                loadingText="Loading Configs"
                empty={
                    <Box margin={{ vertical: 'xs' }} textAlign="center" color="inherit">
                        No configs found
                    </Box>
                }
                header={<Header>Current Configs</Header>}
            />
        </span>
    );
};

export const CurrentSettings = () => {
    const { data, isLoading, isRefetching, isError } = useQuery({
        queryKey: ['currentConfigs'],
        queryFn: getCurrentSettings,
    });

    return (
        <SpaceBetween>
            {isLoading ? (
                <Spinner /> // Render spinner when isLoading is true
            ) : (
                <ConfigsCards configs={data} isLoading={isLoading} />
            )}
        </SpaceBetween>
    );
};
