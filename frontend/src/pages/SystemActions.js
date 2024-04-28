import React, { useState, useEffect } from 'react';
import { Button, Container, ContentLayout, Header, SpaceBetween } from '@cloudscape-design/components';
import { CodeView } from "@cloudscape-design/code-view";

const SystemActions = () => {
    const [output, setOutput] = useState('');

    useEffect(() => {
        console.log(output);
    }, [output]);

    const handleClick = (path) => {
        const eventSource = new EventSource(`http://devpi.local:5000/system/${path}`);

        eventSource.onmessage = (event) => {
            setOutput(prevOutput => prevOutput + event.data);
        };

        eventSource.onerror = (error) => {
            console.error('EventSource error:', error);
        };

        return () => {
            eventSource.close();
        };
    };

    return (
        <ContentLayout>
            <Container
                header={
                    <Header
                        variant="h1"
                        actions={
                            <SpaceBetween direction="horizontal" size="m">
                                <Button onClick={() => handleClick('update/pi')}>Update Raspberry PI</Button>
                                <Button onClick={() => handleClick('update/pi')}>Update Pi Subway Ticker</Button>
                                <Button onClick={() => handleClick('restart')}>Restart Pi</Button>
                            </SpaceBetween>
                        }
                    >
                        System Actions
                    </Header>
                }
            >
                {/* Render the streamed data */}
                <pre>{output}</pre>
            </Container>
        </ContentLayout>
    );
};

export default SystemActions;
