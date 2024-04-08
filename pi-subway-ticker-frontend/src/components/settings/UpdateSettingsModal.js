import React from 'react';
import {getAllStations} from '../../services/API'

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


export const UpdateSettingsModal = ({ settingsState, settingsDispatch, configs }) => {
    const selectedIndex = configs.findIndex((config) => config.type === settingsState.selectedSetting);
    const [value, setValue] = React.useState('');
    const [selectedOption, setSelectedOption] = React.useState({});
    const [statusType, setStatusType] = React.useState('finished');
    const { isError: allTrainsIsError, data: allTrainsData, isLoading: allTrainsIsLoading, isRefetching: allTrainsIsRefetching } = useQuery({
        queryKey: ['allTrains'],
        queryFn: getAllStations,
    });

    React.useEffect(() => {
        if (allTrainsIsError) {
            setStatusType('error');
        }
        else if (allTrainsIsLoading == false) {
            setStatusType('finished')
        }
    }, [allTrainsIsError]);

    
    console.log('selectedOption', selectedOption)
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
                                setSelectedOption({}) 
                                settingsDispatch({
                                    action: { visible: false, selectedSetting: settingsState.selectedSetting },
                                })
                            }}
                        >
                            Cancel
                        </Button>
                        <Button
                            variant="primary"
                            disabled={
                                DROPDOWN_TYPES.includes(configs[selectedIndex].type) ?
                                    (statusType === 'loading' ? true : false) : value === ''
                            }
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

const ConfigsSelect = ({ selectedConfig, selectedOption, setSelectedOption, statusType, setStatusType, allTrainsData }) => {
    let options = [];
    switch (selectedConfig.type.toString()) {
        case 'cycle':
            options = BOOL_TYPE;
            break;
        case 'create_log_file':
            options = BOOL_TYPE;
            break;
        case 'station':
            console.log(allTrainsData)
            options = statusType == 'finished' ? Object.entries(allTrainsData)
            .filter(([key, value]) => value.enabled === true)
            .map(([key, value]) => ({ label: key, value: key })) : []
            break;
    }

    return (
        <Select
        selectedOption={selectedOption}
        onChange={({ detail }) => setSelectedOption(detail.selectedOption)}
        options={options}
        statusType={statusType}
        filteringType="auto"
        filterPlaceholder="Type to filter options" // Optional: Customize filter placeholder text
    />
    );
};

const DROPDOWN_TYPES = ['cycle', 'create_log_file', 'station'];
const BOOL_TYPE = [
    { label: 'true', value: true },
    { label: 'false', value: false },
];

//"cycle": true,
//"force_change_station": "",
//"log_level": "INFO",
//"create_log_file": true,
