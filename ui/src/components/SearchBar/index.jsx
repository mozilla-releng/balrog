import InputBase from '@mui/material/InputBase';
import Paper from '@mui/material/Paper';
import SearchIcon from 'mdi-react/SearchIcon';
import React from 'react';
import { makeStyles } from 'tss-react/mui';

const useStyles = makeStyles()((theme) => ({
  root: {
    padding: theme.spacing(1, 2),
    display: 'flex',
    alignItems: 'center',
    marginBottom: theme.spacing(2),
  },
  input: {
    flex: 1,
  },
  searchIcon: {
    marginRight: theme.spacing(1),
  },
}));

function SearchBar(props) {
  const { ...rest } = props;
  const { classes } = useStyles();

  return (
    <Paper className={classes.root}>
      <InputBase
        className={classes.input}
        placeholder="Search..."
        endAdornment={<SearchIcon />}
        inputProps={{ 'aria-label': 'Search' }}
        {...rest}
      />
    </Paper>
  );
}

export default SearchBar;
