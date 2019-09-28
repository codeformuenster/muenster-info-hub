import React, { useState, useEffect } from 'react';
import { makeStyles } from "@material-ui/core/styles";
import EventCard from "./components/EventCard";
import SearchBar from "./components/SearchBar";
import axios from 'axios';
import * as R from 'ramda';

import logo from './logo.png';

const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(3, 2)
  },
  logo: {
      width: '86%',
      maxWidth: '420px',
      margin: theme.spacing(1),
      marginBottom: 0,
  }
}));

function sortByDate(events) {
 return events.sort(function(a,b){
    return a.time - b.time;
  });
}

function removePastEvents(events) {
  return R.filter(n => n.time >= new Date(), events);
};


function App() {
  const classes = useStyles();

  const [events, setEvents] = useState([]);

  useEffect( () => {
    const fetchEvent = async() => {
      const result = await axios.get(`/_search?size=20`);
      const events = result.data.hits.hits.map(({
        _id: id,
        _source: { link, title, category, subtitle, start_date, images, location_name, description }
      }) => (
        {
          id,
          title: title,
          time: new Date(start_date),
          image: images ? images[0].image_url : null,
          link,
          description,
          place: location_name,
          kicker: subtitle,
          category
        }
      ));

      const polishedEvents = R.pipe(
        sortByDate,
        removePastEvents
      )(events)

      setEvents(polishedEvents)}
    fetchEvent();
  }, []);

  return (
    <div>
      <img src={logo} alt="münster.jetzt logo" className={classes.logo} />
      <SearchBar />
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
    </div>
  );
}

export default App;
