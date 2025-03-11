// src/plugins/axios.js
import axios from 'axios';
import store from '@/store';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8008' // 백엔드 API URL
});

axiosInstance.interceptors.request.use(
  (config) => {
    const token = store.getters.getToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.error('[Axios] 인증 에러: 401');
      store.dispatch('logout');
      alert('인증이 만료되었습니다. 다시 로그인하세요.');
      window.location.href = '/login'; // 로그인 페이지로 이동
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
