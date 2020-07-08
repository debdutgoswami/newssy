import React, {useEffect} from "react";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import Input from "@material-ui/core/Input";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import Chip from "@material-ui/core/Chip";
import axios from 'axios';
//import ArticlesCard from './ArticlesCard'
import NewsCard from './NewsCard'
import Grid from '@material-ui/core/Grid'
import Button from '@material-ui/core/Button'
import Buttonss from './Buttonss'

const useStyles = makeStyles(theme => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
    maxWidth: 500
  },
  chips: {
    display: "flex"
  },
  chip: {
    margin: 2
  },
  noLabel: {
    marginTop: theme.spacing(3)
  }
}));

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250
    }
  }
};

const names = ["Science and Technology", "Health", "Business", "Entertainment"];
const sources = ["BBC News", "times of india"]

function getStyles(name, personName, theme) {
  return {
    fontWeight:
      personName.indexOf(name) === -1
        ? theme.typography.fontWeightRegular
        : theme.typography.fontWeightMedium
  };
}
function getStyles1(sources, sourceName, theme) {
  return {
    fontWeight:
      sourceName.indexOf(sources) === -1
        ? theme.typography.fontWeightRegular
        : theme.typography.fontWeightMedium
  };
}

export default function MultipleSelect(props) {
  const classes = useStyles();
  const theme = useTheme();
  const [personName, setPersonName] = React.useState([]);   
  const [sourceName, setSourceName] = React.useState([]);   
  const [data, setData ] = React.useState([])

  useEffect(() => {
       axios.post('http://104.197.245.159:5000/api/get-news', {
        category: [...personName],
        source: [...sourceName],
        per_page: 20
       })
        .then(res => setData(res.data.articles))
        .catch( err => console.error(err))
  }, [personName, sourceName ])


  

 const handleChange = event => {
    setPersonName(event.target.value);
  };

 const OnsourceChange = e => {
   setSourceName(e.target.value)
 } 
  console.log(personName);
  return (
    <div>
      <FormControl className={classes.formControl}>
        <InputLabel id="demo-mutiple-chip-label">Categories</InputLabel>
        <Select
          labelId="demo-mutiple-chip-label"
          id="demo-mutiple-chip"
          multiple
          value={personName}
          onChange={handleChange}
          input={<Input id="select-multiple-chip" />}
          renderValue={selected => (
            <div className={classes.chips}>
              {selected.map(value => (
                <Chip key={value} label={value} className={classes.chip} />
              ))}
            </div>
          )}
          MenuProps={MenuProps}
        >
          {names.map(name => (
            <MenuItem
              key={name}
              value={name}
              style={getStyles(name, personName, theme)}
            >
              {name}
            </MenuItem>
          ))}
        </Select>
        </FormControl>
        <FormControl className={classes.formControl}>
        <InputLabel id="demo-mutipl-chip-label">Sources</InputLabel>
        <Select
          labelId="demo-mutipl-chip-label"
          id="demo-mutipl-chip"
          multiple
          value={sourceName}
          onChange={OnsourceChange}
          input={<Input id="select-multipl-chip" />}
          renderValue={selected => (
            <div className={classes.chips}>
              {selected.map(value => (
                <Chip key={value} label={value} className={classes.chip} />
              ))}
            </div>
          )}
          MenuProps={MenuProps}
        >
          {sources.map(source => (
            <MenuItem
              key={source}
              value={source}
              style={getStyles1(sources, sourceName, theme)}
            >
              {source}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <br/>
      <Grid
      container
      spacing={10}
      styles={{padding:'10px' ,margin: '15px'}}
      >
      {data.map(news => (
      <Grid item xs={12} sm={6} md={4} lg={4} xl={3}>   
      <NewsCard 
      description={news.body}
      title={news.title}
      img={news.img}
      url={news.url}
      id={news.public_id}
      />
      </Grid>  
      ))}
      </Grid>
      <br/>
      <Buttonss />
    </div>
  );
}
