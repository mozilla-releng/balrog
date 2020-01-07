import React from 'react';
import { instanceOf, func } from 'prop-types';
import DateFnsUtils from '@date-io/date-fns';
import {
  MuiPickersUtilsProvider,
  KeyboardDateTimePicker,
} from '@material-ui/pickers';

export default function DateTimePicker({ value, onDateTimeChange, ...props }) {
  function handleDateChange(date) {
    onDateTimeChange(date);
  }

  return (
    <MuiPickersUtilsProvider utils={DateFnsUtils}>
      <KeyboardDateTimePicker
        margin="normal"
        showTodayButton
        value={value}
        onChange={handleDateChange}
        autoOk
        minDateMessage="Date should not be in the past"
        KeyboardButtonProps={{
          'aria-label': 'change date',
        }}
        format="yyyy/MM/dd hh:mm a"
        {...props}
      />
    </MuiPickersUtilsProvider>
  );
}

DateTimePicker.propTypes = {
  /**
   * A function to execute when the date or time changes.
   * Will receive a single argument which will include the date and time.
   */
  onDateTimeChange: func.isRequired,
  /**
   * The value of the picker.
   */
  value: instanceOf(Date).isRequired,
};
