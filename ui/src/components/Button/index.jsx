import MuiButton from '@mui/material/Button';
import { red } from '@mui/material/colors';
import {
  createTheme,
  StyledEngineProvider,
  ThemeProvider,
} from '@mui/material/styles';
import { oneOf } from 'prop-types';
import React from 'react';

const dangerTheme = createTheme({
  palette: {
    primary: red,
  },
});

// A Material UI Button augmented with a danger color
function Button({ color, ...rest }) {
  if (color === 'danger') {
    return (
      <StyledEngineProvider injectFirst>
        <ThemeProvider theme={dangerTheme}>
          <MuiButton color="primary" {...rest} />
        </ThemeProvider>
      </StyledEngineProvider>
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
