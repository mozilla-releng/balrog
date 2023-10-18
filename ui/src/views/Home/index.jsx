import React from 'react';
import { makeStyles } from '@material-ui/styles';
import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import LinkIcon from 'mdi-react/LinkIcon';
import Dashboard from '../../components/Dashboard';
import Link from '../../utils/Link';
import { RULES_COMMON_FILTERS } from '../../utils/constants';

const useStyles = makeStyles(theme => ({
  cardPaper: {
    background: 'rgba(255, 255, 255, 0.9)',
  },
  link: {
    ...theme.mixins.link,
  },
}));

function Home() {
  const classes = useStyles();

  return (
    <Dashboard title="Home">
      <Card className={classes.cardPaper}>
        <CardContent>
          <Typography gutterBottom component="h2" variant="h5">
            Rules Common Filters
          </Typography>
          <List>
            {RULES_COMMON_FILTERS.map(({ link, label }) => (
              <Link className={classes.link} key={label} to={link}>
                <ListItem button>
                  <ListItemText primary={label} />
                  <LinkIcon />
                </ListItem>
              </Link>
            ))}
          </List>
        </CardContent>
      </Card>
    </Dashboard>
  );
}

export default Home;
