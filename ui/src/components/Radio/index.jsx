import { green, red } from '@mui/material/colors';
import MuiRadio from '@mui/material/Radio';
import React from 'react';
import { makeStyles } from 'tss-react/mui';

const useStyles = makeStyles()({
  greenRoot: {
    '&.Mui-checked': {
      color: green[600],
    },
  },
  redRoot: {
    '&.Mui-checked': {
      color: red[600],
    },
  },
});
const Radio = (props) => {
  const { classes } = useStyles();
  const { variant, classes: classesFromProps, ...rest } = props;

  return (
    <MuiRadio
      classes={{
        root: classes[`${variant}Root`],
        ...classesFromProps,
      }}
      {...rest}
    />
  );
};

Radio.defaultProps = {
  classes: null,
  variant: 'default',
};

export default Radio;
