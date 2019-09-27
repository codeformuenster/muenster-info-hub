import React from "react";
import logo from "./logo.svg";
import "./App.css";
import Paper from "@material-ui/core/Paper";
import { makeStyles } from "@material-ui/core/styles";

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
        <Paper className={classes.root}>
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </Paper>
      </header>
    </div>
  );
}

export default App;
