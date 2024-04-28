import * as React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { PiSubwayTicker } from './PiSubwayTicker';
import { NotificationsProvider } from './services/Notifications';
import { APICheckProvider } from './providers/APICheckProvider';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

createRoot(document.getElementById('app')).render(
    <BrowserRouter>
        <QueryClientProvider client={queryClient}>
            <NotificationsProvider>
                <APICheckProvider>
                    <PiSubwayTicker />
                </APICheckProvider>
            </NotificationsProvider>
        </QueryClientProvider>
    </BrowserRouter>,
);
