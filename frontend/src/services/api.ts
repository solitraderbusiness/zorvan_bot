import axios, { AxiosInstance } from 'axios';
import type {
  User,
  Class,
  File,
  ChatMessage,
  ChatResponse,
  LoginRequest,
  TokenResponse,
  UserCreate,
  ClassCreate,
  PasswordChange,
} from '../types';

const API_URL = import.meta.env.VITE_API_URL || '/api';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_URL,
    });

    // Add auth token to requests
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Handle 401 errors
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth
  async login(data: LoginRequest): Promise<TokenResponse> {
    const response = await this.api.post<TokenResponse>('/auth/login', data);
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.api.get<User>('/auth/me');
    return response.data;
  }

  async changePassword(data: PasswordChange): Promise<void> {
    await this.api.post('/auth/change-password', data);
  }

  // Users
  async getUsers(): Promise<User[]> {
    const response = await this.api.get<User[]>('/users/');
    return response.data;
  }

  async createUser(data: UserCreate): Promise<User> {
    const response = await this.api.post<User>('/users/', data);
    return response.data;
  }

  async deleteUser(userId: number): Promise<void> {
    await this.api.delete(`/users/${userId}`);
  }

  async addUserToClass(userId: number, classId: number): Promise<void> {
    await this.api.post(`/users/${userId}/classes/${classId}`);
  }

  async removeUserFromClass(userId: number, classId: number): Promise<void> {
    await this.api.delete(`/users/${userId}/classes/${classId}`);
  }

  // Classes
  async getClasses(): Promise<Class[]> {
    const response = await this.api.get<Class[]>('/classes/');
    return response.data;
  }

  async getClass(classId: number): Promise<Class> {
    const response = await this.api.get<Class>(`/classes/${classId}`);
    return response.data;
  }

  async createClass(data: ClassCreate): Promise<Class> {
    const response = await this.api.post<Class>('/classes/', data);
    return response.data;
  }

  async updateClass(classId: number, data: ClassCreate): Promise<Class> {
    const response = await this.api.put<Class>(`/classes/${classId}`, data);
    return response.data;
  }

  async deleteClass(classId: number): Promise<void> {
    await this.api.delete(`/classes/${classId}`);
  }

  // Files
  async getFiles(classId: number): Promise<File[]> {
    const response = await this.api.get<File[]>(`/files/class/${classId}`);
    return response.data;
  }

  async uploadFile(classId: number, file: globalThis.File, onProgress?: (progress: number) => void): Promise<File> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await this.api.post<File>(`/files/class/${classId}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total && onProgress) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(progress);
        }
      },
    });

    return response.data;
  }

  async deleteFile(fileId: number): Promise<void> {
    await this.api.delete(`/files/${fileId}`);
  }

  // Chat
  async chat(data: ChatMessage): Promise<ChatResponse> {
    const response = await this.api.post<ChatResponse>('/chat/', data);
    return response.data;
  }
}

export const api = new ApiService();
