import React from 'react';
import * as ReactBootStrap from "react-bootstrap";
import ExitToAppIcon from '@material-ui/icons/ExitToApp';
import FaceIcon from '@material-ui/icons/Face';
import {
    BrowserRouter as Router,
    Link
  } from "react-router-dom";

const NavBarr = ({ user }) => {
    return(
        <div className="App">
    <ReactBootStrap.Navbar fixed-top collapseOnSelect expand="xl" bg="dark"  variant="dark">
  <ReactBootStrap.Navbar.Brand href="/">Newssy</ReactBootStrap.Navbar.Brand>
  <ReactBootStrap.Navbar.Toggle aria-controls="responsive-navbar-nav" />
  <ReactBootStrap.Navbar.Collapse id="responsive-navbar-nav">
   { !user && <ReactBootStrap.Nav>
    <Link to="/signup">
    <ReactBootStrap.Nav.Link href="/signup">Register</ReactBootStrap.Nav.Link>
    </Link>
    <Link to="/login">
    <ReactBootStrap.Nav.Link eventKey={2} href="/login">
    <i class="fa fa-sign-in" aria-hidden="true"></i> Login
      </ReactBootStrap.Nav.Link>
    </Link>
    </ReactBootStrap.Nav>}
   { user && <ReactBootStrap.Nav>
    <Link to="/profile">
    <ReactBootStrap.Nav.Link href="/profile"><FaceIcon/></ReactBootStrap.Nav.Link>
    </Link>
    <Link to="/logout">
    <ReactBootStrap.Nav.Link eventKey={2} href="/logout">
        <ExitToAppIcon/> Logout
      </ReactBootStrap.Nav.Link>
    </Link>
    </ReactBootStrap.Nav>}
  </ReactBootStrap.Navbar.Collapse>
</ReactBootStrap.Navbar>
        </div>
    )
}

export default NavBarr;