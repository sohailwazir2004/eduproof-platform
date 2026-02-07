// submissionService.ts - Submission API Service
//
// API calls for submission endpoints.

import api from './api';

/**
 * Submission Service
 *
 * Methods:
 * - getSubmissions(filters) - GET /submissions
 * - getSubmission(id) - GET /submissions/:id
 * - createSubmission(homeworkId, file) - POST /submissions
 * - gradeSubmission(id, grade, feedback) - PUT /submissions/:id/grade
 * - getAIAnalysis(id) - GET /submissions/:id/ai-analysis
 */

export interface Submission {
  id: string;
  homework_id: string;
  student_id: string;
  file_url: string;
  file_type: string;
  status: 'pending' | 'reviewed' | 'graded';
  grade?: number;
  teacher_feedback?: string;
  ai_analysis?: string;
  submitted_at: string;
  reviewed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface SubmissionCreate {
  homework_id: string;
  file: File;
}

export interface GradeSubmission {
  grade: number;
  teacher_feedback?: string;
}

export interface SubmissionFilters {
  homework_id?: string;
  student_id?: string;
  status?: string;
  skip?: number;
  limit?: number;
}

class SubmissionService {
  /**
   * Get list of submissions with filters
   */
  async getSubmissions(filters?: SubmissionFilters): Promise<Submission[]> {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await api.get<Submission[]>(`/submissions?${params.toString()}`);
    return response.data;
  }

  /**
   * Get submission by ID
   */
  async getSubmission(id: string): Promise<Submission> {
    const response = await api.get<Submission>(`/submissions/${id}`);
    return response.data;
  }

  /**
   * Create new submission (file upload)
   */
  async createSubmission(homework_id: string, file: File): Promise<Submission> {
    const formData = new FormData();
    formData.append('homework_id', homework_id);
    formData.append('file', file);

    const response = await api.post<Submission>('/submissions', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  /**
   * Grade submission
   */
  async gradeSubmission(id: string, data: GradeSubmission): Promise<Submission> {
    const response = await api.put<Submission>(`/submissions/${id}/grade`, data);
    return response.data;
  }

  /**
   * Add feedback to submission
   */
  async addFeedback(id: string, feedback: string): Promise<Submission> {
    const response = await api.put<Submission>(`/submissions/${id}/feedback`, { feedback });
    return response.data;
  }

  /**
   * Get AI analysis for submission
   */
  async getAIAnalysis(id: string): Promise<any> {
    const response = await api.get<any>(`/submissions/${id}/ai-analysis`);
    return response.data;
  }

  /**
   * Delete submission
   */
  async deleteSubmission(id: string): Promise<void> {
    await api.delete(`/submissions/${id}`);
  }
}

export default new SubmissionService();
