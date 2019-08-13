import { createMuiTheme } from '@material-ui/core/styles';
import { red } from '@material-ui/core/colors';

const SPACING = {
  UNIT: 8,
  DOUBLE: 16,
  TRIPLE: 24,
  QUAD: 32,
};

export default createMuiTheme({
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
  },
});
