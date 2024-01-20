import { createTheme } from '@material-ui/core/styles';
import '../node_modules/@mozilla-protocol/core/protocol/css/protocol-components.css';

const SPACING = {
  UNIT: 8,
  DOUBLE: 16,
  TRIPLE: 24,
  QUAD: 32,
};

export default createTheme({
  palette: {
    primary: {
      main: '#000',
    },
    secondary: {
      main: '#c50042',
    },
    success: {
      main: '#3fe1b0',
      dark: '#008787',
    },
  },
  typography: {
    fontDisplay: 'swap',
    fontFamily: "'Zilla Slab', 'Inter', sans-serif",
    fontStyle: 'normal',
    fontWeight: 'normal',
    body1: {
      fontFamily: "'Inter', sans-serif",
    },
    body2: {
      fontFamily: "'Inter', sans-serif",
    },
    caption: {
      fontFamily: "'Inter', sans-serif",
    },
    button: {
      fontFamily: "'Inter', sans-serif",
    },
    overline: {
      fontFamily: "'Inter', sans-serif",
    },
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
