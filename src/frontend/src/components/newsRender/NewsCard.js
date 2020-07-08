import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import FavoriteIcon from '@material-ui/icons/Favorite';
import ShareIcon from '@material-ui/icons/Share';

const useStyles = makeStyles({
  root: {
    maxWidth: 345,
  },
  media: {
    height: 140,
  },
});

export default function NewsCard({description, title, img, url, id}) {
  const classes = useStyles();
  let desc = description.slice(0,)
  return (
    <Card className={classes.root}>
      <CardActionArea>
        <CardMedia
          className={classes.media}
          image={img}
          title={title}
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="h2">
            <a href={url} styles={{decoration: "none"}}>{title}</a>
          </Typography>
          <Typography variant="body2" color="textSecondary" component="p">
           {description}
          </Typography>
        </CardContent>
      </CardActionArea>
      <CardActions disableSpacing>
        <IconButton aria-label="add to favorites">
            <FavoriteIcon color="secondary"/>
        </IconButton>
        <IconButton aria-label="share">
            <ShareIcon  color="primary"/>
        </IconButton>
      </CardActions>
    </Card>
  );
}