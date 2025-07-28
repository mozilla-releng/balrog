import { amber, indigo, red } from '@material-ui/core/colors';
import { createTheme } from '@material-ui/core/styles';

const SPACING = {
  UNIT: 8,
  DOUBLE: 16,
  TRIPLE: 24,
  QUAD: 32,
};

export default createTheme({
  palette: {
    primary: {
      light: '#804cc5',
      main: '#4e1f94',
      dark: '#160065',
    },
    secondary: {
      light: '#678dff',
      main: '#0061f2',
      dark: '#0038be',
    },
    error: red,
    warning: {
      light: amber[300],
      main: amber[500],
      dark: amber[700],
      contrastText: 'rgba(0, 0, 0, 0.9)',
    },
    info: {
      light: indigo[300],
      main: indigo[500],
      dark: indigo[700],
      contrastText: 'rgba(255, 255, 255, 0.9)',
    },
  },
  typography: {
    useNextVariants: true,
  },
  mixins: {
    link: {
      textDecoration: 'none',
      color: 'unset',
    },
    fab: {
      position: 'fixed',
      bottom: SPACING.DOUBLE,
      right: SPACING.TRIPLE,
    },
    textEllipsis: {
      whiteSpace: 'nowrap',
      overflow: 'hidden',
      textOverflow: 'ellipsis',
    },
    redDot: {
      width: SPACING.UNIT,
      height: SPACING.UNIT,
      borderRadius: '50%',
      background: 'red',
      marginLeft: SPACING.UNIT,
    },
  },
  overrides: {
    MuiListItem: {
      dense: {
        paddingTop: SPACING.UNIT / 2,
        paddingBottom: SPACING.UNIT / 2,
      },
    },
    MuiList: {
      padding: {
        paddingTop: 0,
        paddingBottom: 0,
      },
    },
  },
});
