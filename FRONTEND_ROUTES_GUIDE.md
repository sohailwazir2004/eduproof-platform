# Frontend Routes Configuration Guide

## Route Structure for React Router

This document provides the complete route configuration for the EduProof platform.

---

## App.tsx Route Configuration

```tsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import DashboardLayout from './components/layout/DashboardLayout';
import AuthLayout from './components/layout/AuthLayout';

// Auth Pages
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import ForgotPasswordPage from './pages/auth/ForgotPasswordPage';

// Dashboard Pages
import TeacherDashboard from './pages/dashboard/TeacherDashboard';
import StudentDashboard from './pages/dashboard/StudentDashboard';
import ParentDashboard from './pages/dashboard/ParentDashboard';
import PrincipalDashboard from './pages/dashboard/PrincipalDashboard';

// Homework Pages
import HomeworkListPage from './pages/homework/HomeworkListPage';
import HomeworkDetailPage from './pages/homework/HomeworkDetailPage';
import CreateHomeworkPage from './pages/homework/CreateHomeworkPage';

// Submission Pages
import SubmissionListPage from './pages/submissions/SubmissionListPage';
import SubmissionDetailPage from './pages/submissions/SubmissionDetailPage';
import SubmitHomeworkPage from './pages/submissions/SubmitHomeworkPage';

// Other Pages
import TextbookListPage from './pages/textbooks/TextbookListPage';
import TextbookViewerPage from './pages/textbooks/TextbookViewerPage';
import AnalyticsPage from './pages/analytics/AnalyticsPage';
import SettingsPage from './pages/settings/SettingsPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        </Route>

        {/* Protected Routes */}
        <Route element={<ProtectedRoute><DashboardLayout /></ProtectedRoute>}>
          {/* Dashboard Routes */}
          <Route path="/" element={<DashboardRouter />} />

          {/* Homework Routes */}
          <Route path="/homework" element={<HomeworkListPage />} />
          <Route path="/homework/:id" element={<HomeworkDetailPage />} />
          <Route path="/homework/:id/submit" element={<SubmitHomeworkPage />} />
          <Route path="/homework/create" element={<CreateHomeworkPage />} />
          <Route path="/homework/:id/edit" element={<CreateHomeworkPage />} />

          {/* Submission Routes */}
          <Route path="/submissions" element={<SubmissionListPage />} />
          <Route path="/submissions/:id" element={<SubmissionDetailPage />} />

          {/* Textbook Routes */}
          <Route path="/textbooks" element={<TextbookListPage />} />
          <Route path="/textbooks/:id" element={<TextbookViewerPage />} />

          {/* Analytics Routes */}
          <Route path="/analytics" element={<AnalyticsPage />} />

          {/* Settings Routes */}
          <Route path="/settings" element={<SettingsPage />} />
        </Route>

        {/* 404 Route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

// Dashboard Router - Redirects based on role
function DashboardRouter() {
  const userRole = authService.getUserRole();

  switch (userRole) {
    case 'teacher':
      return <TeacherDashboard />;
    case 'student':
      return <StudentDashboard />;
    case 'parent':
      return <ParentDashboard />;
    case 'principal':
      return <PrincipalDashboard />;
    default:
      return <Navigate to="/login" replace />;
  }
}

export default App;
```

---

## Complete Route List

### Authentication Routes (Public)
| Path | Component | Description |
|------|-----------|-------------|
| `/login` | LoginPage | User login page |
| `/register` | RegisterPage | User registration |
| `/forgot-password` | ForgotPasswordPage | Password reset request |

### Dashboard Routes (Protected)
| Path | Component | Access | Description |
|------|-----------|--------|-------------|
| `/` | TeacherDashboard | Teacher | Teacher home |
| `/` | StudentDashboard | Student | Student home |
| `/` | ParentDashboard | Parent | Parent home |
| `/` | PrincipalDashboard | Principal | Principal home |

