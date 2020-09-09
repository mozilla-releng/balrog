import React from 'react';
import { oneOf } from 'prop-types';
import { ThemeProvider } from '@material-ui/styles';
import { createMuiTheme } from '@material-ui/core/styles';
import MuiButton from '@material-ui/core/Button';
import { red } from '@material-ui/core/colors';

const dangerTheme = createMuiTheme({
  palette: {
    primary: red,
  },
});

// A Material UI Button augmented with a danger color
function Button({ color, ...rest }) {
  if (color === 'danger') {
    return (
      <ThemeProvider theme={dangerTheme}>
        <MuiButton color="primary" {...rest} />
      </ThemeProvider>
    );
  }

  return <MuiButton color={color} {...rest} />;
}

Button.propTypes = {
  color: oneOf(['default', 'inherit', 'primary', 'secondary', 'danger']),
};

Button.defaultProps = {
  color: 'default',
};

export default Button;
