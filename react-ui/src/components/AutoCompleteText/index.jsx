import React from 'react';
import { string, bool, object, func } from 'prop-types';
import classNames from 'classnames';
import Downshift from 'downshift';
import { makeStyles } from '@material-ui/styles';
import TextField from '@material-ui/core/TextField';
import MenuItem from '@material-ui/core/MenuItem';
import Paper from '@material-ui/core/Paper';

const useStyles = makeStyles(theme => ({
  paper: {
    position: 'absolute',
    zIndex: 1,
    marginTop: theme.spacing(1),
    left: 0,
    right: 0,
  },
  paperWrapper: {
    position: 'relative',
  },
  selectedText: {
    fontWeight: theme.typography.fontWeightMedium,
  },
}));

/**
 * A wrapper component around downshift-js to render a material-ui TextField
 * with auto complete capabilities.
 */
function AutoCompleteText({
  label,
  required,
  getSuggestions,
  inputProps,
  ...props
}) {
  const classes = useStyles();

  function renderSuggestion({
    suggestion,
    index,
    itemProps,
    highlightedIndex,
    selectedItem,
  }) {
    const isHighlighted = highlightedIndex === index;
    const isSelected = (selectedItem || '').indexOf(suggestion) > -1;

    return (
      <MenuItem
        {...itemProps}
        key={suggestion}
        selected={isHighlighted}
        component="div"
        className={classNames({ [classes.selectedText]: isSelected })}>
        {suggestion}
      </MenuItem>
    );
  }

  return (
    <Downshift {...props}>
      {({
        getInputProps,
        getItemProps,
        getMenuProps,
        highlightedIndex,
        inputValue,
        isOpen,
        selectedItem,
      }) => (
        <div>
          <TextField
            label={label}
            required={required}
            fullWidth
            InputProps={getInputProps(inputProps)}
          />
          {getSuggestions && (
            <div className={classes.paperWrapper} {...getMenuProps()}>
              {Boolean(isOpen) && (
                <Paper className={classes.paper} square>
                  {getSuggestions(inputValue).map((suggestion, index) =>
                    renderSuggestion({
                      suggestion,
                      index,
                      itemProps: getItemProps({ item: suggestion }),
                      highlightedIndex,
                      selectedItem,
                    })
                  )}
                </Paper>
              )}
            </div>
          )}
        </div>
      )}
    </Downshift>
  );
}

AutoCompleteText.propTypes = {
  getSuggestions: func,
  inputProps: object,
  label: string,
  required: bool,
};

AutoCompleteText.defaultProps = {
  getSuggestions: null,
  inputProps: {},
  label: '',
  required: false,
};

export default AutoCompleteText;
