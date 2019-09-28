import React from "react";
import EventCard from "./EventCard";
import DataContext from "../DataContext";

const Events = () => {
  const { events } = React.useContext(DataContext);

  return (
    <>
      {events.map(event => (
        <EventCard
          key={event.id}
          {...event}
          title={event.title}
          kicker={event.kicker}
          link={event.link}
          time={event.time}
          place={event.place}
          tags={[event.category]}
          image={event.image}
          description={event.description}
        />
      ))}
    </>
  );
};

export default Events;
