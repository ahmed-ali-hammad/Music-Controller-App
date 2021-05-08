import React, { Component } from "react";
import { Grid, Button, Typography } from "@material-ui/core"
import { Link } from "react-router-dom"

export default class Room extends Component{
    constructor(props) {
        super(props);
        this.state = {
            votesToSkip:2,
            guestCanPause: false,
            isHost: false,
        };
        this.roomCode = this.props.match.params.roomCode;
        this.getRoomDetail ();
        this.leaveButtonPressed = this.leaveButtonPressed.bind(this);
    };

    getRoomDetail(){  
        fetch ("/api/room/detail/" + this.roomCode + "/" )
        .then((response) => response.json())
        .then((data) => {
            this.setState({
                votesToSkip: data.votes_to_skip,
                guestCanPause: data.guest_can_pause,
                isHost: data.is_host,
            });
        });
    };

    leaveButtonPressed() {
        const requestOptions = {
            method: "POST", 
            headers: {"content-type": "application/json"},
        };
        fetch ("/api/room/leave/", requestOptions)

    }
    render(){
        return (
            <Grid container spacing = {1}>
                <Grid item xs = {12} align = "center">
                    <Typography variant = "h4" Component = "h4">
                        code: {this.roomCode}
                    </Typography>
                </Grid>
                <Grid item xs = {12} align = "center">
                    <Typography variant = "h6" Component = "h6">
                        votes: {this.state.votesToSkip}
                    </Typography>
                </Grid>
                <Grid item xs = {12} align = "center">
                    <Typography variant = "h6" Component = "h6">
                        Guest can Pause: {this.state.guestCanPause.toString()}
                    </Typography>
                </Grid>
                <Grid item xs = {12} align = "center">
                    <Typography variant = "h6" Component = "h6">
                        Host: {this.state.isHost.toString()}
                    </Typography>
                </Grid>
                <Grid item xs = {12} align = "center">
                    <Button variant= "contained" color = "secondary" to='/' component = {Link}>
                        Leave Room
                    </Button>

                </Grid>
            </Grid>
        ); 
    }
}