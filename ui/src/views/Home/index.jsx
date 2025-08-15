import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Typography from '@mui/material/Typography';
import LinkIcon from 'mdi-react/LinkIcon';
import React from 'react';
import { makeStyles } from 'tss-react/mui';
import Dashboard from '../../components/Dashboard';
import balrogSrc from '../../images/balrog.svg';
import { RULES_COMMON_FILTERS } from '../../utils/constants';
import Link from '../../utils/Link';

const useStyles = makeStyles()((theme) => ({
  balrogImage: {
    width: 800,
    height: 800,
    position: 'fixed',
    zIndex: -1,
    opacity: 0.5,
    transform: 'scaleX(-1)',
  },
  cardPaper: {
    background: 'rgba(255, 255, 255, 0.9)',
  },
  link: {
    ...theme.mixins.link,
  },
}));

function Home() {
  const { classes } = useStyles();

  return (
    <Dashboard title="Home">
      <img alt="Balrog logo" className={classes.balrogImage} src={balrogSrc} />
      <Card className={classes.cardPaper}>
        <CardContent>
          <Typography gutterBottom component="h2" variant="h5">
            Rules Common Filters
          </Typography>
          <List>
            {RULES_COMMON_FILTERS.map(({ link, label }) => (
              <ListItem key={label} disablePadding>
                <ListItemButton
                  component={Link}
                  className={classes.link}
                  to={link}
                >
                  <ListItemText primary={label} />
                  <LinkIcon />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </CardContent>
      </Card>
    </Dashboard>
  );
}

export default Home;
