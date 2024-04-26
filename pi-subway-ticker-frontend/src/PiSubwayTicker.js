import * as React from 'react';
import { AppLayout, ContentLayout, Flashbar, Header, SpaceBetween } from '@cloudscape-design/components';
import NavBar from './navigation/NavBar';

import { Home } from './pages/home/Home';
import { Settings } from './pages/settings/Settings';
import NotFoundPage from './pages/PageNotFound';
import SystemActions from './pages/SystemActions';

import { Routes, Route, useParams } from 'react-router-dom';
import { getNotificationsContext } from './services/Notifications'; // Fixed function name

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
    const isMobileDevice = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

    const { notifications } = getNotificationsContext(); // Fixed function call

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
