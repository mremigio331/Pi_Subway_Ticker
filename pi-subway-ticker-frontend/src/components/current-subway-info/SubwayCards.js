import * as React from "react";
import {
  Cards,
  Box,
  ColumnLayout,
  Header,
  SpaceBetween,
} from "@cloudscape-design/components";

import { getNextFourTrains } from "../../services/API";
import { TrainLogos } from "./SubwayLogos"

const getTextColor = (time) => {
  return time === 0 ? "gold" : "green";
};

const CreateRouteText = (item) => {
  return (
    <div style={{ color: getTextColor(item.train_time), alignItems: "center" }}>
      {item.train_direction}
    </div>
  );
};

const CreateTimeText = (item) => {
  return (
    item.time !== 0 && (
      <div style={{ color: "green", alignItems: "center" }}>
        {item.train_time}
      </div>
    )
  );
};

export const SubwayCards = () => {
  // Check if user is on a mobile device
  const isMobileDevice =
    /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
      navigator.userAgent,
    );

  const [trainItems, setTrainItems] = React.useState([]);
  React.useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getNextFourTrains(); // Call the API function
        setTrainItems(data.next_four); // Update the state with the fetched data
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData(); // Fetch data initially

    const intervalId = setInterval(fetchData, 5000); // Fetch data every 5 seconds

    // Clean up interval to avoid memory leaks
    return () => clearInterval(intervalId);
  }, []); // Empty dependency array to run only once on mount

  console.log(trainItems);
  

  return (
    <Cards
      cardDefinition={{
        header: (item) => (
          <Header
            variant="h1"
            actions={
              <Box
                fontSize={isMobileDevice ? "small" : "heading-xl"}
                fontWeight="bold"
                float="right"
              >
                {CreateTimeText(item)}
              </Box>
            }
          >
            <Box
              fontSize={isMobileDevice ? "small" : "heading-xl"}
              fontWeight="bold"
            >
              <SpaceBetween direction="horizontal" size="m">
                <img
                  width={isMobileDevice ? "15" : "25"}
                  height={isMobileDevice ? "15" : "25"}
                  src={TrainLogos[`${item.train.toLowerCase()}`] || ''}
                />
                {CreateRouteText(item)}
              </SpaceBetween>
            </Box>
          </Header>
        ),
      }}
      cardsPerRow={[{ cards: 1 }, { minWidth: 500, cards: 1 }]}
      items={trainItems}
    />
  );
};
