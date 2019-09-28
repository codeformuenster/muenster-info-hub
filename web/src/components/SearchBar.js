import React from "react";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(theme => ({
  searchBar: {
    // margin: theme.spacing(0),
    width: '100%',
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
      <input type="text" className={classes.searchBar} />
    </div>
  );
};

export default SearchBar;
