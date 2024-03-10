import React from "react";
import {
  AppLayout,
  BreadcrumbGroup,
  Container,
  ContentLayout,
  Flashbar,
  Header,
  HelpPanel,
  Link,
  SideNavigation,
  SpaceBetween,
  SplitPanel,
} from "@cloudscape-design/components";
import { CurrentSubwwayInfo } from "../../Components/CurrentSubwayInfo/CurrentSubwayInfo";

export const Home = () => {
  return (
    <AppLayout
      content={
        <ContentLayout header={<Header variant="h1">Pi Subway Ticker</Header>}>
          <SpaceBetween>
            <CurrentSubwwayInfo />
          </SpaceBetween>
        </ContentLayout>
      }
    />
  );
};
