export interface User {
  id: number;
  email: string;
  is_admin: boolean;
  is_active: boolean;
  created_at: string;
}

export interface Class {
  id: number;
  name: string;
  description?: string;
  created_at: string;
  file_count: number;
}

export interface File {
  id: number;
  class_id: number;
  filename: string;
  original_filename: string;
  file_type: 'audio' | 'pdf';
  file_size: number;
  is_processed: boolean;
  created_at: string;
}

export interface ChatMessage {
  class_id: number;
  message: string;
}

export interface SourceDocument {
  filename: string;
  content: string;
}

export interface ChatResponse {
  answer: string;
  sources: SourceDocument[];
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface UserCreate {
  email: string;
  password: string;
  is_admin: boolean;
}

export interface ClassCreate {
  name: string;
  description?: string;
}

export interface PasswordChange {
  old_password: string;
  new_password: string;
}
