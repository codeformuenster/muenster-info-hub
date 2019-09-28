import React from "react";
import axios from "axios";
import * as R from "ramda";
import { useDebounce } from "use-debounce";

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

function onlyShowEventsWithImages(events) {
  return R.filter(event => event.image !== null, events);
}

function sanitizeCategories(events) {
  return events.map(event => {
    if (event.category === "top") {
      event.category = "TOP-Event";
      return event;
    } else {
      return event;
    }
  });
}

function sanatizeSources(events) {
  return events.map(event => {
    if (event.source === "www.muenster.de") {
      event.source = "muenster.de";
      return event;
    } else {
      return event;
    }
  });
}

const DataProvider = ({ children }) => {
  const [searchPhrase, setSearchPhrase] = React.useState("");
  const [events, setEvents] = React.useState([]);
  const [searchPhraseDebounced] = useDebounce(searchPhrase, 200);

  React.useEffect(() => {
    const fetchEvent = async () => {
      const {
        data: {
          hits: { hits }
        }
      } = await axios.post(
        "https://api.muenster.jetzt/msinfohub-events/_search?size=2000",
        searchPhrase.trim() !== ""
          ? {
              query: {
                wildcard: {
                  title: `*${searchPhraseDebounced.trim().toLowerCase()}*`
                }
                // { match: { content: "Elasticsearch" } }
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
            source,
            location_address,
            description
          }
        }) => ({
          id,
          title: title,
          time: new Date(start_date),
          image: images ? images[0].image_url : null,
          source,
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
        removePastEvents,
        onlyShowEventsWithImages,
        sanitizeCategories,
        sanatizeSources
      )(events);

      setEvents(polishedEvents);
    };
    fetchEvent();
  }, [searchPhraseDebounced]);

  return (
    <DataContext.Provider value={{ setSearchPhrase, events }}>
      {children}
    </DataContext.Provider>
  );
};

export { DataContext as default, DataProvider };
