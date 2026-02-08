// textbookService.ts - Textbook API Service
//
// API calls for textbook endpoints.

import api from './api';

/**
 * Textbook Service
 *
 * Methods:
 * - getTextbooks(filters) - GET /textbooks
 * - getTextbook(id) - GET /textbooks/:id
 * - uploadTextbook(file, metadata) - POST /textbooks
 * - deleteTextbook(id) - DELETE /textbooks/:id
 * - getTextbookPages(id) - GET /textbooks/:id/pages
 */

export interface Textbook {
  id: string;
  title: string;
  subject: string;
  grade_level: number;
  publisher?: string;
  isbn?: string;
  file_url: string;
  file_type: string;
  total_pages?: number;
  thumbnail_url?: string;
  uploaded_by: string;
  created_at: string;
  updated_at: string;
}

export interface TextbookCreate {
  title: string;
  subject: string;
  grade_level: number;
  publisher?: string;
  isbn?: string;
  file: File;
}

export interface TextbookFilters {
  subject?: string;
  grade_level?: number;
  skip?: number;
  limit?: number;
}

export interface TextbookPage {
  page_number: number;
  image_url: string;
  thumbnail_url?: string;
  ocr_text?: string;
}

class TextbookService {
  /**
   * Get list of textbooks with filters
   */
  async getTextbooks(filters?: TextbookFilters): Promise<{ items: Textbook[]; total: number }> {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await api.get<{ items: Textbook[]; total: number }>(
      `/textbooks?${params.toString()}`
    );
    return response.data;
  }

  /**
   * Get textbook by ID
   */
  async getTextbook(id: string): Promise<Textbook> {
    const response = await api.get<Textbook>(`/textbooks/${id}`);
    return response.data;
  }

  /**
   * Upload new textbook
   */
  async uploadTextbook(data: TextbookCreate): Promise<Textbook> {
    const formData = new FormData();
    formData.append('title', data.title);
    formData.append('subject', data.subject);
    formData.append('grade_level', data.grade_level.toString());
    if (data.publisher) formData.append('publisher', data.publisher);
    if (data.isbn) formData.append('isbn', data.isbn);
    formData.append('file', data.file);

    const response = await api.post<Textbook>('/textbooks', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  /**
   * Update textbook metadata
   */
  async updateTextbook(
    id: string,
    data: Partial<Omit<TextbookCreate, 'file'>>
  ): Promise<Textbook> {
    const response = await api.put<Textbook>(`/textbooks/${id}`, data);
    return response.data;
  }

  /**
   * Delete textbook
   */
  async deleteTextbook(id: string): Promise<void> {
    await api.delete(`/textbooks/${id}`);
  }

  /**
   * Get textbook pages
   */
  async getTextbookPages(id: string): Promise<TextbookPage[]> {
    const response = await api.get<TextbookPage[]>(`/textbooks/${id}/pages`);
    return response.data;
  }

  /**
   * Get specific page from textbook
   */
  async getTextbookPage(id: string, pageNumber: number): Promise<TextbookPage> {
    const response = await api.get<TextbookPage>(`/textbooks/${id}/pages/${pageNumber}`);
    return response.data;
  }

  /**
   * Search textbooks by keyword
   */
  async searchTextbooks(query: string): Promise<Textbook[]> {
    const response = await api.get<Textbook[]>(`/textbooks/search?q=${encodeURIComponent(query)}`);
    return response.data;
  }
}

export default new TextbookService();
