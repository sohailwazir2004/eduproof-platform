// Submission Type Definitions
export enum SubmissionStatus {
  NOT_SUBMITTED = 'not_submitted',
  SUBMITTED = 'submitted',
  UNDER_REVIEW = 'under_review',
  GRADED = 'graded',
  RESUBMIT_REQUIRED = 'resubmit_required',
}

export interface Submission {
  id: string;
  homework_id: string;
  homework_title?: string;
  student_id: string;
  student_name?: string;
  status: SubmissionStatus;
  submitted_at?: string;
  graded_at?: string;
  graded_by?: string;
  score?: number;
  max_score?: number;
  feedback?: string;
  ai_analysis?: AIAnalysis;
  files: SubmissionFile[];
  created_at: string;
  updated_at: string;
}

export interface SubmissionFile {
  id: string;
  submission_id: string;
  file_name: string;
  file_url: string;
  file_type: string;
  file_size: number;
  page_number?: number;
  uploaded_at: string;
}

export interface AIAnalysis {
  completeness_score: number;
  clarity_score: number;
  accuracy_score: number;
  suggestions: string[];
  detected_issues: string[];
  estimated_grade: number;
  confidence: number;
  analyzed_at: string;
}

export interface CreateSubmissionRequest {
  homework_id: string;
  files: File[];
  notes?: string;
}

export interface GradeSubmissionRequest {
  score: number;
  feedback: string;
}

export interface SubmissionFilters {
  homework_id?: string;
  student_id?: string;
  status?: SubmissionStatus;
  date_from?: string;
  date_to?: string;
}
