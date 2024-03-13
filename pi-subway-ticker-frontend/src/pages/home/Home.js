import React, { useEffect } from "react";
import {
  AppLayout,
  ContentLayout,
  Flashbar,
  Header,
  SpaceBetween,
} from "@cloudscape-design/components";
import { ServiceRunningCheck } from "../../services/API";
import { CurrentSubwayInfo } from "../../components/current-subway-info/CurrentSubwayInfo";
import {
  useAllNotifications,
  NotificationConstants,
} from "../../services/Notifications";

export const Home = () => {
  const [flashbarNotifications] = useAllNotifications();

  return (
    <AppLayout
      notifications={<Flashbar items={flashbarNotifications} />}
      content={
        <ContentLayout header={<Header variant="h1">Pi Subway Ticker</Header>}>
          <SpaceBetween>
            <CurrentSubwayInfo />
          </SpaceBetween>
        </ContentLayout>
      }
    />
  );
};
