import React, { useState } from 'react';
import { func } from 'prop-types';
import { makeStyles } from '@material-ui/styles';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import TextField from '@material-ui/core/TextField';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import MenuItem from '@material-ui/core/MenuItem';
import Grid from '@material-ui/core/Grid';
import MagnifyIcon from 'mdi-react/MagnifyIcon';
import DateTimePicker from '../DateTimePicker';
import Button from '../Button';

const useStyles = makeStyles(theme => ({
  actions: {
    display: 'flex',
    flexFlow: 'row-reverse',
    marginTop: theme.spacing(2),
    '& button:not(:first-child)': {
      marginRight: theme.spacing(2),
    },
  },
  form: {
    width: '100%',
  },
  searchIcon: {
    marginRight: theme.spacing(1),
  },
}));

export default function HistoryFilter(props) {
  const classes = useStyles();
  const { onSubmit } = props;
  const [object, setObject] = useState('');
  const [changedBy, setChangedBy] = useState('');
  const [dateTimeStart, setDateTimeStart] = useState('');
  const [dateTimeEnd, setDateTimeEnd] = useState('');
  const objectOptions = [
    'rules',
    'releases',
    'permissions',
    'required_signoffs/product',
    'required_signoffs/permissions',
  ];

  function handleFormSubmit(e) {
    e.preventDefault();

    onSubmit({
      object,
      changedBy,
      dateTimeStart,
      dateTimeEnd,
    });
  }

  function handleObjectChange({ target }) {
    setObject(target.value);
  }

  function handleChangedByChange({ target }) {
    setChangedBy(target.value);
  }

  function handleDateTimeStartChange(date) {
    setDateTimeStart(date);
  }

  function handleDateTimeEndChange(date) {
    setDateTimeEnd(date);
  }

  return (
    <ExpansionPanel defaultExpanded>
      <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
        <Typography variant="subtitle1">Search Filter</Typography>
      </ExpansionPanelSummary>
      <ExpansionPanelDetails>
        <form className={classes.form} onSubmit={handleFormSubmit}>
          <List>
            <ListItem>
              <TextField
                required
                select
                fullWidth
                label="Objects"
                value={object}
                onChange={handleObjectChange}>
                {objectOptions.map(option => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </TextField>
            </ListItem>
            <ListItem>
              <TextField
                fullWidth
                label="Changed By"
                value={changedBy}
                onChange={handleChangedByChange}>
                {changedBy}
              </TextField>
            </ListItem>
            <Grid container>
              <Grid item xs={12} sm={6}>
                <ListItem>
                  <DateTimePicker
                    fullWidth
                    label="From"
                    onDateTimeChange={handleDateTimeStartChange}
                    value={new Date()}
                  />
                </ListItem>
              </Grid>
              <Grid item xs={12} sm={6}>
                <ListItem>
                  <DateTimePicker
                    fullWidth
                    label="To"
                    onDateTimeChange={handleDateTimeEndChange}
                    value={new Date()}
                  />
                </ListItem>
              </Grid>
            </Grid>
          </List>
          <div className={classes.actions}>
            <Button color="primary" type="submit" variant="contained">
              <MagnifyIcon className={classes.searchIcon} />
              Filter
            </Button>
            <Button>Clear</Button>
          </div>
        </form>
      </ExpansionPanelDetails>
    </ExpansionPanel>
  );
}

HistoryFilter.propTypes = {
  onSubmit: func.isRequired,
};
