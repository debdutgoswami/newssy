import React, { useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import Grid from "@material-ui/core/Grid";
import AccountCircle from "@material-ui/icons/AccountCircle";
import { apiUrl } from "../config.json";
import axios from "axios";
import { toast, ToastContainer } from "react-toastify";

const useStyles = makeStyles((theme) => ({
  margin: {
    margin: theme.spacing(1),
  },
  root: {
    "& > *": {
      margin: theme.spacing(1),
    },
  },
}));
///////////////////////////////////////////////////////////////////////
export default function Resend() {
  const apiEndpoint = apiUrl + "/";
  const classes = useStyles();
  const [value, setValue] = useState("");
  const handleChange = (email) => {
    setValue(email.target.value);
  };
  const submit = () => {
    toast("Check Your Email");
    console.log(value);
    return axios.post(apiEndpoint, {
      email: value,
    });
  };
  return (
    <div>
      <div className={classes.margin}>
        <Grid container spacing={1} alignItems="flex-end">
          <Grid item>
            <AccountCircle />
          </Grid>
          <Grid item>
            <TextField
              id="input-with-icon-grid"
              label="Email"
              onChange={handleChange}
            />
          </Grid>
          <div className={classes.root}>
            <ToastContainer />
            <Button
              variant="outlined"
              color="primary"
              onClick={submit}
              disabled={!value}
            >
              Resend
            </Button>
          </div>
        </Grid>
      </div>
    </div>
  );
}
