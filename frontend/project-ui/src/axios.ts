import axios from 'axios'

const axiosInstance = axios.create({
  baseURL: process.env.VUE_APP_BASE_API_URL || 'http://localhost:5000',
});

export default axiosInstance;