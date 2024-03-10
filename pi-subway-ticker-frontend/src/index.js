import * as React from "react";
import * as ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import { PiSubwayTicker } from "./PiSubwayTicker";

ReactDOM.render(
  <BrowserRouter>
    <PiSubwayTicker />
  </BrowserRouter>,
  document.getElementById("app"),
);
