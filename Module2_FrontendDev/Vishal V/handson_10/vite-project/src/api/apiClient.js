import axios from "axios";

const apiClient = axios.create({
  baseURL: "https://api.example.com",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use((config) => {
  const mockToken = "mock-jwt-token-123";
  config.headers.Authorization = `Bearer ${mockToken}`;
  return config;
});

apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const statusCode = error.response?.status || 500;
    const message =
      error.response?.data?.message || error.message || "Unexpected error occurred";
    return Promise.reject({ message, statusCode });
  }
);

export default apiClient;
