# 📱 Mobile App

React Native + Expo application for Students and Parents.

## Structure

```
mobile/
├── src/
│   ├── components/           # Reusable components
│   │   ├── common/          # Buttons, inputs, cards
│   │   ├── screens/         # Screen-specific components
│   │   └── navigation/      # Navigation components
│   ├── screens/             # App screens
│   │   ├── student/         # Student-specific screens
│   │   ├── parent/          # Parent-specific screens
│   │   ├── auth/            # Login, register screens
│   │   └── homework/        # Homework screens
│   │       ├── list/        # Homework list
│   │       ├── detail/      # Homework detail view
│   │       ├── submission/  # Submit homework
│   │       └── camera/      # Camera capture for OCR
│   ├── hooks/               # Custom hooks
│   ├── utils/               # Helper functions
│   ├── services/            # API services
│   ├── store/               # State management
│   ├── types/               # TypeScript types
│   └── assets/              # Images, icons, fonts
├── tests/                   # Test files
├── app.json                 # Expo config
├── babel.config.js
└── package.json
```

## Key Features

- **Camera Integration**: Capture homework photos for OCR
- **Push Notifications**: Real-time homework updates
- **Offline Support**: View cached homework offline
- **Parent Mode**: Track child's homework progress

## Development

```bash
npm install
npx expo start
```

## Build

```bash
npx expo build:android
npx expo build:ios
```
