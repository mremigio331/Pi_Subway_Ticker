import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';
import { PiSubwayTicker } from './PiSubwayTicker';
import { AllNotificationsProvider } from './services/Notifications';
import { APICheckProvider } from './providers/APICheckProvider';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

ReactDOM.render(
    <BrowserRouter>
        <QueryClientProvider client={queryClient}>
            <AllNotificationsProvider>
                <APICheckProvider>
                    <PiSubwayTicker />
                </APICheckProvider>
            </AllNotificationsProvider>
        </QueryClientProvider>
    </BrowserRouter>,
    document.getElementById('app'),
);
