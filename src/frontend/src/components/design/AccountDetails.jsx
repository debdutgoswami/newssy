// import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import React, { useState, useEffect } from "react";
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
import Chip from "@material-ui/core/Chip";
import Box from "@material-ui/core/Box";
import CloseIcon from "@material-ui/icons/Close";
import SaveIcon from "@material-ui/icons/Save";
import { Link } from "@material-ui/core";
import Fab from "@material-ui/core/Fab";
import DeleteForeverIcon from "@material-ui/icons/DeleteForever";
import { Redirect } from "react-router-dom";

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
  margin: {
    margin: theme.spacing(1),
  },
  extendedIcon: {
    marginRight: theme.spacing(1),
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

async function save(arr) {
  const notifyCall = apiurl.apiUrl + "/change-preference";
  const response = await axios
    .put(
      notifyCall,
      { preference: arr },
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
      console.log(err);
    });
  try {
    const profile = response;
    console.log(profile);
  } catch (error) {}
}

const AccountDetails = ({ Account }) => {
  const apiEndpoint = apiurl.apiUrl + "/email-notification";
  const classes = useStyles();
  console.log({ Account });
  const [button, setButton] = useState({
    checked: Account.email_notify,
  });
  var arr = [];
  // arr = Account.preferences;
  var i = 0;

  const handleSave = async () => {
    let x = 0;
    var i;
    for (i = 0; i < 4; i++) {
      if (categories[i].status === true) {
        arr[x++] = categories[i].title;
      }
    }
    save(arr);

    arr = [];
  };

  async function HandleNews(event) {
    console.log(event);
    const notifyCall = apiurl.apiUrl + "/delete-saved-article";
    const response = await axios
      .put(
        notifyCall,
        { preference: event.public_id },
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
        console.log(err);
      });
    try {
      const profile = response;
      console.log(profile);
    } catch (error) {}
  }
  useEffect(() => {
    async function fetchData() {
      const notify = button.checked;
      try {
        await axios
          .put(
            apiEndpoint,
            { email_notify: notify },
            {
              headers: {
                "x-access-token": localStorage.getItem("token"),
              },
            }
          )
          .then((res) => {
            console.log(res);
            // setButton(res.datat)
          })
          .catch((err) => {
            console.log(err);
          });
      } catch (error) {
        console.error(error);
      }
    }
    fetchData();
  }, [button.checked]);
  const categories = [
    { title: "Science and Technology", status: false },
    { title: "Business", status: false },
    { title: "Health", status: false },
    { title: "Entertainment", status: false },
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
          Email Subscription:{"            "}
          <FormControlLabel
            control={
              <IOSSwitch
                checked={button.checked}
                onChange={(event) => {
                  setButton({ checked: event.target.checked });
                }}
                name="checked"
              />
            }
          />
          {console.log(button.checked)}
        </Typography>

        <Typography gutterBottom variant="h5" component="h2">
          Preferences: &nbsp;
          {Account.email_notify &&
            Account.preferences &&
            Account.preferences.map((item) => (
              <Chip clickable color="primary" label={item} />
            ))}
          <Autocomplete
            multiple
            id="checkboxes-tags-demo"
            disabled={!button.checked}
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
                {console.log(option.title)}
                {console.log(selected)}
                {option.title}
                {(categories[i++].status = selected)}
                {(i === 4 && (i = 0)) || null}
              </React.Fragment>
            )}
            renderTags={(tagValue, getTagProps) =>
              tagValue.map((option, index) => (
                <Chip
                  color="primary"
                  label={option.title}
                  {...getTagProps({ index })}
                  disabled="true"
                />
              ))
            }
            style={{ width: "70%" }}
            renderInput={(params) => (
              <TextField
                {...params}
                label="Fixed tag"
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
          <Autocomplete
            id="combo-box-demo"
            options={Account.saved_article}
            getOptionLabel={(option) => option.title}
            renderOption={(option) => (
              <React.Fragment>
                <a
                  style={{ textDecoration: "none", width: "100%" }}
                  href={option.url}
                >
                  {option.title}
                </a>

                <Button onClick={() => HandleNews(option)}>
                  <DeleteForeverIcon />
                </Button>
              </React.Fragment>
            )}
            style={{ width: "70%" }}
            renderInput={(params) => (
              <TextField {...params} label="Saved Article" variant="outlined" />
            )}
          />
        </Typography>
      </CardContent>
    </Card>
  );
};
export default AccountDetails;
