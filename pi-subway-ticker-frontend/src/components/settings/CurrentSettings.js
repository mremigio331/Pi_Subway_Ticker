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
    ContentLayout,
} from '@cloudscape-design/components';
import { useQuery } from '@tanstack/react-query';

import { UpdateSettingsModal, INITIAL_SETTINGS_MODAL_STATE, settingsReducer } from './UpdateSettingsModal';

import { getCurrentSettings } from '../../services/API';

const ConfigsCards = ({ configs, isLoading, isRefetching, refetch }) => {
    const filteredConfigs = configs.filter((item) => item.type !== 'force_change_station');
    const [settingsState, settingsDispatch] = React.useReducer(settingsReducer, INITIAL_SETTINGS_MODAL_STATE);

    return (
        <>
            {configs != undefined && (
                <UpdateSettingsModal
                    settingsState={settingsState}
                    settingsDispatch={settingsDispatch}
                    configs={filteredConfigs}
                    refetch={refetch}
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
                header={
                    <Header
                        actions={
                            <Button
                                iconName="refresh"
                                variant="icon"
                                disabled={isLoading || isRefetching}
                                onClick={() => refetch()}
                            />
                        }
                    >
                        Current Configs
                    </Header>
                }
            />
        </>
    );
};

export const CurrentSettings = () => {
    const { data, isLoading, isRefetching, isError, refetch } = useQuery({
        queryKey: ['currentConfigs'],
        queryFn: getCurrentSettings,
    });

    return (
        <ContentLayout>
            {isLoading ? (
                <Spinner />
            ) : isError || data == 'Network Error' ? (
                <Container
                    header={
                        <Header
                            actions={
                                <SpaceBetween direction="horizontal" size="s">
                                    <Button>Restart PI</Button>
                                </SpaceBetween>
                            }
                        >
                            Error
                        </Header>
                    }
                >
                    There was an error with the API. Check to confirm the API is running. You can also try to restart
                    the API or the Pi
                </Container>
            ) : (
                <ConfigsCards configs={data} isLoading={isLoading} isRefetching={isRefetching} refetch={refetch} />
            )}
        </ContentLayout>
    );
};
