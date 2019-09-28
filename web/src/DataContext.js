import React from "react";
import axios from "axios";
import * as R from "ramda";

const DataContext = React.createContext({
  setSearchPhrase: () => {},
  events: []
});

function sortByDate(events) {
  return events.sort(function(a, b) {
    return a.time - b.time;
  });
}

function removePastEvents(events) {
  return R.filter(n => n.time >= new Date(), events);
}

const DataProvider = ({ children }) => {
  const [searchPhrase, setSearchPhrase] = React.useState("");
  const [events, setEvents] = React.useState([]);

  React.useEffect(() => {
    const fetchEvent = async () => {
      const {
        data: {
          hits: { hits }
        }
      } = await axios.post(
        "https://api.muenster.jetzt/infohub/_search?size=20",
        searchPhrase.trim() !== ""
          ? {
              query: {
                bool: {
                  must: [
                    { match: { title: searchPhrase.trim() } }
                    // { match: { content: "Elasticsearch" } }
                  ]
                }
              }
            }
          : undefined
      );
      const events = hits.map(
        ({
          _id: id,
          _source: {
            link,
            title,
            category,
            subtitle,
            start_date,
            images,
            location_name,
            location_address,
            description
          }
        }) => ({
          id,
          title: title,
          time: new Date(start_date),
          image: images ? images[0].image_url : null,
          link,
          description,
          place: location_name,
          address: location_address,
          kicker: subtitle,
          category
        })
      );

      const polishedEvents = R.pipe(
        sortByDate,
        removePastEvents
      )(events);

      setEvents(polishedEvents);
    };
    fetchEvent();
  }, [searchPhrase]);

  return (
    <DataContext.Provider value={{ setSearchPhrase, events }}>
      {children}
    </DataContext.Provider>
  );
};

export { DataContext as default, DataProvider };
