import { renderTimeViewClock } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { DateTimePicker as MUIDateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { func, instanceOf } from 'prop-types';
import React, { useEffect, useState } from 'react';

export default function DateTimePicker({
  value,
  onDateTimeChange,
  disablePast,
  fullWidth,
  inputVariant,
  error,
  helperText,
  slotProps,
  ...props
}) {
  // We don't want to call onDateTimeChange before the datetime is fully selected so we have to use an intermediate
  // state here...
  const [internalValue, setInternalValue] = useState(value);

  useEffect(() => {
    setInternalValue(value);
  }, [value]);

  // disablePast on the input is too eager and will mark the input as invalid when the page loads
  const minDateTime = disablePast
    ? (() => {
        const now = new Date();
        return new Date(
          now.getFullYear(),
          now.getMonth(),
          now.getDate(),
          now.getHours(),
          now.getMinutes(),
          0,
          0,
        );
      })()
    : undefined;

  const handleChange = (newValue) => {
    setInternalValue(newValue);
    if (newValue === null) {
      onDateTimeChange(newValue);
    }
  };

  const mergedSlotProps = {
    textField: {
      margin: 'normal',
      fullWidth,
      variant: inputVariant || 'outlined',
      error,
      helperText,
      ...slotProps?.textField,
    },
    actionBar: {
      actions: ['today', 'clear', 'accept'],
      ...slotProps?.actionBar,
    },
    ...slotProps,
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <MUIDateTimePicker
        value={internalValue}
        onChange={handleChange}
        onAccept={onDateTimeChange}
        minDateTime={minDateTime}
        format="yyyy/MM/dd hh:mm a"
        viewRenderers={{
          hours: renderTimeViewClock,
          minutes: renderTimeViewClock,
        }}
        slotProps={mergedSlotProps}
        {...props}
      />
    </LocalizationProvider>
  );
}

DateTimePicker.propTypes = {
  /**
   * A function to execute when the date or time changes.
   * Will receive a single argument which will include the date and time.
   */
  onDateTimeChange: func.isRequired,
  /**
   * The value of the picker. Can be a Date object or null.
   */
  value: instanceOf(Date),
};
