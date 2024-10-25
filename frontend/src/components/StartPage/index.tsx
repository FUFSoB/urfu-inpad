import React from "react";

import MapComponent from "./Map/MapComponent";
import SceneComponent from "./SceneComponent";

export const StartPage: React.FC = () => {
  return (
    <div>
      <MapComponent />
      <SceneComponent />
    </div>
  );
};
