import React from "react";
import EventCard from "./EventCard";
import DataContext from "../DataContext";
import Grid from "@material-ui/core/Grid";

const Events = () => {
  const { events } = React.useContext(DataContext);

  return (
    <Grid container>
      {events.map((event, i) => (
        <Grid item key={event.id} xs="12" sm="6" md="4" lg="3" xl="2">
          <EventCard
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
        </Grid>
      ))}
    </Grid>
  );
};

export default Events;
