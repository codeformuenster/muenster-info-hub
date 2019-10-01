import React from "react";
import EventCard from "./EventCard";
import DataContext from "../DataContext";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(theme => ({
  eventslist: {
    display: "flex"
  }
}));

const Events = () => {
  const { events } = React.useContext(DataContext);
  const classes = useStyles();

  return (
    <div className={classes.eventslist}>
      {events.map(event => (
        <EventCard
          key={event.id}
          {...event}
          title={event.title}
          kicker={event.kicker}
          link={event.link}
          time={event.time}
          place={event.place}
          address={event.address}
          tags={[event.category]}
          image={event.image}
          description={event.description}
        />
      ))}
    </div>
  );
};

export default Events;
