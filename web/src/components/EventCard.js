import React from "react";
import Paper from "@material-ui/core/Paper";
import './EventCard.css'

import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(3, 2),
    margin: theme.spacing(2, 2),
    display: 'grid',

  }
}));

function EventCard({title, time, place, tags, image, description, lat, lon}) {
  const classes = useStyles();

  const [isExpanded, setExpanded] = React.useState(false);

  return (
    <Paper
      className={classes.root}>
      <div className="grid-container">
        <div className="title">{title}</div>
        <div className="info">
          <div className="stats">
            <div className="time">{time}</div>
            <div className="place">{place}</div>
    {tags.map(tag =>
    <div className="tags">{tag}</div>
    )}
          </div>
          <div className="image">
            <img className="event-image" src={image} alt="das Bild" />
          </div>
        </div>
      </div>
    </Paper>
  );
}

export default EventCard;
