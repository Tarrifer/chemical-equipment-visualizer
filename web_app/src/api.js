import axios from "axios";

const BASE_URL = "http://127.0.0.1:8001";

export const api = axios.create({
  baseURL: BASE_URL,
});

export function setAuthToken(token) {
  if (token) {
    api.defaults.headers.common["Authorization"] = `Token ${token}`;
    localStorage.setItem("token", token);
  } else {
    delete api.defaults.headers.common["Authorization"];
    localStorage.removeItem("token");
  }
}