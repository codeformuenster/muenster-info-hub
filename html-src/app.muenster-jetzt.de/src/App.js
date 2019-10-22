import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import SearchBar from "./components/SearchBar";
import Events from './components/Events';
import { DataProvider } from "./DataContext";

import logo from "./logo.png";

const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(3, 2)
  },
  logo: {
    width: "86%",
    maxWidth: "420px",
    margin: theme.spacing(1),
    marginBottom: 0
  }
}));

function App() {
  const classes = useStyles();

  return (
    <div>
      <DataProvider>
        <img src={logo} alt="münster.jetzt logo" className={classes.logo} />
        <SearchBar />
        <Events />
      </DataProvider>
    </div>
  );
}

export default App;
