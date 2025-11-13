import React from "react";
import "./BusCityBackground.css";

export default function MergedBusSunsetBackground() {
  return (
    <div className="merged-bg">

      {/* 🌆 Sunset Sky */}
      <div className="sunset-sky"></div>

      {/* 🌥 Slow Clouds */}
      <div className="cloud c1"></div>
      <div className="cloud c2"></div>
      <div className="cloud c3"></div>

      {/* 🌅 Glowing Sun */}
      <div className="sun"></div>

      {/* 🏙 City Skyline */}
      <div className="city"></div>

      {/* 🏢 Front Buildings */}
      <div className="front-buildings"></div>

      {/* 🌳 Trees */}
      <div className="trees"></div>

      {/* 🛣 Road */}
      <div className="road">
        <div className="road-lines"></div>
      </div>

      {/* 🚌 Bus */}
      <div className="bus">
        <div className="bus-body">
          <div className="window w1"></div>
          <div className="window w2"></div>
          <div className="window w3"></div>
          <div className="window w4"></div>
          <div className="door"></div>
        </div>

        <div className="wheel wheel1"></div>
        <div className="wheel wheel2"></div>
        <div className="dust"></div>
      </div>
    </div>
  );
}
