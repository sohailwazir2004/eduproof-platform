// Homework Type Definitions
export enum HomeworkStatus {
  DRAFT = 'draft',
  ASSIGNED = 'assigned',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  GRADED = 'graded',
}

export interface Homework {
  id: string;
  title: string;
  description: string;
  teacher_id: string;
  teacher_name?: string;
  class_id: string;
  class_name?: string;
  subject: string;
  textbook_id?: string;
  textbook_title?: string;
  page_numbers?: string;
  due_date: string;
  total_points: number;
  status: HomeworkStatus;
  created_at: string;
  updated_at: string;
  attachments?: HomeworkAttachment[];
  submission_count?: number;
  graded_count?: number;
}

export interface HomeworkAttachment {
  id: string;
  homework_id: string;
  file_name: string;
  file_url: string;
  file_type: string;
  file_size: number;
  uploaded_at: string;
}

export interface CreateHomeworkRequest {
  title: string;
  description: string;
  class_id: string;
  subject: string;
  textbook_id?: string;
  page_numbers?: string;
  due_date: string;
  total_points: number;
  attachments?: File[];
}

export interface UpdateHomeworkRequest {
  title?: string;
  description?: string;
  due_date?: string;
  total_points?: number;
  status?: HomeworkStatus;
}

export interface HomeworkFilters {
  class_id?: string;
  subject?: string;
  status?: HomeworkStatus;
  date_from?: string;
  date_to?: string;
}
