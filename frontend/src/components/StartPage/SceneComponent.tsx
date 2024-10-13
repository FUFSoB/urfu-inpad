import React, { useEffect, useRef } from "react";

import { Engine, type EngineOptions, Scene, type SceneOptions } from "@babylonjs/core";

type TScreenComponentProps = {
  /** Опциональный параметр для включения сглаживания. */
  antialias?: boolean;

  /** Опциональные параметры для настройки движка Babylon.js. */
  engineOptions?: EngineOptions;

  /** Опциональный параметр для адаптации к устройствам. */
  adaptToDeviceRatio?: boolean;

  /** Опциональные параметры для настройки сцены. */
  sceneOptions?: SceneOptions;

  /** Функция обратного вызова для процесса рендеринга. */
  onRender?: (scene: Scene) => void;

  /** Обязательная функция обратного вызова, вызываемая, когда сцена готова. */
  onSceneReady: (scene: Scene) => void;
};

const SceneComponent: React.FC<TScreenComponentProps> = props => {
  const { antialias, engineOptions, adaptToDeviceRatio, sceneOptions, onRender, onSceneReady, ...rest } = props;

  const reactCanvas = useRef(null);

  useEffect(() => {
    if (reactCanvas.current) {
      const engine = new Engine(reactCanvas.current, antialias, engineOptions, adaptToDeviceRatio);
      const scene = new Scene(engine, sceneOptions);

      if (scene.isReady()) {
        onSceneReady(scene);
      } else {
        scene.onReadyObservable.addOnce(scene => onSceneReady(scene));
      }

      engine.runRenderLoop(() => {
        if (typeof onRender === "function") {
          onRender(scene);
        }
        scene.render();
      });

      const resize = () => {
        scene.getEngine().resize();
      };

      if (window) {
        window.addEventListener("resize", resize);
      }

      return () => {
        scene.getEngine().dispose();

        if (window) {
          window.removeEventListener("resize", resize);
        }
      };
    }
  }, [reactCanvas]);

  return (
    <canvas
      ref={reactCanvas}
      {...rest}
    />
  );
};

export default SceneComponent;
