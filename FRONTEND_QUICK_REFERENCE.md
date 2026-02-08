# Frontend Quick Reference Guide - EduProof

## Quick Links to Implemented Pages

### Dashboard Pages
- **Teacher Dashboard**: `frontend/src/pages/dashboard/TeacherDashboard.tsx`
- **Student Dashboard**: `frontend/src/pages/dashboard/StudentDashboard.tsx`
- **Parent Dashboard**: `frontend/src/pages/dashboard/ParentDashboard.tsx`
- **Principal Dashboard**: `frontend/src/pages/dashboard/PrincipalDashboard.tsx`

### Homework Pages
- **Homework List**: `frontend/src/pages/homework/HomeworkListPage.tsx`
- **Homework Detail**: `frontend/src/pages/homework/HomeworkDetailPage.tsx`
- **Create Homework**: `frontend/src/pages/homework/CreateHomeworkPage.tsx`

### Submission Pages
- **Submission List**: `frontend/src/pages/submissions/SubmissionListPage.tsx`
- **Submission Detail**: `frontend/src/pages/submissions/SubmissionDetailPage.tsx`
- **Submit Homework**: `frontend/src/pages/submissions/SubmitHomeworkPage.tsx`

### Common Components
- **FileUpload**: `frontend/src/components/common/FileUpload.tsx`
- **Charts**: `frontend/src/components/common/Charts.tsx`

---

## Component Usage Examples

### FileUpload Component

```tsx
import FileUpload from '../../components/common/FileUpload';

<FileUpload
  accept="image/*,application/pdf"
  multiple={false}
  maxSize={10}
  onFilesSelected={(files) => setSelectedFiles(files)}
  onUpload={async (files) => {
    // Handle upload
  }}
/>
```

### LineChart Component

```tsx
import { LineChart } from '../../components/common/Charts';

<LineChart
  data={chartData}
  xAxisKey="date"
  dataKey="value"
  color="#3B82F6"
  height={300}
/>
```

### DonutChart Component

```tsx
import { DonutChart } from '../../components/common/Charts';

<DonutChart
  data={[
    { name: 'Completed', value: 30 },
    { name: 'Pending', value: 10 }
  ]}
  dataKey="value"
  nameKey="name"
  height={250}
/>
```

---

## API Service Usage

### Homework Service

```tsx
import { homeworkService } from '../../services';

// Get homework list
const homework = await homeworkService.getHomeworkList({
  class_id: 'class-123',
  status: 'active'
});

// Get single homework
const hw = await homeworkService.getHomework('hw-123');

// Create homework
const newHw = await homeworkService.createHomework({
  title: 'Math Homework',
  class_id: 'class-123',
  due_date: '2026-02-15T23:59:00'
});

// Get submissions
const subs = await homeworkService.getHomeworkSubmissions('hw-123');
```

### Submission Service

```tsx
import { submissionService } from '../../services';

// Get submissions
const submissions = await submissionService.getSubmissions({
  homework_id: 'hw-123',
  status: 'pending'
});

// Create submission
const sub = await submissionService.createSubmission('hw-123', file);

// Grade submission
await submissionService.gradeSubmission('sub-123', {
  grade: 95,
  teacher_feedback: 'Excellent work!'
});
```

### Analytics Service

```tsx
import { analyticsService } from '../../services';

// Get student stats
const stats = await analyticsService.getStudentStats('student-123');

// Get teacher stats
const teacherStats = await analyticsService.getTeacherStats('teacher-123');

// Get school stats
const schoolStats = await analyticsService.getSchoolStats();
```

---

## React Query Patterns

### Basic Query

```tsx
const { data, isLoading, error } = useQuery({
  queryKey: ['homework-list'],
  queryFn: () => homeworkService.getHomeworkList()
});
```

### Query with Parameters

```tsx
const { data } = useQuery({
  queryKey: ['homework', homeworkId],
  queryFn: () => homeworkService.getHomework(homeworkId),
  enabled: !!homeworkId
});
```

### Mutation

```tsx
const mutation = useMutation({
  mutationFn: (data) => homeworkService.createHomework(data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['homework-list'] });
    navigate('/homework');
  }
});
```

---

## Form Validation with Zod

### Basic Schema

```tsx
import { z } from 'zod';

const homeworkSchema = z.object({
  title: z.string().min(1, 'Title is required'),
  description: z.string().optional(),
  class_id: z.string().min(1, 'Class is required'),
  due_date: z.string().min(1, 'Due date is required')
});

type HomeworkFormData = z.infer<typeof homeworkSchema>;
```

### React Hook Form Integration

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const {
  register,
  handleSubmit,
  formState: { errors }
} = useForm<HomeworkFormData>({
  resolver: zodResolver(homeworkSchema)
});

const onSubmit = (data: HomeworkFormData) => {
  // Handle form submission
};
```

---

## Common Patterns

### Status Badge

```tsx
const getStatusBadge = (status: string) => {
  const badges = {
    graded: 'bg-green-100 text-green-700',
    pending: 'bg-yellow-100 text-yellow-700',
    reviewed: 'bg-blue-100 text-blue-700'
  };

  return (
    <span className={`px-2 py-1 text-xs font-medium rounded-full ${badges[status]}`}>
      {status}
    </span>
  );
};
```

### Empty State

```tsx
<div className="text-center py-12">
  <Icon className="w-12 h-12 mx-auto mb-3 text-gray-300" />
  <p className="text-gray-500">No data available</p>
  <Button onClick={action} className="mt-4">
    Take Action
  </Button>
