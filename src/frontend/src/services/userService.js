import http from "./httpService";
import { apiUrl } from "../config.json";

const apiEndpoint = apiUrl + "/signup";

export function register(user) {
  return http.post(apiEndpoint, {
    email: user.email,
    password: user.password,
    fname: user.fname,
    lname: user.lname,
  });
}
