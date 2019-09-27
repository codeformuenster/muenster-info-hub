import React from "react";
import logo from "./logo.svg";
import "./App.css";
import Paper from "@material-ui/core/Paper";
import { makeStyles } from "@material-ui/core/styles";
import EventCard from "./components/EventCard";

const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(3, 2)
  }
}));

function App() {
  const classes = useStyles();

  return (
    <div className="App">
      <header className="App-header">
        <EventCard
          title='Nützliche und schädliche „Beziehungskisten“ im Naturkundemuseum'
          time='ab 19:00 Uhr'
          place='Sputnikhalle'
          tags={['#techno', '#freieliebe']}
          image='https://www.wn.de/var/storage/images/wn/startseite/fotos/freizeit/3977199-das-ist-los-am-wochenende-27.-29.-september/jhf0078854/110570507-1-ger-DE/JHF0078854_image_1024_width.jpg'
          description='DJ Frank läd ein zum abendlichen Zappeln, natürlich wie immer im Bademantel.Die 14. Covernight startet am Samstag (28. September) um 20 Uhr im Kinderhauser Bürgerhaus; Einlass ab 19.30 Uhr. Fester Bestandteil der  Livemusik-Party ist die Band „Undercover“.'
    />
        <EventCard
          title='Nützliche und schädliche „Beziehungskisten“ im Naturkundemuseum'
          time='ab 19:00 Uhr'
          place='Sputnikhalle'
          tags={['#techno', '#freieliebe']}
          image='https://www.wn.de/var/storage/images/wn/startseite/fotos/freizeit/3977199-das-ist-los-am-wochenende-27.-29.-september/jhf0078854/110570507-1-ger-DE/JHF0078854_image_1024_width.jpg'
          description='DJ Frank läd ein zum abendlichen Zappeln, natürlich wie immer im Bademantel.Die 14. Covernight startet am Samstag (28. September) um 20 Uhr im Kinderhauser Bürgerhaus; Einlass ab 19.30 Uhr. Fester Bestandteil der  Livemusik-Party ist die Band „Undercover“.'
    />
      </header>
    </div>
  );
}

export default App;
