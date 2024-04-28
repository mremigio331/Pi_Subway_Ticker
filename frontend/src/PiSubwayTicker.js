import * as React from 'react';
import { AppLayout, Flashbar } from '@cloudscape-design/components';
import NavBar from './navigation/NavBar';

import { Home } from './pages/home/Home';
import { Settings } from './pages/settings/Settings';
import NotFoundPage from './pages/PageNotFound';
import SystemActions from './pages/SystemActions';

import { Routes, Route, useParams } from 'react-router-dom';
import { getNotificationsContext } from './services/Notifications';
const PageRoutes = () => {
    const { location } = useParams();
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/system" element={<SystemActions />} />
            <Route path="*" element={<NotFoundPage />} />
        </Routes>
    );
};
export const PiSubwayTicker = () => {
    document.title = 'Pi Subway Ticker';
    const { notifications } = getNotificationsContext(); 

    return (
        <div>
            <div style={{ position: 'sticky', top: 0, zIndex: 1002 }}>
                <NavBar />
            </div>
            <AppLayout
                notifications={<Flashbar items={notifications} />}
                content={<PageRoutes />}
                navigationHide
                toolsHide
                maxContentWidth={Number.MAX_VALUE}
            />
        </div>
    );
};
