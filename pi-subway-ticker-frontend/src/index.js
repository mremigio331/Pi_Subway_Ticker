import * as React from "react";
import * as ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import { PiSubwayTicker } from "./PiSubwayTicker";
import { AllNotificationsProvider } from "./services/Notifications"; // Import the context provider

ReactDOM.render(
  <BrowserRouter>
    <AllNotificationsProvider>
      <PiSubwayTicker />
    </AllNotificationsProvider>
  </BrowserRouter>,
  document.getElementById("app"),
);
