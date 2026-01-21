import axios from "axios";

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true, // browser will send cookies to server automatically on every req
});

// Inject Clerk token from cookies to headers
export const setupAxiosInterceptors = (getToken) => {
  axiosInstance.interceptors.request.use(async (config) => {
    try {
      const token = await getToken();
      if (token) config.headers.Authorization = `Bearer ${token}`;
    } catch (err) {
      console.error("Error fetching Clerk token: ", err);
    }
    return config;
  });
};

export default axiosInstance;
