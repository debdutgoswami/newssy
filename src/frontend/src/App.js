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

class App extends Component {
  state = {};

  componentDidMount() {
    const user = auth.getCurrentUser();
    this.setState({ user });
  }

  render() {
    const { user } = this.state;

    return (
      <React.Fragment>
        <ToastContainer />
        <CssBaseline />
        <NavBar user={user} />
        <main className="container">
          <Switch>
            <Route path="/signup" component={RegisterForm} />
            <Route path="/login" component={LoginForm} />
            <Route path="/logout" component={Logout} />
            {/* <ProtectedRoute path="/news/:id" component={MovieForm} />
            <Route
              path="/news"
              render={(props) => <Movies {...props} user={this.state.user} />}
            /> */}
            <Route path="/news" component={news} />
            <Route path="/resend" component={Resend} />
            <Route path="/not-found" component={NotFound} />
            <Route path="/confirm" component={Token} />
            <Redirect from="/" exact to="/news" />
            <Redirect to="/not-found" />
          </Switch>
        </main>
      </React.Fragment>
    );
  }
}

export default App;
