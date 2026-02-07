# 📦 Shared Packages

Reusable packages shared across web and mobile applications.

## Structure

```
packages/
├── shared-types/            # TypeScript types/interfaces
│   ├── src/
│   │   ├── models/         # Data model types
│   │   │   ├── user.ts
│   │   │   ├── homework.ts
│   │   │   ├── class.ts
│   │   │   └── notification.ts
│   │   ├── api/            # API request/response types
│   │   └── index.ts        # Public exports
│   └── package.json
├── ui-components/           # Shared UI components (web)
│   ├── src/
│   │   ├── Button/
│   │   ├── Input/
│   │   ├── Card/
│   │   ├── Modal/
│   │   └── index.ts
│   └── package.json
└── utils/                   # Shared utility functions
    ├── src/
    │   ├── date.ts         # Date formatting
    │   ├── validation.ts   # Input validation
    │   ├── formatting.ts   # Text formatting
    │   └── index.ts
    └── package.json
```

## Usage

```typescript
// In web or mobile app
import { User, Homework } from '@school/shared-types';
import { Button, Card } from '@school/ui-components';
import { formatDate, validateEmail } from '@school/utils';
```

## Benefits

- **Single Source of Truth**: Types defined once, used everywhere
- **Consistency**: Same utilities across all apps
- **Maintainability**: Update once, propagate everywhere
