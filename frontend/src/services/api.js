import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Books API
export const bookService = {
  getAll: (params) => api.get('/books', { params }),
  getById: (id) => api.get(`/books/${id}`),
  create: (data) => api.post('/books', data),
  update: (id, data) => api.put(`/books/${id}`, data),
  delete: (id) => api.delete(`/books/${id}`),
  getCategories: () => api.get('/books/categories'),
  getAvailable: () => api.get('/books/available'),
};

// Members API
export const memberService = {
  getAll: (params) => api.get('/members', { params }),
  getById: (id) => api.get(`/members/${id}`),
  create: (data) => api.post('/members', data),
  update: (id, data) => api.put(`/members/${id}`, data),
  delete: (id) => api.delete(`/members/${id}`),
  getBorrowed: (id) => api.get(`/members/${id}/borrowed`),
};

// Transactions API
export const transactionService = {
  getAll: (params) => api.get('/transactions', { params }),
  borrowBook: (data) => api.post('/transactions/borrow', data),
  returnBook: (data) => api.post('/transactions/return', data),
  getOverdue: () => api.get('/transactions/overdue'),
  payFine: (id) => api.post(`/transactions/pay-fine/${id}`),
  getStats: () => api.get('/transactions/stats'),
};

export default api;