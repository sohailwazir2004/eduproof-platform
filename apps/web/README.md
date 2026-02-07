# 🌐 Web Dashboard

React + Vite + Tailwind CSS application for Teacher, Parent, and Principal dashboards.

## Structure

```
web/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── common/         # Buttons, inputs, modals, cards
│   │   ├── dashboard/      # Dashboard-specific widgets
│   │   │   ├── teacher/    # Teacher dashboard components
│   │   │   ├── parent/     # Parent dashboard components
│   │   │   ├── principal/  # Principal dashboard components
│   │   │   └── widgets/    # Shared dashboard widgets
│   │   ├── auth/           # Login, register, password reset
│   │   ├── homework/       # Homework management components
│   │   │   ├── list/       # Homework listing
│   │   │   ├── detail/     # Single homework view
│   │   │   ├── submission/ # Submission viewing
│   │   │   └── grading/    # Grading interface
│   │   ├── notifications/  # Notification components
│   │   └── layout/         # Header, sidebar, footer
│   ├── pages/              # Route pages
│   │   ├── teacher/        # Teacher portal pages
│   │   ├── parent/         # Parent portal pages
│   │   ├── principal/      # Principal portal pages
│   │   └── auth/           # Authentication pages
│   ├── hooks/              # Custom React hooks
│   ├── utils/              # Helper functions
│   ├── services/           # API service layers
│   ├── store/              # State management (Zustand/Redux)
│   ├── types/              # TypeScript types/interfaces
│   ├── assets/             # Static assets
│   └── styles/             # Global styles, Tailwind config
├── public/                 # Static public files
├── index.html
├── vite.config.ts
├── tailwind.config.js
└── package.json
```

## Development

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```
