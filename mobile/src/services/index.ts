// Services Barrel Export

export { default as api } from './api';
export { default as authService } from './authService';
export { default as homeworkService } from './homeworkService';
export { default as submissionService } from './submissionService';

// Export types
export type { LoginCredentials, RegisterData, TokenResponse, User } from './authService';
export type { Homework, HomeworkFilters, HomeworkDetail } from './homeworkService';
export type { Submission, SubmissionFilters, ImageData, UploadProgress } from './submissionService';
