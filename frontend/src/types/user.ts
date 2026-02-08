// User Type Definitions
export enum UserRole {
  STUDENT = 'student',
  TEACHER = 'teacher',
  PARENT = 'parent',
  PRINCIPAL = 'principal',
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
  profile?: StudentProfile | TeacherProfile | ParentProfile | PrincipalProfile;
}

export interface StudentProfile {
  id: string;
  user_id: string;
  student_id: string;
  grade_level: number;
  class_id?: string;
  parent_id?: string;
  date_of_birth?: string;
  phone_number?: string;
}

export interface TeacherProfile {
  id: string;
  user_id: string;
  employee_id: string;
  subject?: string;
  department?: string;
  phone_number?: string;
  classes?: string[];
}

export interface ParentProfile {
  id: string;
  user_id: string;
  phone_number?: string;
  children?: string[];
  occupation?: string;
}

export interface PrincipalProfile {
  id: string;
  user_id: string;
  employee_id: string;
  phone_number?: string;
  office_location?: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
  role: UserRole;
}

export interface AuthResponse {
  user: User;
  tokens: AuthTokens;
}
