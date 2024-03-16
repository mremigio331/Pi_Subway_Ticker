import * as React from "react";
import { Container, Header, SpaceBetween } from "@cloudscape-design/components";
import { SubwayCards } from "./SubwayCards";
import { SubwayMap } from "./SubwayMap";
import { getNextFourTrains } from "../../services/API";
import { TrainLogos } from "./SubwayLogos";
import { getRandomTrainLogos } from "../loading/TrainsLoading";

const LOADING_INFO = {
  timestamp: "Loading",
  loading: false,
  current_station: { stop_name: "Loading", train_lines: [] },
  next_four: [
    {
      train: "",
      train_time: "Loading...",
      train_direction: "",
    },
    {
      train: "",
      train_time: "Loading...",
      train_direction: "",
    },
    {
      train: "",
      train_time: "Loading...",
      train_direction: "",
    },
    {
      train: "",
      train_time: "Loading...",
      train_direction: "",
    },
  ],
};

export const CurrentSubwayInfo = () => {
  const [trainItems, setTrainItems] = React.useState(LOADING_INFO);
  const [loadingTrains, setLoadingTrains] = React.useState([]);

  const isMobileDevice =
    /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
      navigator.userAgent,
    );

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getNextFourTrains(); // Call the API function
        data != undefined && setTrainItems(data); // Update the state with the fetched data
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    fetchData();
    const intervalId = setInterval(fetchData, 11000);
    return () => clearInterval(intervalId);
  }, []);

  React.useEffect(() => {
    const intervalId = setInterval(() => {
      const randomLogos = getRandomTrainLogos();
      setLoadingTrains(randomLogos);
    }, 1000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <Container
      header={
        <Header variant="h2">
          <SpaceBetween direction="vertical" size="l">
            {trainItems.current_station.stop_name || "Loading"}
            <SpaceBetween direction="horizontal" size="m">
              {trainItems.current_station.train_lines.map((train) => (
                <img
                  width={isMobileDevice ? "15" : "25"}
                  height={isMobileDevice ? "15" : "25"}
                  src={TrainLogos[`${train.toLowerCase()}`] || ""}
                />
              ))}
            </SpaceBetween>
          </SpaceBetween>
        </Header>
      }
    >
      {trainItems.next_four.some(
        (train) => train.train_direction.toLowerCase() === "Loading...",
      ) ? (
        <SpaceBetween direction="horizontal" size="m">
          {loadingTrains.map((train) => (
            <img
              width={isMobileDevice ? "15" : "25"}
              height={isMobileDevice ? "15" : "25"}
              src={train || ""}
            />
          ))}
        </SpaceBetween>
      ) : (
        <SubwayCards
          trainItems={trainItems.next_four}
          isMobileDevice={isMobileDevice}
        />
      )}

      <SubwayMap />
    </Container>
  );
};