### Homework Routes (Protected)
| Path | Component | Access | Description |
|------|-----------|--------|-------------|
| `/homework` | HomeworkListPage | All | List all homework |
| `/homework/:id` | HomeworkDetailPage | All | View homework details |
| `/homework/create` | CreateHomeworkPage | Teacher | Create new homework |
| `/homework/:id/edit` | CreateHomeworkPage | Teacher | Edit homework |
| `/homework/:id/submit` | SubmitHomeworkPage | Student | Submit homework |

### Submission Routes (Protected)
| Path | Component | Access | Description |
|------|-----------|--------|-------------|
| `/submissions` | SubmissionListPage | Teacher | List all submissions |
| `/submissions/:id` | SubmissionDetailPage | Teacher, Student | View submission details |

### Textbook Routes (Protected)
| Path | Component | Access | Description |
|------|-----------|--------|-------------|
| `/textbooks` | TextbookListPage | All | List all textbooks |
| `/textbooks/:id` | TextbookViewerPage | All | View textbook |

### Analytics Routes (Protected)
| Path | Component | Access | Description |
|------|-----------|--------|-------------|
| `/analytics` | AnalyticsPage | All | View analytics |

### Settings Routes (Protected)
| Path | Component | Access | Description |
|------|-----------|--------|-------------|
| `/settings` | SettingsPage | All | User settings |

---

## Navigation Structure

### Teacher Navigation
```tsx
const teacherNav = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/homework', label: 'Homework', icon: BookOpen },
  { path: '/submissions', label: 'Submissions', icon: FileText },
  { path: '/textbooks', label: 'Textbooks', icon: Book },
  { path: '/analytics', label: 'Analytics', icon: BarChart },
  { path: '/settings', label: 'Settings', icon: Settings }
];
```

### Student Navigation
```tsx
const studentNav = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/homework', label: 'Homework', icon: BookOpen },
  { path: '/textbooks', label: 'Textbooks', icon: Book },
  { path: '/settings', label: 'Settings', icon: Settings }
];
```

### Parent Navigation
```tsx
const parentNav = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/homework', label: 'Homework', icon: BookOpen },
  { path: '/analytics', label: 'Progress', icon: TrendingUp },
  { path: '/settings', label: 'Settings', icon: Settings }
];
```

### Principal Navigation
```tsx
const principalNav = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/analytics', label: 'Analytics', icon: BarChart },
  { path: '/homework', label: 'Homework', icon: BookOpen },
  { path: '/submissions', label: 'Submissions', icon: FileText },
  { path: '/settings', label: 'Settings', icon: Settings }
];
```

---

## Route Guards

### ProtectedRoute Component

```tsx
import { Navigate, useLocation } from 'react-router-dom';
import { authService } from '../services';

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles?: string[];
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  allowedRoles
}) => {
  const location = useLocation();
  const isAuthenticated = authService.isAuthenticated();
  const userRole = authService.getUserRole();

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (allowedRoles && !allowedRoles.includes(userRole)) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;
```

### Role-Based Route Usage

```tsx
// Teacher-only route
<Route
  path="/homework/create"
  element={
    <ProtectedRoute allowedRoles={['teacher']}>
      <CreateHomeworkPage />
    </ProtectedRoute>
  }
/>

// Multiple roles
<Route
  path="/analytics"
  element={
    <ProtectedRoute allowedRoles={['teacher', 'principal', 'parent']}>
      <AnalyticsPage />
    </ProtectedRoute>
  }
/>
```

---

## Navigation Helpers

### useNavigate Hook Examples

```tsx
import { useNavigate } from 'react-router-dom';

const navigate = useNavigate();

// Navigate to route
navigate('/homework');

// Navigate with state
navigate('/homework/create', { state: { from: 'dashboard' } });

// Navigate with replace (no back button)
navigate('/login', { replace: true });

// Go back
navigate(-1);

// Go forward
navigate(1);
```

### Link Component Examples

```tsx
import { Link } from 'react-router-dom';

// Basic link
<Link to="/homework">View Homework</Link>

// Link with styling
<Link
  to="/homework"
  className="text-primary-600 hover:text-primary-700"
>
  View Homework
</Link>

// Link with state
<Link
  to="/homework/123"
  state={{ from: 'dashboard' }}
>
  View Details
</Link>
```

