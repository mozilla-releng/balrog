import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { makeStyles } from '@material-ui/styles';
import { arrayOf, bool, func, object, string } from 'prop-types';
import React from 'react';

const useStyles = makeStyles((theme) => ({
  chip: {
    fontSize: '0.60rem',
    height: 'auto',
    marginRight: theme.spacing(0.5),
    '& .MuiChip-label': {
      fontSize: '0.60rem',
      padding: '0.2rem',
      marginLeft: '0.3rem',
    },
    '& .MuiChip-deleteIcon': {
      width: '24px',
      height: '12px',
      marginLeft: '0.2rem',
    },
  },
}));

/**
 * A wrapper component around Material UI Autocomplete to render a TextField
 * with auto complete capabilities.
 */
function AutoCompleteText({
  onValueChange,
  value,
  label,
  required,
  disabled,
  getSuggestions,
  inputProps,
  selectedItems,
  onSelectedItemsChange,
  multi,
  ...props
}) {
  const classes = useStyles();
  const handleSingleChange = (_event, newValue) => {
    onValueChange(newValue || '');
  };

  const handleMultiChange = (_event, newValues) => {
    if (onSelectedItemsChange) {
      onSelectedItemsChange(newValues);
    }
  };

  const handleInputChange = (_event, newInputValue) => {
    onValueChange(newInputValue);
  };

  const options = getSuggestions ? getSuggestions(value) : [];

  if (multi) {
    return (
      <Autocomplete
        {...props}
        multiple
        options={options}
        value={selectedItems}
        onChange={handleMultiChange}
        inputValue={value}
        onInputChange={handleInputChange}
        disabled={disabled}
        ChipProps={{
          className: classes.chip,
          size: 'small',
        }}
        renderInput={(params) => (
          <TextField
            {...params}
            {...inputProps}
            label={label}
            required={required}
            fullWidth
          />
        )}
      />
    );
  }

  return (
    <Autocomplete
      {...props}
      options={options}
      value={value}
      onChange={handleSingleChange}
      inputValue={value}
      onInputChange={handleInputChange}
      disabled={disabled}
      freeSolo
      renderInput={(params) => (
        <TextField
          {...params}
          {...inputProps}
          label={label}
          required={required}
          fullWidth
        />
      )}
    />
  );
}

AutoCompleteText.propTypes = {
  // Callback triggered when the value of the text field is changed.
  onValueChange: func.isRequired,
  value: string.isRequired,
  getSuggestions: func,
  inputProps: object,
  label: string,
  required: bool,
  disabled: bool,
  // Selected items for when `multi` is set to `true`.
  selectedItems: arrayOf(string),
  // Callback triggered when the list of chips change.
  onSelectedItemsChange: func,
  // If true, the text field will allow multi text selection
  multi: bool,
};

AutoCompleteText.defaultProps = {
  getSuggestions: null,
  selectedItems: [],
  onSelectedItemsChange: null,
  inputProps: {},
  label: '',
  required: false,
  disabled: false,
  multi: false,
};

export default AutoCompleteText;
