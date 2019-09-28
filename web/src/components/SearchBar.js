import React from "react";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(theme => ({
  searchBar: {
    // margin: theme.spacing(0),
    padding: theme.spacing(1),
    width: `calc(100% - ${theme.spacing(4)}px)`,
    fontSize: theme.typography.h5.fontSize
  },
  wrapper: {
    display: "flex",
    justifyContent: 'center',
    margin: theme.spacing(1, 2, -1)
  }
}));

const SearchBar = () => {
  const classes = useStyles();
  return (
    <div className={classes.wrapper}>
      <input type="text" className={classes.searchBar} placeholder="Suche" />
    </div>
  );
};

export default SearchBar;
