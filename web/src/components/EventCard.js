import React from "react";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";
import ClockIcon from "@material-ui/icons/WatchLater";

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
        background: `linear-gradient( rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6) ), url(${image})`
      }}
    >
      <div className="grid-container">
        <div className="title">
          <Typography
            variant="h6"
            component="h2"
            gutterBottom={2}
            className={classes.title}
          >
            {title.length > 50 ? <>{title.substring(0, 50)}&hellip;</> : title}
          </Typography>
        </div>
        <div className="info">
          <div className="stats">
            <div className="time">
              <ClockIcon /> {time}
            </div>
            <div className="place">{place}</div>
            <div className="tags">
              {tags.map(tag => (
                <span key={tag} className={classes.tag}>
                  {tag}
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
