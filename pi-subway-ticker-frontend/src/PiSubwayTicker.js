import * as React from "react";
import "@cloudscape-design/components";
import { useCookies } from "react-cookie";
import NavBar from "./NavBar";
import {
  applyMode,
  applyDensity,
  Density,
  Mode,
} from "@cloudscape-design/global-styles";
import { Home } from "./Pages/Home/Home";
import { Routes, Route } from "react-router-dom";

const PageRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
    </Routes>
  );
};
export const PiSubwayTicker = () => {
  document.title = "Pi Subway Ticker";
  return (
    <div>
      <div style={{ position: "sticky", top: 0, zIndex: 1002 }}>
        <NavBar />
      </div>
      {<PageRoutes />}
    </div>
  );
};
