// submissionService.ts - Submission Service
//
// Submission API calls for mobile with image upload support.

import api from './api';

/**
 * Submission Service for Students
 *
 * Methods:
 * - getSubmissions(filters) - GET /submissions
 * - getSubmission(id) - GET /submissions/:id
 * - submitHomework(homeworkId, images) - POST /submissions (with progress)
 * - getMySubmissions() - GET /submissions/my
 * - deleteSubmission(id) - DELETE /submissions/:id
 */

export interface Submission {
  id: string;
  homework_id: string;
  homework_title?: string;
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

export interface SubmissionFilters {
  homework_id?: string;
  status?: string;
  skip?: number;
  limit?: number;
}

export interface SubmitHomeworkData {
  homework_id: string;
  images: ImageData[];
}

export interface ImageData {
  uri: string;
  type: string;
  name: string;
}

export interface UploadProgress {
  loaded: number;
  total: number;
  percentage: number;
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
   * Submit homework with images
   * Supports upload progress tracking
   */
  async submitHomework(
    homework_id: string,
    images: ImageData[],
    onProgress?: (progress: UploadProgress) => void
  ): Promise<Submission> {
    const formData = new FormData();
    formData.append('homework_id', homework_id);

    // Add each image to form data
    images.forEach((image, index) => {
      const file = {
        uri: image.uri,
        type: image.type || 'image/jpeg',
        name: image.name || `homework_${index}.jpg`,
      } as any;

      formData.append('files', file);
    });

    const response = await api.post<Submission>('/submissions', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const percentage = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress({
            loaded: progressEvent.loaded,
            total: progressEvent.total,
            percentage,
          });
        }
      },
    });

    return response.data;
  }

  /**
   * Get current student's submissions
   */
  async getMySubmissions(filters?: { status?: string }): Promise<Submission[]> {
    const params = new URLSearchParams();
    if (filters?.status) {
      params.append('status', filters.status);
    }

    const response = await api.get<Submission[]>(`/submissions/my?${params.toString()}`);
    return response.data;
  }

  /**
   * Get submission history for a homework
   */
  async getHomeworkSubmissions(homeworkId: string): Promise<Submission[]> {
    const response = await api.get<Submission[]>(`/submissions?homework_id=${homeworkId}`);
    return response.data;
  }

  /**
   * Delete submission (if allowed)
   */
  async deleteSubmission(id: string): Promise<void> {
    await api.delete(`/submissions/${id}`);
  }

  /**
   * Get AI analysis for submission
   */
  async getAIAnalysis(id: string): Promise<any> {
    const response = await api.get<any>(`/submissions/${id}/ai-analysis`);
    return response.data;
  }

  /**
   * Resubmit homework (create new submission)
   */
  async resubmitHomework(
    homework_id: string,
    images: ImageData[],
    onProgress?: (progress: UploadProgress) => void
  ): Promise<Submission> {
    return this.submitHomework(homework_id, images, onProgress);
  }
}

export default new SubmissionService();
