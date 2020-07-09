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
import {
  TwitterShareButton,WhatsappShareButton,EmailShareButton,TelegramShareButton
} from 'react-share';
import {
  EmailIcon,TelegramIcon,TwitterIcon,WhatsappIcon
} from "react-share";
import './Share.css';

const useStyles = makeStyles({
  root: {
    maxWidth: 350,
    margin: 0,
    padding: 0
  },
  media: {
    height: 140
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
          <TwitterShareButton
            url={url}
            title={title}
            className="Demo__some-network__share-button"
          >
            <TwitterIcon size={32} round />
          </TwitterShareButton>
          </IconButton>
          <IconButton aria-label="share">
          <WhatsappShareButton
            url={url}
            title={title}
            separator=":: "
            className="Demo__some-network__share-button"
          >
            <WhatsappIcon size={32} round />
          </WhatsappShareButton>
        </IconButton>
        <IconButton aria-label="share">
        <EmailShareButton
            url={url}
            subject={title}
            body="body"
            className="Demo__some-network__share-button"
          >
            <EmailIcon size={32} round />
          </EmailShareButton>
          </IconButton>
      </CardActions>
    </Card>
  );
}