---

## Query Parameters

### Reading Query Params

```tsx
import { useSearchParams } from 'react-router-dom';

const [searchParams] = useSearchParams();

const classId = searchParams.get('class');
const status = searchParams.get('status');
```

### Setting Query Params

```tsx
const [searchParams, setSearchParams] = useSearchParams();

setSearchParams({ class: 'class-123', status: 'active' });
```

---

## Breadcrumb Implementation

```tsx
import { Link, useLocation } from 'react-router-dom';

const Breadcrumbs: React.FC = () => {
  const location = useLocation();
  const paths = location.pathname.split('/').filter(Boolean);

  return (
    <nav className="flex items-center space-x-2 text-sm">
      <Link to="/" className="text-gray-600 hover:text-gray-900">
        Home
      </Link>
      {paths.map((path, index) => {
        const to = `/${paths.slice(0, index + 1).join('/')}`;
        const isLast = index === paths.length - 1;

        return (
          <React.Fragment key={to}>
            <span className="text-gray-400">/</span>
            {isLast ? (
              <span className="text-gray-900 font-medium capitalize">
                {path}
              </span>
            ) : (
              <Link
                to={to}
                className="text-gray-600 hover:text-gray-900 capitalize"
              >
                {path}
              </Link>
            )}
          </React.Fragment>
        );
      })}
    </nav>
  );
};
```

---

## Redirect Patterns

### After Login

```tsx
const location = useLocation();
const from = location.state?.from?.pathname || '/';

// After successful login
navigate(from, { replace: true });
```

### After Create/Edit

```tsx
// After creating homework
const homework = await homeworkService.createHomework(data);
navigate(`/homework/${homework.id}`);

// After editing
navigate(`/homework/${id}`);
```

### After Delete

```tsx
// After deleting homework
await homeworkService.deleteHomework(id);
navigate('/homework');
```

---

## 404 Handling

### Not Found Page

```tsx
const NotFoundPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
        <p className="text-xl text-gray-600 mb-8">Page not found</p>
        <Button onClick={() => navigate('/')}>
          Go to Dashboard
        </Button>
      </div>
    </div>
  );
};
```

---

## Sidebar Navigation Component

```tsx
import { NavLink } from 'react-router-dom';

const Sidebar: React.FC = () => {
  const userRole = authService.getUserRole();
  const navigation = getNavigationForRole(userRole);

  return (
    <aside className="w-64 bg-white border-r border-gray-200">
      <nav className="p-4 space-y-2">
        {navigation.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-2 rounded-lg transition-colors ${
                isActive
                  ? 'bg-primary-50 text-primary-600'
                  : 'text-gray-700 hover:bg-gray-100'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};
```

---

## Route Transition Animation

```tsx
import { useLocation } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';

const AnimatedRoutes: React.FC = () => {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={location.pathname}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.2 }}
      >
        <Routes location={location}>
          {/* Routes here */}
        </Routes>
      </motion.div>
    </AnimatePresence>
  );
};
```

---

## Testing Routes

### Example Test

```tsx
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import HomeworkListPage from './HomeworkListPage';

test('renders homework list page', () => {
  render(
    <BrowserRouter>
      <HomeworkListPage />
    </BrowserRouter>
  );

  expect(screen.getByText('Homework')).toBeInTheDocument();
});
```

---

## Environment-Specific Routes

### Development

```tsx
// Show dev tools in development
{process.env.NODE_ENV === 'development' && (
  <Route path="/dev-tools" element={<DevTools />} />
)}
```

### Production

```tsx
// Redirect all unknown routes to 404
<Route path="*" element={<NotFoundPage />} />
```

---

## Deep Linking Support

For mobile app or PWA support, ensure all routes are:
- Shareable via URL
- Bookmarkable
- Supports browser back/forward
- Maintains state via URL params

---

**Last Updated:** February 8, 2026
