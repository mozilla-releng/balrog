import DateFnsUtils from '@date-io/date-fns';
import {
  KeyboardDateTimePicker,
  MuiPickersUtilsProvider,
} from '@material-ui/pickers';
import { func, instanceOf } from 'prop-types';
import React from 'react';

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
