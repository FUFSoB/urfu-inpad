import React from "react";

import { createElementHook, createElementObject, createLeafComponent, createPathHook } from "@react-leaflet/core";
import L, { type LatLngExpression } from "leaflet";
import { Circle, FeatureGroup, MapContainer, Marker, Popup, TileLayer, useMapEvent } from "react-leaflet";
import { EditControl } from "react-leaflet-draw";

import styles from "./Map.module.scss";

const BASE_LATITUDE: number = 56.840447;
const BASE_LONGTITDE: number = 60.651281;
const BASE_CENTER: LatLngExpression = [BASE_LATITUDE, BASE_LONGTITDE];

const MapComponent: React.FC = () => {
  const [markers, setMarkers] = React.useState<JSX.Element[]>([]);

  function getBounds(props) {
    return L.latLng(props.center).toBounds(props.size);
  }

  function createSquare(props, context) {
    return createElementObject(new L.Rectangle(getBounds(props)), context);
  }

  function updateSquare(instance, props, prevProps) {
    if (props.center !== prevProps.center || props.size !== prevProps.size) {
      instance.setBounds(getBounds(props));
    }
  }

  const useSquareElement = createElementHook(createSquare, updateSquare);
  const useSquare = createPathHook(useSquareElement);

  const updateMarkers = React.useCallback(
    (latLng: LatLngExpression) => {
      const Square = createLeafComponent(useSquare);

      console.log(Square);

      setMarkers(prev => [
        ...prev,
        <Square
          size={10}
          center={latLng}
          key={`${JSON.stringify(latLng)}_${prev.length + 1}`}
        />, // <Marker
        //   position={latLng}
        //   key={JSON.stringify(latLng)}
        // >
        //   <Popup>{JSON.stringify(latLng)}</Popup>
        // </Marker>,
      ]);
    },
    [useSquare]
  );

  return (
    <MapContainer
      zoom={17}
      center={BASE_CENTER}
      className={styles.map}
    >
      <TileLayer
        attribution=""
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {markers.map(elem => elem)}
      {/* <CustomMapComponent updateMarkers={updateMarkers} /> */}
      <FeatureGroup>
        <EditControl
          position="topright"
          draw={{
            rectangle: false,
          }}
        />
        <Circle
          center={[51.51, -0.06]}
          radius={200}
        />
      </FeatureGroup>
    </MapContainer>
  );
};

const CustomMapComponent = ({ updateMarkers }: { updateMarkers(latLng: LatLngExpression): void }) => {
  const map = useMapEvent("click", e => {
    updateMarkers(e.latlng);
  });

  return null;
};

export default MapComponent;
