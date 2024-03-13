import * as React from "react";
import { Container, Header } from "@cloudscape-design/components";
import { SubwayCards } from "./SubwayCards";
import { SubwayMap } from "./SubwayMap";

export const CurrentSubwayInfo = () => {
  return (
    <Container
      header={
        <Header variant="h2" description="Container description">
          161st Street Yankee Stadium
        </Header>
      }
    >
      <SubwayCards />
      <SubwayMap />
    </Container>
  );
};
