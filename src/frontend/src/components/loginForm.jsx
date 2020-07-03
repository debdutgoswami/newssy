import React from "react";
import { Redirect } from "react-router-dom";
import Joi from "joi-browser";
import Form from "./common/form";
import auth from "../services/authService";
import { toast, ToastContainer } from "react-toastify";
import { apiUrl } from "../config.json";
import axios from "axios";

class LoginForm extends Form {
  state = {
    data: { email: "", password: "" },
    errors: {},

    redir: {},
  };
  componentDidMount() {
    if (this.props.location.state) {
      const { account } = this.props.location.state;
      this.state.redir = account;
    }
  }
  schema = {
    email: Joi.string().required().email().label("email"),
    password: Joi.string().required().label("Password"),
  };

  doSubmit = async () => {
    const apiEndpoint = apiUrl + "/login";
    const tokenKey = "token";
    try {
      const response = await axios
        .post(apiEndpoint, this.state.data)
        .catch((err) => {
          this.setState({ status: err.response.status });
        });
      console.log(response);
      try {
        localStorage.setItem(tokenKey, response.data["token"]);
        const status = response.status;
        this.setState({ status });
      } catch (error) {}
      // const { data } = this.state;
      // // const response = await auth.login(data.email, data.password);
      const { state } = this.props.location;
      if (this.state.status) {
        if (this.state.status === 402) {
          toast.error("Confirm Your Email");
        } else if (this.state.status === 201) {
          console.log(this.state.status);
          // window.location = "/";
          window.location = state ? state.from.pathname : "/";
        } else if (this.state.status === 401) {
          toast.error("Email or Password is incorrect");
        } else if (this.state.status === 403) {
          toast.error("You Have Been BANNED");
        } else {
          toast.error("Unknown ERROR");
        }
      }
      console.log(response.status);
    } catch (ex) {
      // if (ex.response && ex.response.status === 400) {
      //   const errors = { ...this.state.errors };
      //   errors.email = ex.response.data;
      //   this.setState({ errors });
      // } else {
      //   this.setState({ code: ex.response.status });
      // }
    }
  };

  render() {
    if (auth.isLoggedIn() === true) return <Redirect to="/" />;

    return (
      <div>
        <ToastContainer />
        <h1>Login</h1>
        <form onSubmit={this.handleSubmit}>
          {this.renderInput("email", "email")}
          {this.renderInput("password", "Password", "password")}
          {this.renderButton("Login")}
        </form>
        <div>
          <small>Forget password?</small>
          <a href="/resend">
            <small>NIKALL LAWDE</small>
          </a>
        </div>
        <small>didnt registered yet?</small>
        <a href="/signup">
          <small>sign up NOW</small>
        </a>
      </div>
    );
  }
}

export default LoginForm;
