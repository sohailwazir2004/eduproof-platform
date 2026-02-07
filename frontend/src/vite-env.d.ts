/// <reference types="vite/client" />

// Vite environment variable types
interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_FIREBASE_API_KEY: string
  readonly VITE_FIREBASE_PROJECT_ID: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
