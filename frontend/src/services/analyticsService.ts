// analyticsService.ts - Analytics API Service
//
// API calls for analytics and statistics endpoints.

import api from './api';

/**
 * Analytics Service
 *
 * Methods:
 * - getClassStats(classId) - GET /analytics/classes/:id
 * - getStudentStats(studentId) - GET /analytics/students/:id
 * - getTeacherStats(teacherId) - GET /analytics/teachers/:id
 * - getSchoolStats() - GET /analytics/school
 * - getHomeworkCompletionRates() - GET /analytics/homework-completion
 * - getGradeDistribution() - GET /analytics/grade-distribution
 */

export interface ClassStats {
  class_id: string;
  class_name: string;
  total_students: number;
  total_homework: number;
  total_submissions: number;
  submission_rate: number;
  average_grade: number;
  pending_submissions: number;
  on_time_rate: number;
}

export interface StudentStats {
  student_id: string;
  student_name: string;
  total_homework: number;
  completed_homework: number;
  completion_rate: number;
  average_grade: number;
  on_time_submissions: number;
  late_submissions: number;
  pending_homework: number;
  recent_submissions: SubmissionSummary[];
}

export interface TeacherStats {
  teacher_id: string;
  teacher_name: string;
  total_classes: number;
  total_students: number;
  total_homework_assigned: number;
  total_submissions: number;
  pending_reviews: number;
  average_class_grade: number;
  homework_by_subject: SubjectBreakdown[];
}

export interface SchoolStats {
  total_students: number;
  total_teachers: number;
  total_classes: number;
  total_homework: number;
  total_submissions: number;
  overall_completion_rate: number;
  overall_average_grade: number;
  active_homework: number;
  pending_reviews: number;
}

export interface SubmissionSummary {
  homework_id: string;
  homework_title: string;
  submitted_at: string;
  grade?: number;
  status: string;
}

export interface SubjectBreakdown {
  subject: string;
  count: number;
  average_grade: number;
}

export interface HomeworkCompletionData {
  date: string;
  assigned: number;
  completed: number;
  completion_rate: number;
}

export interface GradeDistribution {
  grade_range: string;
  count: number;
  percentage: number;
}

class AnalyticsService {
  /**
   * Get class statistics
   */
  async getClassStats(classId: string): Promise<ClassStats> {
    const response = await api.get<ClassStats>(`/analytics/classes/${classId}`);
    return response.data;
  }

  /**
   * Get student statistics
   */
  async getStudentStats(studentId: string): Promise<StudentStats> {
    const response = await api.get<StudentStats>(`/analytics/students/${studentId}`);
    return response.data;
  }

  /**
   * Get teacher statistics
   */
  async getTeacherStats(teacherId: string): Promise<TeacherStats> {
    const response = await api.get<TeacherStats>(`/analytics/teachers/${teacherId}`);
    return response.data;
  }

  /**
   * Get school-wide statistics (principal only)
   */
  async getSchoolStats(): Promise<SchoolStats> {
    const response = await api.get<SchoolStats>('/analytics/school');
    return response.data;
  }

  /**
   * Get homework completion rates over time
   */
  async getHomeworkCompletionRates(
    startDate?: string,
    endDate?: string
  ): Promise<HomeworkCompletionData[]> {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);

    const response = await api.get<HomeworkCompletionData[]>(
      `/analytics/homework-completion?${params.toString()}`
    );
    return response.data;
  }

  /**
   * Get grade distribution
   */
  async getGradeDistribution(filters?: {
    class_id?: string;
    subject?: string;
    start_date?: string;
    end_date?: string;
  }): Promise<GradeDistribution[]> {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });
    }

    const response = await api.get<GradeDistribution[]>(
      `/analytics/grade-distribution?${params.toString()}`
    );
    return response.data;
  }

  /**
   * Get student performance trend
   */
  async getStudentPerformanceTrend(studentId: string): Promise<any[]> {
    const response = await api.get<any[]>(`/analytics/students/${studentId}/performance-trend`);
    return response.data;
  }

  /**
   * Export analytics report
   */
  async exportReport(
    type: 'class' | 'student' | 'school',
    id?: string,
    format: 'csv' | 'pdf' = 'csv'
  ): Promise<Blob> {
    const endpoint = id ? `/analytics/${type}/${id}/export` : `/analytics/${type}/export`;
    const response = await api.get(endpoint, {
      params: { format },
      responseType: 'blob',
    });
    return response.data;
  }
}

export default new AnalyticsService();
