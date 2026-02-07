// homeworkService.ts - Homework API Service
//
// API calls for homework endpoints.

import api from './api';

/**
 * Homework Service
 *
 * Methods:
 * - getHomeworkList(filters) - GET /homework
 * - getHomework(id) - GET /homework/:id
 * - createHomework(data) - POST /homework
 * - updateHomework(id, data) - PUT /homework/:id
 * - deleteHomework(id) - DELETE /homework/:id
 */

export interface Homework {
  id: string;
  title: string;
  description?: string;
  teacher_id: string;
  class_id: string;
  subject_id?: string;
  textbook_id?: string;
  page_numbers?: string;
  due_date: string;
  created_at: string;
  updated_at: string;
}

export interface HomeworkCreate {
  title: string;
  description?: string;
  class_id: string;
  subject_id?: string;
  textbook_id?: string;
  page_numbers?: string;
  due_date: string;
}

export interface HomeworkFilters {
  class_id?: string;
  subject_id?: string;
  teacher_id?: string;
  status?: 'active' | 'past_due' | 'all';
  skip?: number;
  limit?: number;
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
   * Get homework by ID
   */
  async getHomework(id: string): Promise<Homework> {
    const response = await api.get<Homework>(`/homework/${id}`);
    return response.data;
  }

  /**
   * Create new homework
   */
  async createHomework(data: HomeworkCreate): Promise<Homework> {
    const response = await api.post<Homework>('/homework', data);
    return response.data;
  }

  /**
   * Update homework
   */
  async updateHomework(id: string, data: Partial<HomeworkCreate>): Promise<Homework> {
    const response = await api.put<Homework>(`/homework/${id}`, data);
    return response.data;
  }

  /**
   * Delete homework
   */
  async deleteHomework(id: string): Promise<void> {
    await api.delete(`/homework/${id}`);
  }

  /**
   * Get submissions for homework
   */
  async getHomeworkSubmissions(id: string): Promise<any[]> {
    const response = await api.get<any[]>(`/homework/${id}/submissions`);
    return response.data;
  }
}

export default new HomeworkService();
