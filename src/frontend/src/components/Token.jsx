import React, { Component } from "react";
import { Link } from "react-router-dom";
import { apiUrl } from "../config.json";
import axios from "axios";

class Token extends Component {
  async componentDidMount() {
    const q = window.location.search;
    const url = new URLSearchParams(q);
    const token = url.get("token");
    console.log(token);
    const apiEndpoint = apiUrl + "/confirm/" + token;

    const { data: response } = await axios.get(apiEndpoint);

    console.log(response);
  }
  render() {
    return (
      <div>
        <h1>You Account has been verified NOW</h1>

        <Link to="/login">Click Here!!</Link>
      </div>
    );
  }
}
export default {
  Token,
};
