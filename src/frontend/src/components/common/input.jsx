import React from "react";

const Input = ({ name, label, error, errors, field, ...rest }) => {
  if (name === "name") {
    return (
      <div className="row form-group">
        <div className="col">
          <label htmlFor="fname">First Name</label>
          <input {...rest} name="fname" id="fname" className="form-control" />
          {errors["fname"] && (
            <div className="alert alert-danger">{errors["fname"]}</div>
          )}
        </div>
        <div className="col">
          <label htmlFor="lname">Last Name</label>
          <input {...rest} name="lname" id="lname" className="form-control" />
          {errors["lname"] && (
            <div className="alert alert-danger">{errors["lname"]}</div>
          )}
        </div>
      </div>
    );
  } else if (name === "password" && field === "cpassword") {
    return (
      <div className="row form-group">
        <div className="col">
          <label htmlFor={name}>{label}</label>
          <input {...rest} name={name} id={name} className="form-control" />
          {error && <div className="alert alert-danger">{error}</div>}
        </div>
        <div className="col">
          <label htmlFor="cpassword">Confirm Password</label>
          <input
            {...rest}
            type="password"
            name="cpassword"
            id="cpassword"
            className="form-control"
          />
        </div>
      </div>
    );
  } else {
    return (
      <div className="form-group">
        <label htmlFor={name}>{label}</label>
        <input {...rest} name={name} id={name} className="form-control" />
        {error && <div className="alert alert-danger">{error}</div>}
      </div>
    );
  }
};

export default Input;
