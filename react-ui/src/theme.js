import { createMuiTheme } from '@material-ui/core/styles';

const SPACING = {
  UNIT: 8,
  DOUBLE: 16,
  TRIPLE: 24,
  QUAD: 32,
};

export default createMuiTheme({
  typography: {
    useNextVariants: true,
  },
  mixins: {
    link: {
      textDecoration: 'none',
      color: 'unset',
      height: '100%',
      width: '100%',
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
