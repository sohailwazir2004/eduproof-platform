// API Services Barrel Export

export { default as api } from './api';
export { default as authService } from './authService';
export { default as homeworkService } from './homeworkService';
export { default as submissionService } from './submissionService';
export { default as textbookService } from './textbookService';
export { default as analyticsService } from './analyticsService';
export { default as classService } from './classService';

// Export types
export type { LoginCredentials, RegisterData, TokenResponse, User } from './authService';
export type { Homework, HomeworkCreate, HomeworkFilters } from './homeworkService';
export type { Submission, SubmissionCreate, GradeSubmission } from './submissionService';
export type { Textbook, TextbookCreate, TextbookFilters } from './textbookService';
export type { ClassStats, StudentStats, TeacherStats, SchoolStats } from './analyticsService';
export type { Class, ClassCreate, ClassFilters, Student } from './classService';
