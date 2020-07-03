import React from "react";
import { Redirect } from "react-router-dom";
const codeStatus = ({ code }) => {
  if (code === 201) {
    render(){
      return (
        <Redirect to={{ pathname: "/login", state: { account: true } }} />
      
      )}















  } else {
    return <link to={{ pathname: "/signup", state: { codes: code } }} />;
  }
};

export default codeStatus;
