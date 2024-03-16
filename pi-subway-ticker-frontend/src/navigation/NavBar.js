import * as React from "react";
import { TopNavigation } from "@cloudscape-design/components";
import { useNavigate } from "react-router-dom";

export default () => {
  const navigate = useNavigate();
  const handleClick = (event) => {
    event.preventDefault();
    navigate(event.detail.href);
  };
  return (
    <TopNavigation
      identity={{
        href: "/",
        title: "Pi Subway Ticker",
      }}
    />
  );
};
