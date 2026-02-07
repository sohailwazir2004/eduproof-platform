# Mobile - EduProof Mobile App

## Overview
React Native + Expo mobile application for Students and Parents.

## Tech Stack
- React Native
- Expo SDK
- React Navigation v6
- React Query
- Zustand
- Expo Camera (for homework submission)
- Expo Notifications

## Structure
```
mobile/
├── src/
│   ├── screens/      # Screen components
│   ├── components/   # Reusable UI components
│   ├── navigation/   # Navigation configuration
│   ├── hooks/        # Custom React hooks
│   ├── services/     # API service functions
│   ├── stores/       # Zustand state stores
│   ├── utils/        # Helper utilities
│   ├── types/        # TypeScript type definitions
│   └── assets/       # Static assets
├── app.json          # Expo configuration
└── tests/            # Component and E2E tests
```

## Setup
1. Install dependencies: `npm install`
2. Configure `.env` file
3. Start Expo: `npx expo start`
4. Run on device: Scan QR with Expo Go app
