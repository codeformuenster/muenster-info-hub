import React from "react";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(theme => ({
  searchBar: {
    margin: theme.spacing(1),
  }
}));

const SearchBar = () => {
  const classes = useStyles();
  return <input type="text" className={classes.searchBar} />;
};

export default SearchBar;
