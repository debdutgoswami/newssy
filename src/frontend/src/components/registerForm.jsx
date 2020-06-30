import React from "react";
import Joi from "joi-browser";
import Form from "./common/form";
import * as userService from "../services/userService";
import auth from "../services/authService";
import { Redirect } from "react-router-dom";

class RegisterForm extends Form {
  state = {
    data: { email: "", password: "", cpassword: "", fname: "", lname: "" },
    errors: {},
  };

  schema = {
    email: Joi.string().required().email().label("Email"),
    password: Joi.string().required().min(5).max(25).label("Password"),
    cpassword: Joi.string()
      .required()
      .valid(Joi.ref("password"))
      .label("Confirm Password")
      .options({
        language: {
          any: {
            allowOnly: "!!Passwords do not match",
          },
        },
      }),
    fname: Joi.string().required().max(25).label("First Name"),
    lname: Joi.string().required().max(25).label("Last Name"),
  };

  doSubmit = async () => {
    try {
      console.log(this.state.data);
      const response = await userService.register(this.state.data);
      console.log(response);
      // auth.loginWithJwt(response.headers["x-auth-token"]);
      // TODO response code check
      window.location = "/";
    } catch (ex) {
      console.log(ex.response);
      if (ex.response && ex.response.status === 400) {
        const errors = { ...this.state.errors };
        errors.email = ex.response.data;
        this.setState({ errors });
      }
    }
  };

  render() {
    if (auth.isLoggedIn() === true) return <Redirect to="/" />;
    return (
      <div>
        <h1>Register</h1>
        <form onSubmit={this.handleSubmit}>
          {this.renderInput("name", "Name")}
          {this.renderInput("email", "Email")}
          {this.renderInput("password", "Password", "password")}
          {this.renderButton("Register")}
        </form>
        <small>Already registered?</small>
        <a href="/login">
          <small>LOGIN RIGHT NOW</small>
        </a>
      </div>
    );
  }
}

export default RegisterForm;
