/// <reference types="vite/client" />

interface ImportMetaEnv {
  VITE_MAPBOX_TOKEN: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
