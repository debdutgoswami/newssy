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
    const apiEndpoint = apiUrl + "/confirm/" + token;

    const response = await axios.get(apiEndpoint).catch(err => {
      this.setState({status: err.response.status})
    });
    
    try {
      const status = response.status;
      this.setState({ status });
    }catch (error) {}
  }

  render() {
    return (
      <div>
        {console.log(this.state.status)}
        {this.state.status === 201 && (
          <React.Fragment>
            <h1>Account has been verified</h1>

            <Link to="/login">Login?</Link>
          </React.Fragment>
        )}
        {this.state.status === 402 && (
          <React.Fragment>
            <h1>Token has expired</h1>

            <Link to="">Generate a new one?</Link>
          </React.Fragment>
        )}
        {this.state.status === 202 && (
          <React.Fragment>
            <h1>Email doesn't Exists</h1>

            <Link to="/signup">Register?</Link>
          </React.Fragment>
        )}
        {this.state.status === 203 && (
          <React.Fragment>
            <h1>Email already confirmed</h1>

            <Link to="/login">Login?</Link>
          </React.Fragment>
        )}
      </div>
    );
  }
}
export default Token;
