import React from "react";

import { type AbstractMesh, FreeCamera, HemisphericLight, MeshBuilder, Scene, Vector3 } from "@babylonjs/core";

import MapComponent from "./Map";
import SceneComponent from "./SceneComponent";

export const StartPage: React.FC = () => {
  let box: AbstractMesh | undefined;

  /**
   * Вызывается, когда сцена готова для рендеринга.
   *
   * @param scene - Сцена, которая будет использоваться для рендеринга.
   */
  const onSceneReady = (scene: Scene) => {
    /**
     * Создает и позиционирует свободную камеру (без меша).
     */
    const camera = new FreeCamera("camera1", new Vector3(0, 5, -10), scene);

    /**
     * Нацеливает камеру на исходную точку сцены.
     */
    camera.setTarget(Vector3.Zero());

    const canvas = scene.getEngine().getRenderingCanvas();

    /**
     * Прикрепляет камеру к холсту (canvas).
     */
    camera.attachControl(canvas, true);

    /**
     * Создает свет, направленный 0,1,0 - в небо (без сетки).
     */
    const light = new HemisphericLight("light", new Vector3(0, 1, 0), scene);

    /**
     * Устанавливает интенсивность света.
     */
    light.intensity = 0.8;

    /**
     * Создает встроенную форму "box".
     */
    box = MeshBuilder.CreateBox("box", { size: 2 }, scene);

    /**
     * Перемещает коробку вверх на 1/2 ее высоты.
     */
    if (box) {
      box.position.y = 1;
    }

    /**
     * Создает встроенную форму "ground".
     */
    MeshBuilder.CreateGround("ground", { width: 6, height: 6 }, scene);
  };

  /**
   * Вызывается при рендеринге каждого кадра. Вращает коробку по оси y.
   *
   * @param scene - Сцена, которая будет использоваться для рендеринга.
   */
  const onRender = (scene: Scene) => {
    if (box) {
      const deltaTimeInMillis = scene.getEngine().getDeltaTime();
      const rpm = 10;

      box.rotation.y += (rpm / 60) * Math.PI * 2 * (deltaTimeInMillis / 1000);
    }
  };

  return (
    <div>
      <SceneComponent
        antialias
        onSceneReady={onSceneReady}
        onRender={onRender}
      />
      <MapComponent />
    </div>
  );
};
