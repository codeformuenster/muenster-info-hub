import React from "react";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";
import "./EventCard.css";

import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(1),
    margin: theme.spacing(2, 2)
  }
}));

function EventCard({ title, time, place, tags, image, description, lat, lon }) {
  const classes = useStyles();

  const [isExpanded, setExpanded] = React.useState(false);

  return (
    <Paper className={classes.root}>
      <div className="grid-container">
        <div className="title">
          <Typography variant="h5" component="h2" gutterBottom={2}>
            {title}
          </Typography>
        </div>
        <div className="info">
          <div className="stats">
            <div className="time">{time}</div>
            <div className="place">{place}</div>
            <div className="tags">
              {tags.map(tag => (
                <span key={tag}>{tag}</span>
              ))}
            </div>
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
