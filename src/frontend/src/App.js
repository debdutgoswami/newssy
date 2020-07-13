import React, { Component } from "react";
import { Route, Redirect, Switch } from "react-router-dom";
import LoginForm from "./components/loginForm";
import RegisterForm from "./components/registerForm";
import { ToastContainer } from "react-toastify";
import NotFound from "./components/notFound";
import Logout from "./components/logout";
//import ProtectedRoute from "./components/common/protectedRoute";
import NavBar from "./components/navBar";
import auth from "./services/authService";
import "react-toastify/dist/ReactToastify.css";
import "./App.css";
import news from "./components/news";
import Token from "./components/TokenVerify";
import CssBaseline from "@material-ui/core/CssBaseline";
import Resend from "./components/resend";
import Newssy from "./components/newsRender/App";
import Footer from "./components/footer";
import NavBarr from "./components/navBarr";
import Profile from "./components/Profile";

class App extends Component {
  state = {};

  componentDidMount() {
    const user = auth.getCurrentUser();
    this.setState({ user });
  }

  render() {
    const { user } = this.state;

    return (
      <div className="page-container">
        <div className="content-wrap">
          <ToastContainer autoClose={4000} />
          <CssBaseline />
          {/* <NavBar user={user} /> */}
          <NavBarr user={user} />
          <main className="container">
            <Switch>
              <Route path="/signup" component={RegisterForm} />
              <Route path="/login" component={LoginForm} />
              <Route path="/logout" component={Logout} />
              <Route path="/news" component={Newssy} />
              <Route path="/resend" component={Resend} />
              <Route path="/not-found" component={NotFound} />
              <Route path="/profile" component={Profile} />
              <Route path="/confirm" component={Token} />

              <Redirect from="/" exact to="/news" />
              <Redirect to="/not-found" />
            </Switch>
          </main>
        </div>
        <br />
        <Footer />
      </div>
    );
  }
}

export default App;
