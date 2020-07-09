// import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import React, { useState } from "react";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Switch from "@material-ui/core/Switch";
import { withStyles } from "@material-ui/core/styles";
import apiurl from "../../config.json";
import Checkbox from "@material-ui/core/Checkbox";
import TextField from "@material-ui/core/TextField";
import Autocomplete from "@material-ui/lab/Autocomplete";
import CheckBoxOutlineBlankIcon from "@material-ui/icons/CheckBoxOutlineBlank";
import CheckBoxIcon from "@material-ui/icons/CheckBox";
import axios from "axios";
import Button from "@material-ui/core/Button";
import { makeStyles } from "@material-ui/core/styles";

import SaveIcon from "@material-ui/icons/Save";

// const useStyles = makeStyles({
//   root: {
//     color: "#2196f3",
//   },
//   text: {
//     color: "#e1f5fe",
//   },
// });

const useStyles = makeStyles((theme) => ({
  button: {
    margin: theme.spacing(1),
  },
}));

const icon = <CheckBoxOutlineBlankIcon fontSize="small" />;
const checkedIcon = <CheckBoxIcon fontSize="small" />;

const IOSSwitch = withStyles((theme) => ({
  root: {
    width: 42,
    height: 26,
    padding: 0,
    margin: theme.spacing(1),
  },
  switchBase: {
    padding: 1,
    "&$checked": {
      transform: "translateX(16px)",
      color: theme.palette.common.white,
      "& + $track": {
        backgroundColor: "#52d869",
        opacity: 1,
        border: "none",
      },
    },
    "&$focusVisible $thumb": {
      color: "#52d869",
      border: "6px solid #fff",
    },
  },
  thumb: {
    width: 24,
    height: 24,
  },
  track: {
    borderRadius: 26 / 2,
    border: `1px solid ${theme.palette.grey[400]}`,
    backgroundColor: theme.palette.grey[50],
    opacity: 1,
    transition: theme.transitions.create(["background-color", "border"]),
  },
  checked: {},
  focusVisible: {},
}))(({ classes, ...props }) => {
  return (
    <Switch
      focusVisibleClassName={classes.focusVisible}
      disableRipple
      classes={{
        root: classes.root,
        switchBase: classes.switchBase,
        thumb: classes.thumb,
        track: classes.track,
        checked: classes.checked,
      }}
      {...props}
    />
  );
});

const news = async ({ Account }) => {
  const notifyCall = apiurl + "/change-preference";
  const response = await axios
    .get(notifyCall, {
      headers: {
        "x-access-token": localStorage.getItem("token"),
      },
    })
    .catch((err) => {
      Account.preferences = err.response.status;
      console.log(err.response.status);
    });
  try {
    Account.preferences = response;
    console.log(Account.preferences);
  } catch (error) {
    console.log(error);
  }
};

const AccountDetails = ({ Account }) => {
  const apiEndpoint = apiurl.apiUrl + "/email-notification";
  const classes = useStyles();
  console.log({ Account });
  const [button, setButton] = useState({
    checked: Account.email_notify,
  });
  var arr = [];
  arr = Account.preferences;

  const [save, setSave] = useState(arr);
  console.log(save);
  const handleSave = async (event) => {
    console.log({});
  };

  // const [button, setButton] = useState({
  //   checked: Account.email_notify,
  // });
  const handleChange = async (event) => {
    setButton({ checked: event.target.checked });

    const notify = button.checked;

    const response = await axios
      .put(
        apiEndpoint,
        { email_notify: !notify },
        {
          headers: {
            "x-access-token": localStorage.getItem("token"),
          },
        }
      )
      .then((res) => {
        window.location = "/profile";
      })
      .catch((err) => {
        // console.log(err);
      });
    try {
      const profile = response;
      console.log(profile);
    } catch (error) {}
  };
  const categories = [
    { title: "Science and Technology" },
    { title: "Business" },
    { title: "Entertainment" },
    { title: "Health" },
  ];

  return (
    <Card>
      <CardContent>
        <Typography gutterBottom variant="h5" component="h2">
          Name: {Account.first_name} {Account.last_name}
        </Typography>
        <Typography gutterBottom variant="h5" component="h2">
          Email: {Account.email}
        </Typography>
        <Typography gutterBottom variant="h5" component="h2">
          Joined on: {Account.joined_on}
        </Typography>
        <Typography gutterBottom variant="h5" component="h2">
          email_notify:{"            "}
          <FormControlLabel
            control={
              <IOSSwitch
                checked={button.checked}
                onChange={handleChange}
                name="checked"
              />
            }
          />
        </Typography>
        <Typography gutterBottom variant="h5" component="h2">
          Preferences:
          <Autocomplete
            multiple
            id="checkboxes-tags-demo"
            disabled={!Account.email_notify}
            options={categories}
            disableCloseOnSelect
            getOptionLabel={(option) => option.title}
            renderOption={(option, { selected }) => (
              <React.Fragment>
                <Checkbox
                  icon={icon}
                  checkedIcon={checkedIcon}
                  style={{ marginRight: 8 }}
                  checked={selected}
                />
                {console.log(selected)}
                if(selected) setSave(option.title)
                {option.title}
                {console.log(option.title)}
              </React.Fragment>
            )}
            style={{ width: "70%" }}
            renderInput={(params) => (
              <TextField
                {...params}
                variant="outlined"
                label="Newspaper"
                placeholder="Favorites"
              />
            )}
          />
          <Button
            onClick={handleSave}
            variant="contained"
            color="primary"
            size="large"
            className={classes.button}
            startIcon={<SaveIcon />}
          >
            Save
          </Button>
        </Typography>
        <Typography gutterBottom variant="h5" component="h2">
          saved_article: {Account.saved_article}
        </Typography>
      </CardContent>
    </Card>
  );
};
export default AccountDetails;
