import jwtDecode from "jwt-decode";
import http from "./httpService";
import { apiUrl } from "../config.json";

const apiEndpoint = apiUrl + "/login";
const tokenKey = "token";

http.setJwt(getJwt());

export async function login(email, password) {
  const { data: jwt } = await http.post(apiEndpoint, { email, password });
  localStorage.setItem(tokenKey, jwt["token"]);
}

export function loginWithJwt(jwt) {
  localStorage.setItem(tokenKey, jwt["token"]);
}

export function logout() {
  localStorage.removeItem(tokenKey);
}

export function isLoggedIn() {
  try {
    const jwt = localStorage.getItem(tokenKey);
    if (jwt) {
      return true;
    } else {
      return false;
    }
  } catch (e) {
    return false;
  }
}

export function getCurrentUser() {
  try {
    const jwt = localStorage.getItem(tokenKey);
    return jwtDecode(jwt);
  } catch (ex) {
    return null;
  }
}

export function getJwt() {
  return localStorage.getItem(tokenKey);
}

export default {
  login,
  loginWithJwt,
  logout,
  getCurrentUser,
  getJwt,
  isLoggedIn,
};
