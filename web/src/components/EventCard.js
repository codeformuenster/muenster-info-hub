import React from "react";
import * as moment from 'moment';
import 'moment/locale/de';
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";
import RoomIcon from '@material-ui/icons/Room';
import ClockIcon from "@material-ui/icons/WatchLater";
import LabelIcon from '@material-ui/icons/Label';


import "./EventCard.css";

import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(1),
    margin: theme.spacing(2, 2),
    color: "white"
  },
  tag: {
    fontVariant: "small-caps"
  },
  title: {
    letterSpacing: 1
  }
}));

function EventCard({ title, time, place, tags, image, description, lat, lon }) {
  const classes = useStyles();

  const [isExpanded, setExpanded] = React.useState(false);

  return (
    <Paper
      className={classes.root}
      elevation={3}
      style={{
        background: `linear-gradient( rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6) ), url(${image})`,
        backgroundSize: 'cover'
      }}
    >
      <div className="grid-container">
        <div className="title">
          <Typography
            variant="h6"
            component="h2"
            gutterBottom
            className={classes.title}
          >
            {title.length > 50 ? <>{title.substring(0, 50)}&hellip;</> : title}
          </Typography>
        </div>
        <div className="info">
          <div className="stats">
            <div className="time">
              <ClockIcon /> {moment(time).fromNow()}
            </div>
            <div className="place">
              <RoomIcon /> {place}</div>
            <div className="tags">
              {tags.map(tag => (
                <span key={tag} className={classes.tag}>
                  <LabelIcon /> {tag}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </Paper>
  );
}

export default EventCard;
