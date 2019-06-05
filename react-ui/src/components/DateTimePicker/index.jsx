import React, { useState } from 'react';
import { func } from 'prop-types';
import { DateFormatInput, TimeFormatInput } from 'material-ui-next-pickers';
import Grid from '@material-ui/core/Grid';
import { makeStyles } from '@material-ui/styles';
import { getHours, getMinutes, addMinutes, addHours } from 'date-fns';

const useStyles = makeStyles(theme => ({
  container: {
    display: 'flex',
  },
  datePicker: {
    marginRight: theme.spacing(1),
  },
}));

export default function DateTimePicker(props) {
  const { onDateTimeChange } = props;
  const classes = useStyles();
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');

  function handleDateTimeChange() {
    const hours = getHours(time) || 0;
    const minutes = getMinutes(time) || 0;
    const result = addHours(addMinutes(date, minutes), hours);

    onDateTimeChange(result);
  }

  function onDateChange(date) {
    setDate(date);
    handleDateTimeChange();
  }

  function handleTimeChange(time) {
    setTime(time);
    handleDateTimeChange();
  }

  return (
    <Grid container spacing={8}>
      <Grid item xs={12} sm={12} md={6}>
        <DateFormatInput
          className={classes.datePicker}
          name="date-input"
          value={date}
          onChange={onDateChange}
          fullWidth
        />
      </Grid>
      <Grid item xs={12} sm={12} md={6}>
        <TimeFormatInput
          name="time-input"
          value={time}
          onChange={handleTimeChange}
          fullWidth
        />
      </Grid>
    </Grid>
  );
}

DateTimePicker.propTypes = {
  /**
   * A function to execute when the date or time changes.
   * Will receive a single argument which will include the date and time.
   */
  onDateTimeChange: func.isRequired,
};
