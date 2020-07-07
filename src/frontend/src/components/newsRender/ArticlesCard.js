import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import GridListTileBar from '@material-ui/core/GridListTileBar';
import IconButton from '@material-ui/core/IconButton';
import LoyaltyIcon from '@material-ui/icons/Loyalty';


const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    //flexWrap: 'wrap',
    justifyContent: 'space-around',
    overflow: 'hidden',
    backgroundColor: theme.palette.background.paper,
  },
  gridList: {
    width: 1100,
    height: 450,
  },
  icon: {
    color: 'rgba(255, 255, 255, 0.54)',
  },
}));


export default function TitlebarGridList(props) {

  const classes = useStyles();
  const { details } = props;

  return (
    
    <div className={classes.root}>
      <GridList   className={classes.gridList}>
        {details.map((news) => (
          <GridListTile key={news.public_id}>
            <img src={news.img} alt={news.title} />
            <GridListTileBar
              title={<a href={news.url} style={{ textDecoration: 'none', color: 'white'}}>{news.title}</a>}
              subtitle={<span>by: {news.source}</span>}
              actionIcon={
                <IconButton aria-label={`info about ${news.title}`} className={classes.icon}>
                  <LoyaltyIcon  />
                </IconButton>
                
              }
            />
            
          </GridListTile>
        ))}
      </GridList>
    </div>
  );
}