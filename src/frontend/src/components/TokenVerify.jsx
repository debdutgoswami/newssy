import React, { Component } from "react";
import { Link } from "react-router-dom";
import { apiUrl } from "../config.json";
import axios from "axios";

class Token extends Component {
  state = { status: {} };
  async componentDidMount() {
    const q = window.location.search;
    const url = new URLSearchParams(q);
    const token = url.get("token");
    console.log(token);
    const apiEndpoint = apiUrl + "/confirm/" + token;

    const response = await axios.get(apiEndpoint);
    const status = response.status;
    this.setState({ status });
  }

  render() {
    return (
      <div>
        {console.log(this.state.status)}
        {this.state.status === 201 && (
          <React.Fragment>
            <h1>You Account has been verified NOW</h1>

            <Link to="/login">Click Here To LOGIN RIGHT NOW!!!</Link>
          </React.Fragment>
        )}
        {this.state.status === 402 && (
          <React.Fragment>
            <h1>Your Token Has Been Expired</h1>

            <Link to="">Click Here to Resend ur Verification Code</Link>
          </React.Fragment>
        )}
        {this.state.status === 202 && (
          <React.Fragment>
            <h1>Your Account Doesnt Exists PLEASE REGISTER UR ACCOUNT </h1>

            <Link to="/signup">Click Here to Register</Link>
          </React.Fragment>
        )}
      </div>
    );
  }
}
export default Token;
