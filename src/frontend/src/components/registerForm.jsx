import React from "react";
import Joi from "joi-browser";
import Form from "./common/form";
import * as userService from "../services/userService";
import auth from "../services/authService";
import { Redirect } from "react-router-dom";
import { toast, ToastContainer } from "react-toastify";
// import codeStatus from "./manageCode";

class RegisterForm extends Form {
  state = {
    data: { email: "", password: "", cpassword: "", fname: "", lname: "" },
    errors: {},
    code: {},
    notify: {},
  };
  componentDidMount() {
    if (this.props.location.state) {
      const { codes } = this.props.location.state;

      this.state.notify = codes;
    }
  }
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
  // checkStatus(code) {
  //   return <codeStatus code={code} />;
  // }

  doSubmit = async () => {
    try {
      const response = await userService.register(this.state.data);
      console.log(response);

      this.setState({ code: response.status });
      // auth.loginWithJwt(response.headers["x-auth-token"]);
      // TODO response code check
      // window.location = "/";
      // this.checkStatus = this.checkStatus.bind(response.status);
      if (response.status) {
        if (response.status === 202) {
          toast.error("User Already Exists");
        } else if (response.status === 201) {
          this.props.history.push("/login");
          toast.success("Check ur Email");
          console.log("Successfully register");
        } else {
          toast.error("Unknown ERROR");
        }
      }
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
    console.log(this.props.location.state);
    if (auth.isLoggedIn() === true) return <Redirect to="/" />;

    return (
      <div>
        <ToastContainer />
        <h1>Register</h1>
        <form onSubmit={this.handleSubmit}>
          {this.renderInput("name", "Name")}
          {this.renderInput("email", "Email")}
          {this.renderInput("password", "Password", "password", "cpassword")}
          {this.renderButton("Register", this.state.code)}
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
