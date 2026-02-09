# Mobile App Deployment Guide (Expo EAS)

## Overview

EduProof mobile app is built with React Native + Expo. Deployment options:
- **Development Build**: Testing on physical devices
- **Preview Build**: Internal testing (APK/IPA)
- **Production Build**: App Store / Play Store submission

## Pre-deployment Checklist

- [ ] Backend API deployed and accessible
- [ ] Expo account created
- [ ] EAS CLI installed
- [ ] iOS: Apple Developer account ($99/year)
- [ ] Android: Google Play Developer account ($25 one-time)

## Setup

### 1. Install EAS CLI

```bash
npm install -g eas-cli
```

### 2. Login to Expo

```bash
eas login
```

### 3. Configure Project

```bash
cd mobile
eas init
```

This creates/updates:
- `eas.json` (already provided)
- Project ID in Expo dashboard

### 4. Update Configuration

Edit `eas.json` and replace placeholder URLs:

```json
{
  "build": {
    "preview": {
      "env": {
        "EXPO_PUBLIC_API_BASE_URL": "https://your-backend.railway.app/api/v1"
      }
    },
    "production": {
      "env": {
        "EXPO_PUBLIC_API_BASE_URL": "https://your-backend.railway.app/api/v1"
      }
    }
  }
}
```

## Building

### Development Build (for testing)

Build for Android:
```bash
eas build --profile development --platform android
```

Build for iOS (requires macOS or EAS cloud build):
```bash
eas build --profile development --platform ios
```

Install on device:
1. Download from Expo dashboard
2. Install APK (Android) or IPA via TestFlight (iOS)
3. Run `npx expo start --dev-client`

### Preview Build (internal testing)

Android APK (shareable):
```bash
eas build --profile preview --platform android
```

iOS (TestFlight):
```bash
eas build --profile preview --platform ios
```

### Production Build

Build for both platforms:
```bash
eas build --profile production --platform all
```

Or individually:
```bash
eas build --profile production --platform android
eas build --profile production --platform ios
```

## Build Status

Check build status:
```bash
eas build:list
```

Or visit: https://expo.dev/accounts/[your-account]/projects/eduproof/builds

## Submission to Stores

### Google Play Store

#### 1. Prepare Store Listing
- App name, description, screenshots
- Privacy policy URL (required)
- Content rating questionnaire

#### 2. Create Service Account (for automated submission)
1. Google Play Console → Setup → API access
2. Create service account
3. Download JSON key
4. Save as `google-service-account.json`

#### 3. Submit via EAS
```bash
eas submit --platform android
```

Or manually:
1. Download AAB from EAS dashboard
2. Upload to Google Play Console
3. Create release in Production/Internal testing track

### Apple App Store

#### 1. Prepare Store Listing
- App Store Connect: Create app record
- Screenshots, description, keywords
- Privacy policy URL

#### 2. Configure App Store Connect
Update `eas.json` with your Apple credentials:
```json
{
  "submit": {
    "production": {
      "ios": {
        "appleId": "your-email@example.com",
        "ascAppId": "1234567890",
        "appleTeamId": "TEAM123"
      }
    }
  }
}
```

#### 3. Submit via EAS
```bash
eas submit --platform ios
```

Or manually:
1. Download IPA from EAS
2. Upload via Transporter app or Xcode
3. Submit for review in App Store Connect

## Over-the-Air (OTA) Updates

After initial app store release, push updates without rebuilding:

### Publish Update
```bash
eas update --branch production --message "Bug fixes"
```

### For Different Environments
```bash
eas update --branch preview --message "Test new feature"
eas update --branch production --message "Release v1.1"
```

### Update Strategy
- Minor fixes, UI changes: OTA update
- Native code changes, new permissions: New build required

## Testing

### Internal Testing

1. **Android**: Share preview APK directly
   ```bash
   eas build --profile preview --platform android
   ```
   Download link appears in terminal and dashboard.

2. **iOS**: Use TestFlight
   ```bash
   eas build --profile preview --platform ios
   eas submit --platform ios
   ```
   Add testers in App Store Connect → TestFlight.

### Testing Checklist

