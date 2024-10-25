import { useEffect, useMemo, useRef, useState } from "react";

import MapboxDraw, { type DrawCreateEvent, type DrawDeleteEvent, type DrawUpdateEvent } from "@mapbox/mapbox-gl-draw";
import "@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css";
import * as turf from "@turf/turf";
import type { Feature, GeoJsonProperties, Geometry, Point } from "geojson";
import mapboxgl, { type Map } from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

import "../styles.scss";

const paragraphStyle = {
  fontFamily: "Open Sans",
  margin: 0,
  fontSize: 13,
};

const MapComponent = () => {
  const mapContainerRef = useRef<HTMLDivElement>(null);

  /** Ссылка на карту */
  const mapRef = useRef<Map | null>(null);
  /** Ссылка на экземпляр MapboxDraw */
  const drawInstanceRef = useRef<MapboxDraw | null>(null);
  /** Нарисованная область */
  const drawedFeature = useRef<Feature<Geometry, GeoJsonProperties> | null>(null);

  /** Центр области */
  const centerAreaRef = useRef<Feature<Point, GeoJsonProperties> | null>(null);
  /** Округлённая площадь */
  const [roundedArea, setRoundedArea] = useState<number>();

  /** Эффект для подключения карты */
  useEffect(() => {
    if (!mapContainerRef.current) return;
    mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN;

    const mapboxMap = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: "mapbox://styles/mapbox/streets-v12",
      center: [60.6122, 56.8519],
      zoom: 12,
    });

    mapRef.current = mapboxMap;

    const draw = new MapboxDraw({
      displayControlsDefault: false,
      controls: {
        polygon: true,
        trash: true,
      },
      defaultMode: "simple_select",
    });

    drawInstanceRef.current = draw;

    mapboxMap.addControl(draw);

    mapboxMap.on("draw.create", onCreateArea);
    mapboxMap.on("draw.delete", onRemoveArea);
    mapboxMap.on("draw.update", onUpdateArea);
  }, []);

  /**
   * Получаем необходимые географические данные по GeoJSON.
   *
   * @param {Feature<Geometry, GeoJsonProperties>} - Географические данные
   * @returns {void}
   */
  const onGetGeoData = (feature: Feature<Geometry, GeoJsonProperties>) => {
    const area = turf.area(feature);
    setRoundedArea(Math.round(area * 100) / 100);

    if (centerAreaRef.current && drawInstanceRef.current && typeof centerAreaRef.current?.id === "string") {
      drawInstanceRef.current.delete(centerAreaRef.current.id);
    }

    const center = { ...turf.centerOfMass(feature), id: (Math.random() * 1000).toString() };
    centerAreaRef.current = center;
    drawInstanceRef.current?.add(center);

    console.log("");
    console.log("");
    console.log("Площадь в квадратных метрах", turf.area(feature));
    console.log("Центр", turf.centerOfMass(feature).geometry.coordinates);
    console.log("Длина в километрах", turf.length(feature, { units: "kilometers" }));
    console.log("");
    console.log("");
  };

  /**
   * Обрабатывает создание новой области (многоугольника) на карте.
   *
   * @param {DrawCreateEvent} e - Событие рисования, содержащее созданные объекты.
   * @returns {void}
   */
  const onCreateArea = (e: DrawCreateEvent) => {
    const feature = e.features[0];

    console.log("нарисованные данные", feature);

    if (drawInstanceRef.current && drawedFeature.current && typeof drawedFeature.current?.id === "string") {
      drawInstanceRef.current.delete(drawedFeature.current.id);
    }

    drawedFeature.current = feature;

    onGetGeoData(feature);
  };

  /**
   * Обрабатывает обновление области (многоугольника) на карте.
   *
   * @param {DrawUpdateEvent} e - Событие рисования, содержащее обновленные объекты.
   * @returns {void}
   */
  const onUpdateArea = (e: DrawUpdateEvent) => {
    const feature = e.features[0];

    drawedFeature.current = feature;

    onGetGeoData(feature);
  };

  /**
   * Обрабатывает удаление области (многоугольника) с карты.
   *
   * @param {DrawDeleteEvent} e - Событие рисования, содержащее удаленные объекты.
   * @returns {void}
   */
  const onRemoveArea = (e: DrawDeleteEvent) => {
    const feature = e.features[0];
    if (typeof feature?.id !== "string" || !drawInstanceRef.current) return;

    drawedFeature.current = null;
    drawInstanceRef.current.delete(feature.id);

    setRoundedArea(0);
  };

  return (
    <>
      <div
        id="map"
        ref={mapContainerRef}
      ></div>
      <div
        className="calculation-box"
        style={{
          height: 75,
          width: 150,
          position: "absolute",
          bottom: 40,
          left: 10,
          backgroundColor: "rgba(255, 255, 255, 0.9)",
          padding: 15,
          textAlign: "center",
        }}
      >
        <div id="calculated-area">
          {roundedArea && (
            <>
              <p style={paragraphStyle}>
                <strong>{roundedArea}</strong>
              </p>
              <p style={paragraphStyle}>квадратных метров</p>
            </>
          )}
        </div>
      </div>
    </>
  );
};

export default MapComponent;
