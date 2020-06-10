import jwtDecode from "jwt-decode";
import http from "./httpService";
import { apiUrl } from "../config.json";

const apiEndpoint = apiUrl + "/login";
const tokenKey = "token";

http.setJwt(getJwt());

export async function login(email, password) {
  const { data: jwt } = await http.post(apiEndpoint, { email, password });
  localStorage.setItem(tokenKey, jwt);
  console.log(jwt)
}

export function loginWithJwt(jwt) {
  console.log(jwtDecode(jwt))
  localStorage.setItem(tokenKey, jwt);
}

export function logout() {
  console.log(tokenKey)
  localStorage.removeItem(tokenKey);
}

export function getCurrentUser() {
  try {
    const jwt = localStorage.getItem(tokenKey);
    console.log(jwtDecode(jwt))
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
  getJwt
};
