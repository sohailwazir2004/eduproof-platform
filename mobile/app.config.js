// app.config.js - Dynamic Expo Configuration
// Allows environment variables to be used in app.json

export default {
  expo: {
    name: "EduProof",
    slug: "eduproof",
    version: "1.0.0",
    orientation: "portrait",
    icon: "./assets/icon.png",
    userInterfaceStyle: "automatic",
    splash: {
      image: "./assets/splash.png",
      resizeMode: "contain",
      backgroundColor: "#ffffff"
    },
    assetBundlePatterns: [
      "**/*"
    ],
    ios: {
      supportsTablet: true,
      bundleIdentifier: "com.eduproof.app",
      infoPlist: {
        NSCameraUsageDescription: "EduProof needs camera access to capture homework submissions.",
        NSPhotoLibraryUsageDescription: "EduProof needs photo library access to upload homework images."
      }
    },
    android: {
      adaptiveIcon: {
        foregroundImage: "./assets/adaptive-icon.png",
        backgroundColor: "#ffffff"
      },
      package: "com.eduproof.app",
      permissions: [
        "CAMERA",
        "READ_EXTERNAL_STORAGE",
        "WRITE_EXTERNAL_STORAGE"
      ]
    },
    plugins: [
      [
        "expo-camera",
        {
          cameraPermission: "Allow EduProof to access your camera to capture homework."
        }
      ],
      [
        "expo-notifications",
        {
          icon: "./assets/notification-icon.png",
          color: "#ffffff"
        }
      ]
    ],
    extra: {
      eas: {
        projectId: process.env.EAS_PROJECT_ID || "your-project-id"
      },
      apiBaseUrl: process.env.EXPO_PUBLIC_API_BASE_URL,
      appEnv: process.env.EXPO_PUBLIC_APP_ENV
    }
  }
};
