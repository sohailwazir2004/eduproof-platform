// classService.ts - Class Management API Service
//
// API calls for class/classroom endpoints.

import api from './api';

/**
 * Class Service
 *
 * Methods:
 * - getClasses(filters) - GET /classes
 * - getClass(id) - GET /classes/:id
 * - createClass(data) - POST /classes
 * - updateClass(id, data) - PUT /classes/:id
 * - deleteClass(id) - DELETE /classes/:id
 * - getClassStudents(id) - GET /classes/:id/students
 * - addStudent(classId, studentId) - POST /classes/:id/students
 * - removeStudent(classId, studentId) - DELETE /classes/:id/students/:studentId
 */

export interface Class {
  id: string;
  name: string;
  grade_level: number;
  section?: string;
  subject?: string;
  teacher_id: string;
  teacher_name?: string;
  academic_year: string;
  student_count?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ClassCreate {
  name: string;
  grade_level: number;
  section?: string;
  subject?: string;
  academic_year: string;
}

export interface ClassFilters {
  teacher_id?: string;
  grade_level?: number;
  subject?: string;
  is_active?: boolean;
  skip?: number;
  limit?: number;
}

export interface Student {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  avatar_url?: string;
  enrollment_date?: string;
}

class ClassService {
  /**
   * Get list of classes with filters
   */
  async getClasses(filters?: ClassFilters): Promise<{ items: Class[]; total: number }> {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await api.get<{ items: Class[]; total: number }>(
      `/classes?${params.toString()}`
    );
    return response.data;
  }

  /**
   * Get class by ID
   */
  async getClass(id: string): Promise<Class> {
    const response = await api.get<Class>(`/classes/${id}`);
    return response.data;
  }

  /**
   * Create new class
   */
  async createClass(data: ClassCreate): Promise<Class> {
    const response = await api.post<Class>('/classes', data);
    return response.data;
  }

  /**
   * Update class
   */
  async updateClass(id: string, data: Partial<ClassCreate>): Promise<Class> {
    const response = await api.put<Class>(`/classes/${id}`, data);
    return response.data;
  }

  /**
   * Delete class
   */
  async deleteClass(id: string): Promise<void> {
    await api.delete(`/classes/${id}`);
  }

  /**
   * Get students in class
   */
  async getClassStudents(id: string): Promise<Student[]> {
    const response = await api.get<Student[]>(`/classes/${id}/students`);
    return response.data;
  }

  /**
   * Add student to class
   */
  async addStudent(classId: string, studentId: string): Promise<{ message: string }> {
    const response = await api.post<{ message: string }>(`/classes/${classId}/students`, {
      student_id: studentId,
    });
    return response.data;
  }

  /**
   * Remove student from class
   */
  async removeStudent(classId: string, studentId: string): Promise<{ message: string }> {
    const response = await api.delete<{ message: string }>(
      `/classes/${classId}/students/${studentId}`
    );
    return response.data;
  }

  /**
   * Get class homework
   */
  async getClassHomework(id: string): Promise<any[]> {
    const response = await api.get<any[]>(`/classes/${id}/homework`);
    return response.data;
  }
}

export default new ClassService();
