import React, { Component } from "react";
import { apiUrl } from "../config.json";
import axios from "axios";
import AccountDetails from "./design/AccountDetails";

class Profile extends Component {
  state = { done: false, profile: {} };

  async componentDidMount() {
    const apiEndpoint = apiUrl + "/profile-data";

    const response = await axios
      .get(apiEndpoint, {
        headers: {
          "x-access-token": localStorage.getItem("token"),
        },
      })
      .catch((err) => {
        this.setState({ profile: err.response.status });
      });
    try {
      const profile = response;
      this.setState({ profile });
      this.setState({ done: true });
    } catch (error) {}
  }

  render() {
    console.log(this.state.profile);

    if (this.state.done) {
      return (
        <div>
          <h1>Your Account</h1>
          <AccountDetails Account={this.state.profile.data} />
        </div>
      );
    } else {
      return <div></div>;
    }
  }
}

export default Profile;
