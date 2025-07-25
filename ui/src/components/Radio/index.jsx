import { green, red } from '@material-ui/core/colors';
import MuiRadio from '@material-ui/core/Radio';
import { makeStyles } from '@material-ui/styles';
import { object, oneOf } from 'prop-types';
import React from 'react';

const useStyles = makeStyles({
  greenRoot: {
    '&$checked': {
      color: green[600],
    },
  },
  redRoot: {
    '&$checked': {
      color: red[600],
    },
  },
  checked: {},
});
const Radio = (props) => {
  const classes = useStyles();
  const { variant, classes: classesFromProps, ...rest } = props;

  return (
    <MuiRadio
      classes={{
        checked: classes.checked,
        root: classes[`${variant}Root`],
        ...classesFromProps,
      }}
      {...rest}
    />
  );
};

Radio.propTypes = {
  classes: object,
  variant: oneOf(['red', 'green', 'default']),
};

Radio.defaultProps = {
  classes: null,
  variant: 'default',
};

export default Radio;
