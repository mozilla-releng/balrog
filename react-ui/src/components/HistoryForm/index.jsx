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
import ListSubheader from '@material-ui/core/ListSubheader';
import Button from '@material-ui/core/Button';
import MenuItem from '@material-ui/core/MenuItem';
import MagnifyIcon from 'mdi-react/MagnifyIcon';
import DateTimePicker from '../DateTimePicker';

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

export default function HistoryForm(props) {
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
            <ListSubheader>From</ListSubheader>
            <ListItem>
              <DateTimePicker onDateTimeChange={handleDateTimeStartChange} />
            </ListItem>
            <ListSubheader>To</ListSubheader>
            <ListItem>
              <DateTimePicker onDateTimeChange={handleDateTimeEndChange} />
            </ListItem>
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

HistoryForm.propTypes = {
  onSubmit: func.isRequired,
};