</div>
```

### Loading State

```tsx
{isLoading ? (
  <div className="flex items-center justify-center h-64">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
  </div>
) : (
  <Content />
)}
```

---

## Styling Guidelines

### Color Palette

```css
/* Primary Colors */
primary-50: #EFF6FF
primary-100: #DBEAFE
primary-600: #2563EB
primary-700: #1D4ED8

/* Status Colors */
green: Success, Completed, Graded
yellow: Warning, Pending, Due Soon
red: Error, Overdue, Danger
blue: Info, Reviewed
purple: Analytics, Performance
```

### Common Classes

```css
/* Cards */
border border-gray-200 rounded-lg p-6

/* Buttons */
px-4 py-2 rounded-lg font-medium

/* Input Fields */
w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500

/* Text */
text-gray-900 (headings)
text-gray-600 (body)
text-gray-500 (labels)
```

---

## Date Formatting

```tsx
import { format } from 'date-fns';

// Short date
format(new Date(date), 'MMM dd, yyyy')
// Output: Feb 08, 2026

// Full date with time
format(new Date(date), 'MMMM dd, yyyy hh:mm a')
// Output: February 08, 2026 03:30 PM

// Date difference
import { differenceInDays } from 'date-fns';
const daysUntilDue = differenceInDays(new Date(dueDate), new Date());
```

---

## Navigation Patterns

### useNavigate Hook

```tsx
import { useNavigate } from 'react-router-dom';

const navigate = useNavigate();

// Navigate to route
navigate('/homework');

// Navigate with ID
navigate(`/homework/${id}`);

// Go back
navigate(-1);
```

### Route Parameters

```tsx
import { useParams } from 'react-router-dom';

const { id } = useParams<{ id: string }>();
```

---

## User Role Access

### Get Current User Info

```tsx
import { authService } from '../../services';

const userRole = authService.getUserRole();
const userId = authService.getUserId();
const isAuthenticated = authService.isAuthenticated();
```

### Role-Based Rendering

```tsx
{userRole === 'teacher' && (
  <Button onClick={handleCreate}>Create Homework</Button>
)}

{userRole === 'student' && (
  <Button onClick={handleSubmit}>Submit Homework</Button>
)}
```

---

## Error Handling

### Try-Catch Pattern

```tsx
const handleDelete = async (id: string) => {
  try {
    await homeworkService.deleteHomework(id);
    // Success
    queryClient.invalidateQueries(['homework-list']);
  } catch (error) {
    console.error('Failed to delete:', error);
    alert('Failed to delete homework');
  }
};
```

### Mutation Error Handling

```tsx
const mutation = useMutation({
  mutationFn: createHomework,
  onSuccess: () => {
    // Handle success
  },
  onError: (error) => {
    console.error('Error:', error);
    alert('Operation failed');
  }
});
```

---

## File Upload Handling

### Single File Upload

```tsx
const [file, setFile] = useState<File | null>(null);

<FileUpload
  multiple={false}
  onFilesSelected={(files) => setFile(files[0])}
/>

// Submit
const formData = new FormData();
formData.append('file', file);
await api.post('/upload', formData);
```

### Multiple Files

```tsx
const [files, setFiles] = useState<File[]>([]);

<FileUpload
  multiple={true}
  onFilesSelected={setFiles}
/>
```

---

## TypeScript Tips

### Service Response Types

```tsx
// Import types from services
import type { Homework, Submission, User } from '../../types';

// Use in component state
const [homework, setHomework] = useState<Homework | null>(null);
const [submissions, setSubmissions] = useState<Submission[]>([]);
```

### Props Interface

```tsx
interface ComponentProps {
  title: string;
  onSave: (data: FormData) => void;
  optional?: boolean;
}

const Component: React.FC<ComponentProps> = ({ title, onSave, optional }) => {
  // Component logic
};
```

---

## Performance Tips

1. **Use Query Keys Properly**: Include all dependencies in query keys
2. **Enable Queries Conditionally**: Use `enabled` option
3. **Debounce Search**: Use setTimeout for search inputs
4. **Memoize Expensive Calculations**: Use useMemo
5. **Lazy Load Images**: Use loading="lazy"

---

## Debugging Tips

### React Query DevTools

```tsx
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

<ReactQueryDevtools initialIsOpen={false} />
```

### Console Logging

```tsx
// Log query data
useEffect(() => {
  console.log('Homework data:', homework);
}, [homework]);

// Log errors
onError: (error) => {
  console.error('API Error:', error);
}
```

---

## Testing Checklist

- [ ] All forms validate correctly
- [ ] Loading states show properly
- [ ] Error messages display
- [ ] Empty states render
- [ ] Navigation works
- [ ] Role-based features work
- [ ] File uploads function
- [ ] Charts render data
- [ ] Responsive on mobile
- [ ] Accessible via keyboard

---

## Common Issues & Solutions

### Issue: Query not refetching
**Solution**: Check query key dependencies and use `invalidateQueries`

### Issue: Form validation not working
**Solution**: Verify Zod schema matches form fields

### Issue: Navigation not working
**Solution**: Check route configuration and path parameters

### Issue: Images not loading
**Solution**: Verify API returns full URLs, not relative paths

### Issue: Charts not displaying
**Solution**: Ensure data format matches chart requirements

---

## Additional Resources

- React Query Docs: https://tanstack.com/query/latest
- React Hook Form: https://react-hook-form.com/
- Zod Validation: https://zod.dev/
- Tailwind CSS: https://tailwindcss.com/
- Recharts: https://recharts.org/

---

**Last Updated:** February 8, 2026
