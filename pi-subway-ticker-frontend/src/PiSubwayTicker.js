import * as React from 'react';
import { AppLayout, ContentLayout, Flashbar, Header, SpaceBetween } from '@cloudscape-design/components';
import { useCookies } from 'react-cookie';
import NavBar from './navigation/NavBar';
import SideNav from './navigation/SideNav';

import { applyMode, applyDensity, Density, Mode } from '@cloudscape-design/global-styles';

import { Home } from './pages/home/Home';
import { Settings } from './pages/settings/Settings';

import { Routes, Route, useParams } from 'react-router-dom';
import { useAllNotifications, NotificationConstants } from './services/Notifications';

const PageRoutes = () => {
    const { location } = useParams();
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="settings" element={<Settings />} />
            <Route path={`/${location}`} element={<div>Page not found</div>} />
        </Routes>
    );
};
export const PiSubwayTicker = () => {
    document.title = 'Pi Subway Ticker';

    const [flashbarNotifications] = useAllNotifications();

    return (
        <div>
            <div style={{ position: 'sticky', top: 0, zIndex: 1002 }}>
                <NavBar />
            </div>
            <AppLayout
                navigation={<SideNav />}
                notifications={<Flashbar items={flashbarNotifications} />}
                content={<PageRoutes />}
            />
        </div>
    );
};
