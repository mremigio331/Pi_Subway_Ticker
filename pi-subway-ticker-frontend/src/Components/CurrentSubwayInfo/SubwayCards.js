import * as React from "react";
import {
  Cards,
  Box,
  ColumnLayout,
  Header,
  SpaceBetween,
} from "@cloudscape-design/components";
import train_4 from "../../../Images/SubwaySVGs/4.svg";
import train_d from "../../../Images/SubwaySVGs/b.svg";
import train_b from "../../../Images/SubwaySVGs/d.svg";

const sampleInfo = [
  {
    subwayLine: "D",
    route: "Norwood-205th Street",
    time: "Arriving",
    logo: train_d,
  },
  {
    subwayLine: "4",
    route: "Woodland",
    time: "4 minutes",
    logo: train_4,
  },
  {
    subwayLine: "B",
    route: "Bedford Park Boulevard",
    time: "10 minutes",
    logo: train_b,
  },
  {
    subwayLine: "D",
    route: "Conehy Island-Stillwell Avenue",
    time: "12 minutes",
    logo: train_d,
  },
];

const getTextColor = (time) => {
  return time === "Arriving" ? "gold" : "green";
};

const CreateRouteText = (item) => {
  return <div style={{ color: getTextColor(item.time), alignItems: 'center' }}>{item.route}</div>;
};

const CreateTimeText = (item) => {
  return (
    item.time !== "Arriving" && <div style={{ color: "green", alignItems: 'center' } }>{item.time}</div>
  );
};


export const SubwayCards = () => {
  // Check if user is on a mobile device
  const isMobileDevice = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

  return (
    <Cards
      cardDefinition={{
        header: (item) => (
          <Header
            variant="h1"
            actions={
              <Box fontSize={isMobileDevice ? "small" : "heading-xl"} fontWeight="bold" float="right">
                {CreateTimeText(item)}
              </Box>
            }
          >
             <Box fontSize={isMobileDevice ? "small" : "heading-xl"} fontWeight="bold">
            <SpaceBetween direction="horizontal" size="m">
              <img width={isMobileDevice ? "15": "25"} height={isMobileDevice ? "15": "25"} src={item.logo} />
              {CreateRouteText(item)}
            </SpaceBetween>
            </Box>
          </Header>
        ),
      }}
      cardsPerRow={[{ cards: 1 }, { minWidth: 500, cards: 1 }]}
      items={sampleInfo}
    />
  );
};
