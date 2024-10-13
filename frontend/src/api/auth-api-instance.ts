import axios, { InternalAxiosRequestConfig } from "axios";

const AUTH_ERROR = 401;

const appHost = "localhost";
const appPort = "3000";

const baseURL = `http://${appHost}:${appPort}`;

/** Axios для авторизации */
const authAxiosInstance = axios.create({
  baseURL,
});

const authInterceptor = (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
  config.headers.Authorization = `${sessionStorage.getItem("userToken")}`;
  config.headers["Content-Type"] = "application/json";
  config.headers.Accept = "application/json";
  config.withCredentials = true;

  return config;
};

authAxiosInstance.interceptors.request.use(authInterceptor);

/** Отлавливаем ошибку с окончанием токена и обновляем его */
authAxiosInstance.interceptors.response.use(
  config => config,
  async error => {
    // const originalRequest = error.config;

    if (error.response && error.response?.status === AUTH_ERROR && error.response?.statusText === "Unauthorized") {
      try {
        // const { data: responseData } = await authAxiosInstance.get("/auth/refresh");
        // sessionStorage.setItem("userToken", responseData.access_token);
        sessionStorage.setItem("userToken", "");
        window.location.replace("/auth");
      } catch (e) {
        console.log(e);
      } finally {
        // return authAxiosInstance.request(originalRequest);
      }
    }

    throw error;
  }
);

export default authAxiosInstance;
