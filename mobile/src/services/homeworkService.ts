// homeworkService.ts - Homework Service
//
// Homework API calls for mobile (student-focused).

import api from './api';

/**
 * Homework Service for Students
 *
 * Methods:
 * - getHomeworkList(filters) - GET /homework (student's homework)
 * - getHomework(id) - GET /homework/:id
 * - getMyHomework() - GET /homework/my (current user's homework)
 * - getHomeworkSubmissions(id) - GET /homework/:id/submissions
 */

export interface Homework {
  id: string;
  title: string;
  description?: string;
  teacher_id: string;
  teacher_name?: string;
  class_id: string;
  class_name?: string;
  subject?: string;
  textbook_id?: string;
  textbook_title?: string;
  page_numbers?: string;
  due_date: string;
  created_at: string;
  updated_at: string;
  is_submitted?: boolean;
  submission_status?: 'not_submitted' | 'submitted' | 'graded';
}

export interface HomeworkFilters {
  class_id?: string;
  subject?: string;
  status?: 'active' | 'past_due' | 'all';
  is_submitted?: boolean;
  skip?: number;
  limit?: number;
}

export interface HomeworkDetail extends Homework {
  textbook_pages?: string[];
  total_submissions?: number;
  my_submission?: {
    id: string;
    status: string;
    submitted_at: string;
    grade?: number;
  };
}

class HomeworkService {
  /**
   * Get list of homework with filters
   */
  async getHomeworkList(filters?: HomeworkFilters): Promise<Homework[]> {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await api.get<Homework[]>(`/homework?${params.toString()}`);
    return response.data;
  }

  /**
   * Get homework by ID with details
   */
  async getHomework(id: string): Promise<HomeworkDetail> {
    const response = await api.get<HomeworkDetail>(`/homework/${id}`);
    return response.data;
  }

  /**
   * Get current student's homework
   */
  async getMyHomework(filters?: { status?: string }): Promise<Homework[]> {
    const params = new URLSearchParams();
    if (filters?.status) {
      params.append('status', filters.status);
    }

    const response = await api.get<Homework[]>(`/homework/my?${params.toString()}`);
    return response.data;
  }

  /**
   * Get homework statistics for student
   */
  async getHomeworkStats(): Promise<{
    total: number;
    pending: number;
    submitted: number;
    graded: number;
    completion_rate: number;
  }> {
    const response = await api.get('/homework/stats');
    return response.data;
  }

  /**
   * Get upcoming homework deadlines
   */
  async getUpcomingHomework(days: number = 7): Promise<Homework[]> {
    const response = await api.get<Homework[]>(`/homework/upcoming?days=${days}`);
    return response.data;
  }
}

export default new HomeworkService();
