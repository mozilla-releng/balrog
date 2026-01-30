import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import React from 'react';
import { makeStyles } from 'tss-react/mui';

const useStyles = makeStyles()((theme) => ({
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
  const { classes } = useStyles();
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