- [ ] Login/authentication works
- [ ] API calls succeed (check backend URL)
- [ ] Camera permissions granted
- [ ] Image upload works
- [ ] Notifications display correctly
- [ ] Offline behavior acceptable
- [ ] Performance acceptable on low-end devices

## Environment Configuration

### Local Development (.env)
```env
EXPO_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
EXPO_PUBLIC_APP_ENV=development
```

### Preview/Production (eas.json)
Environment variables set in `eas.json` under each build profile.

### Access in Code
```typescript
const API_URL = process.env.EXPO_PUBLIC_API_BASE_URL;
```

## App Icons & Splash Screens

Ensure these assets exist:
- `assets/icon.png` (1024x1024)
- `assets/splash.png` (1284x2778 for iPhone 13 Pro Max)
- `assets/adaptive-icon.png` (1024x1024, Android)
- `assets/notification-icon.png` (96x96, transparent)

Generate all sizes:
```bash
npx expo install expo-asset
```

## Credentials Management

### Automatic (Recommended)
EAS manages certificates and provisioning profiles:
```bash
eas credentials
```

### Manual
Store credentials in Expo dashboard or locally.

For iOS:
- Distribution certificate
- Provisioning profile

For Android:
- Upload keystore
- Or let EAS generate one

## Monitoring & Analytics

### Crash Reporting

Add Sentry:
```bash
npx expo install sentry-expo
```

Configure in `app.json`:
```json
{
  "expo": {
    "plugins": [
      [
        "sentry-expo",
        {
          "organization": "your-org",
          "project": "eduproof-mobile"
        }
      ]
    ]
  }
}
```

### Usage Analytics

Add Expo Analytics or Firebase Analytics:
```bash
npx expo install expo-firebase-analytics
```

## Versioning

Before each release:

1. Update version in `app.json`:
```json
{
  "version": "1.0.1",
  "android": {
    "versionCode": 2
  },
  "ios": {
    "buildNumber": "1.0.1"
  }
}
```

2. Commit changes:
```bash
git add .
git commit -m "Bump version to 1.0.1"
git tag v1.0.1
```

## Troubleshooting

### Build Fails

Check logs:
```bash
eas build:list
# Click build ID to view logs
```

Common issues:
- Missing credentials: Run `eas credentials`
- Invalid package name: Check `app.json`
- Dependency conflicts: Update packages

### API Connection Fails

1. Check `EXPO_PUBLIC_API_BASE_URL` in `eas.json`
2. Verify backend is accessible from mobile network
3. Test with `curl` or Postman
4. Check CORS settings on backend

### Camera/Permissions Not Working

1. Verify permissions in `app.json`
2. Request permissions at runtime:
```typescript
const { status } = await Camera.requestCameraPermissionsAsync();
```

### OTA Update Not Applying

1. Check branch matches:
```bash
eas channel:list
```

2. Force reload:
```typescript
import * as Updates from 'expo-updates';
await Updates.fetchUpdateAsync();
await Updates.reloadAsync();
```

## Cost Estimation

### Expo EAS
- Free tier: Limited builds/month
- Production: $29/month (unlimited builds)
- Enterprise: Custom pricing

### App Stores
- Apple: $99/year
- Google: $25 one-time

### Optional Services
- Push notifications: Free (Expo Push)
- Sentry: Free tier available
- Analytics: Free (Firebase)

## Release Checklist

Before submitting to stores:

- [ ] Test on multiple devices (iOS + Android)
- [ ] Verify all features work in production build
- [ ] Update version numbers
- [ ] Create release notes
- [ ] Prepare store screenshots (required sizes)
- [ ] Write app description
- [ ] Create privacy policy
- [ ] Test payment flows (if applicable)
- [ ] Enable crash reporting
- [ ] Set up analytics

## Best Practices

1. **Always test preview builds** before production
2. **Use OTA updates** for quick fixes
3. **Monitor crash reports** after releases
4. **Keep development build** for testing
5. **Version consistently** across platforms
6. **Test on real devices** not just simulators
7. **Follow store guidelines** to avoid rejection

## Support

- Expo Docs: https://docs.expo.dev
- EAS Build: https://docs.expo.dev/build/introduction
- EAS Submit: https://docs.expo.dev/submit/introduction
- Expo Forums: https://forums.expo.dev
