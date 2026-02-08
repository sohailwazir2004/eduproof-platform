// Type Definitions Barrel Export

export type { LoginCredentials, RegisterData, TokenResponse, User } from '../services/authService';
export type { Homework, HomeworkCreate, HomeworkFilters } from '../services/homeworkService';
export type { Submission, SubmissionCreate, GradeSubmission, SubmissionFilters } from '../services/submissionService';
export type { Textbook, TextbookCreate, TextbookFilters } from '../services/textbookService';
export type {
  ClassStats,
  StudentStats,
  TeacherStats,
  SchoolStats,
  HomeworkCompletionData,
  GradeDistribution
} from '../services/analyticsService';
export type { Class, ClassCreate, ClassFilters, Student } from '../services/classService';

// Additional common types
export type UserRole = 'student' | 'teacher' | 'parent' | 'principal';

export type HomeworkStatus = 'active' | 'past_due' | 'completed' | 'draft';

export type SubmissionStatus = 'pending' | 'reviewed' | 'graded';

export interface FileUploadProgress {
  file: File;
  progress: number;
  status: 'pending' | 'uploading' | 'completed' | 'error';
  error?: string;
}

export interface PaginationParams {
  skip?: number;
  limit?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}

export interface SelectOption {
  value: string;
  label: string;
}
