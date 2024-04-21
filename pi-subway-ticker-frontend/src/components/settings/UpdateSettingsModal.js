import React, { useState, useEffect } from 'react';
import { getAllStations, updateConfig, updateCurrentStation } from '../../services/API';
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
    Select,
    SpaceBetween,
    Textarea,
    TextContent,
} from '@cloudscape-design/components';
import { useQuery } from '@tanstack/react-query';
import {
    getNotificationsContext,
    NotificationConstants,
    enhanceMessagesWithDismissAction,
} from '../../services/Notifications'; // Updated import
import { v4 as uuidv4 } from 'uuid';

export const UpdateSettingsModal = ({ settingsState, settingsDispatch, configs, refetch }) => {
    const selectedIndex = configs.findIndex((config) => config.type === settingsState.selectedSetting);
    const [value, setValue] = useState('');
    const [selectedOption, setSelectedOption] = useState({});
    const [statusType, setStatusType] = useState('finished');
    const {
        isError: allTrainsIsError,
        data: allTrainsData,
        isLoading: allTrainsIsLoading,
        isRefetching: allTrainsIsRefetching,
        refetch: refetchAllTrains
    } = useQuery({
        queryKey: ['allTrains'],
        queryFn: getAllStations,
    });

    const { dismissNotification, pushNotification, modifyNotificationContent } =
        getNotificationsContext(); // Updated usage

    const handleUpdateClick = async () => {
        const message_id = uuidv4();
        const message = {
            content: 'Updating config',
            type: NotificationConstants.INFO,
            id: message_id,
            onDismiss: () => dismissNotification(message_id),
            dismissible: false,
            dismissLabel: 'Dismiss',
            loading: true,
        };
        pushNotification(message);
        settingsDispatch({ action: { visible: false, selectedSetting: settingsState.selectedSetting } });
        const response = await updateConfig(configs[selectedIndex].type, value);
        if (response.status === 200 || response.status === 204) {
            message.content = response.data;
            message.type = NotificationConstants.SUCCESS;
            message.dismissible = true;
            message.loading = false;
            modifyNotificationContent(message_id, message);
        } else {
            message.content = `Failed to update config: ${response.error}`;
            message.type = NotificationConstants.ERROR;
            message.dismissible = true;
            message.loading = false;
            modifyNotificationContent(message_id, message);
        }
        refetch()

    };

    useEffect(() => {
        if (allTrainsIsError) {
            setStatusType('error');
        } else if (allTrainsIsLoading === false) {
            setStatusType('finished');
        }
    }, [allTrainsIsError, allTrainsIsLoading]);

    return (
        <Modal
            onDismiss={() =>
                settingsDispatch({ action: { visible: false, selectedSetting: settingsState.selectedSetting } })
            }
            visible={settingsState.visible}
            footer={
                <Box float="right">
                    <SpaceBetween direction="horizontal" size="xs">
                        <Button
                            variant="link"
                            onClick={() => {
                                setSelectedOption({});
                                setValue('')
                                settingsDispatch({
                                    action: { visible: false, selectedSetting: settingsState.selectedSetting },
                                });
                            }}
                        >
                            Cancel
                        </Button>
                        <Button
                            variant="primary"
                            disabled={
                                DROPDOWN_TYPES.includes(configs[selectedIndex].type)
                                    ? statusType === 'loading'
                                    : value === ''
                            }
                            onClick={handleUpdateClick}
                        >
                            Update
                        </Button>
                    </SpaceBetween>
                </Box>
            }
            header={<Header> Update {settingsState.selectedSetting}</Header>}
        >
            <SpaceBetween direction="vertical">
                <TextContent>
                    <p>Current Value: {configs[selectedIndex].value.toString()} </p>
                </TextContent>
                {DROPDOWN_TYPES.includes(configs[selectedIndex].type) ? (
                    <ConfigsSelect
                        selectedConfig={configs[selectedIndex]}
                        selectedOption={selectedOption}
                        setSelectedOption={setSelectedOption}
                        statusType={statusType}
                        setStatusType={setStatusType}
                        allTrainsData={allTrainsData}
                        setValue={setValue}
                    />
                ) : (
                    <Textarea
                        onChange={({ detail }) => setValue(detail.value)}
                        value={value}
                        placeholder={configs[selectedIndex].value}
                        autoFocus
                    />
                )}
            </SpaceBetween>
        </Modal>
    );
};

export const INITIAL_SETTINGS_MODAL_STATE = {
    visible: false,
    selectedSetting: 'api_key',
};

export const settingsReducer = (settingsSate, action) => {
    return action.action;
};

const ConfigsSelect = ({
    selectedConfig,
    selectedOption,
    setSelectedOption,
    statusType,
    setStatusType,
    allTrainsData,
    setValue,
}) => {
    let options = [];
    switch (selectedConfig.type.toString()) {
        case 'cycle':
            options = BOOL_TYPE;
            break;
        case 'create_log_file':
            options = BOOL_TYPE;
            break;
        case 'station':
            options =
                statusType === 'finished'
                    ? Object.entries(allTrainsData)
                          .filter(([key, value]) => value.enabled === true)
                          .map(([key, value]) => ({ label: key, value: key }))
                    : [];
            break;
        default:
            options = [];
            break;
    }

    return (
        <Select
            selectedOption={selectedOption}
            onChange={({ detail }) => {
                setSelectedOption(detail.selectedOption);
                setValue(detail.selectedOption.value);
            }}
            options={options}
            statusType={statusType}
            filteringType="auto"
            filterPlaceholder="Type to filter options"
        />
    );
};

const DROPDOWN_TYPES = ['cycle', 'create_log_file', 'station'];
const BOOL_TYPE = [
    { label: 'true', value: true },
    { label: 'false', value: false },
];
