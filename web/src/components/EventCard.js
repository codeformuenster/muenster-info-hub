import React from "react";
import * as moment from "moment";
import "moment/locale/de";
import Typography from "@material-ui/core/Typography";
import { Link } from '@material-ui/core';
import RoomIcon from "@material-ui/icons/Room";
import ClockIcon from "@material-ui/icons/WatchLater";
import LabelIcon from "@material-ui/icons/Label";
import DirectionsIcon from '@material-ui/icons/Directions';
import InfoIcon from '@material-ui/icons/Info';


import Card from "@material-ui/core/Card";
import CardActions from "@material-ui/core/CardActions";
import CardActionArea from '@material-ui/core/CardActionArea';
import CardContent from "@material-ui/core/CardContent";
import CardMedia from "@material-ui/core/CardMedia";
import Button from "@material-ui/core/Button";
import IconButton from '@material-ui/core/IconButton';


import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";

import ExpansionPanel from "@material-ui/core/ExpansionPanel";
import ExpansionPanelSummary from "@material-ui/core/ExpansionPanelSummary";
import ExpansionPanelDetails from "@material-ui/core/ExpansionPanelDetails";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";

import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(theme => ({
  card: {
    margin: theme.spacing(2)
  },
  tag: {
    fontVariant: "small-caps"
  },
  title: {
    letterSpacing: 1,
    fontWeight: theme.typography.fontWeightLight
  },
  media: {
    height: 140
  },
  cardContent: {
    padding: theme.spacing(1, 2)
  },
  actions: {
    justifyContent: "center"
  },
  cardContentDetails: {
    height: 0,
    transition: "height 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms"
  },
  eventStats: {
    minWidth: 35,
  },
  eventDetails: {
    color: theme.palette.grey[800],
    backgroundColor: theme.palette.grey[300],
    '& .MuiExpansionPanelSummary-content': {
      display: 'none',
    },
    '& .MuiIconButton-edgeEnd': {
      marginRight: 'unset'
    },
    '& .MuiExpansionPanelSummary-expandIcon': {
      backgroundColor: theme.palette.grey[400],
      padding: 6,
      margin: 6
    }
  },
  detailsExpanded: {
    height: "auto",
    transition: "height 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms"
  },
  listItem: {
    padding: 0
  },
  clockIcon: {
    color: '#d70f64'
  },
  roomIcon: {
    color: '#00a396'
  },
  labelIcon: {
    color: 'rgba(0, 0, 0, 0.54)'
  },
  infoIcon: {
    color: '#4666FF'
  },
  directionsIcon: {
    marginLeft: theme.spacing(1),
  },
  directionsButton: {
    width: '100%'
  },
}));

function getMapsLink(place, address, lat, lon) {
  if (lat && lon) {
    return `http://maps.google.com/?ll=${lat},${lon}`
  } else if (place && address) {
   return `http://maps.google.com/?q=${place}+${address}`
  } else if (address) {
   return `http://maps.google.com/?q=${address}`
  } else {
   return `http://maps.google.com/?q=${place}`
  }
}

function EventCard({ source, title, link, time, place, address, tags, image, description, lat, lon }) {
  const classes = useStyles();

  const [isExpanded, setExpanded] = React.useState(false);

  return (
    <Card className={classes.card} raised={true}>
      <CardActionArea>
        <Link href={link} target="_blank" rel="noopener">
          <CardMedia className={classes.media} image={image} title={title} />
          <CardContent className={classes.cardContent}>
            <Typography
              gutterBottom
              variant="h5"
              component="h2"
              className={classes.title}
            >
              {title}
            </Typography>
            <Typography variant="body1" color="textSecondary" component="p">
              <List disablePadding={true}>
                <ListItem dense={true} className={classes.listItem}>
                  <ListItemIcon className={classes.eventStats}>
                    <ClockIcon className={classes.clockIcon}/>
                  </ListItemIcon>
                  <ListItemText primary={moment(time).fromNow()} />
                </ListItem>
                <ListItem dense={true} className={classes.listItem}>
                  <ListItemIcon className={classes.eventStats}>
                    <RoomIcon className={classes.roomIcon}/>
                  </ListItemIcon>
                  <ListItemText primary={place} />
                </ListItem>
                <ListItem dense={true} className={classes.listItem}>
                  <ListItemIcon className={classes.eventStats}>
                    <LabelIcon className={classes.labelIcon}/>
                  </ListItemIcon>
                  <ListItemText primary={tags.join(", ")} />
                </ListItem>
                <ListItem dense={true} className={classes.listItem}>
                  <ListItemIcon className={classes.eventStats}>
                    <InfoIcon className={classes.infoIcon}/>
                  </ListItemIcon>
                  <ListItemText primary={source} />
                </ListItem>
              </List>
            </Typography>
          </CardContent>
        </Link>
      </CardActionArea>
      <ExpansionPanel className={classes.eventDetails}>
        <ExpansionPanelSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
        >
        </ExpansionPanelSummary>
        <ExpansionPanelDetails>
          <Typography>
            {description}
          </Typography>
        </ExpansionPanelDetails>
        <Button href={getMapsLink(place, address, lat, lon)} target="_blank" rel="noopener" variant="contained" color="secondary" className={classes.directionsButton}>
            Bring mich hin!
            <DirectionsIcon className={classes.directionsIcon} />
        </Button>

      </ExpansionPanel>
    </Card>
  );
}

export default EventCard;
