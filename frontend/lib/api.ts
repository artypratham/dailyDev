import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== "undefined") {
        localStorage.removeItem("token");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  signup: (data: {
    email: string;
    password: string;
    name?: string;
    phone_whatsapp?: string;
    timezone?: string;
  }) => api.post("/auth/signup", data),

  login: (data: { email: string; password: string }) =>
    api.post("/auth/login", data),

  me: () => api.get("/auth/me"),
};

// User API
export const userApi = {
  getProfile: () => api.get("/users/me"),
  updateProfile: (data: any) => api.patch("/users/me", data),
  uploadResume: (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return api.post("/users/me/resume", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  getStats: () => api.get("/users/me/stats"),
  connectWhatsApp: (phone: string) =>
    api.post(`/users/me/whatsapp/connect?phone_number=${encodeURIComponent(phone)}`),
};

// Topics API
export const topicsApi = {
  getAll: () => api.get("/topics/"),
  getById: (id: string) => api.get(`/topics/${id}`),
  select: (data: { topic_ids: string[]; duration_days: number }) =>
    api.post("/topics/select", data),
  getMyTopics: () => api.get("/topics/me/selected"),
};

// Roadmap API
export const roadmapApi = {
  getAll: () => api.get("/roadmap/"),
  getByTopic: (topicId: string) => api.get(`/roadmap/topic/${topicId}`),
  getToday: () => api.get("/roadmap/today"),
};

// Articles API
export const articlesApi = {
  getById: (id: string) => api.get(`/articles/${id}`),
  generate: (roadmapId: string) => api.post(`/articles/${roadmapId}/generate`),
  save: (id: string, notes?: string) =>
    api.post(`/articles/${id}/save`, { notes }),
  unsave: (id: string) => api.delete(`/articles/${id}/save`),
  getSaved: () => api.get("/articles/library/saved"),
};
