import React, { Component } from "react";
import { Grid, Button, Typography } from "@material-ui/core"


export default class Room extends Component{
    constructor(props) {
        super(props);
        this.state = {
            votesToSkip:2,
            guestCanPause: false,
            isHost: false,
            showSettings: false,
        };
        this.roomCode = this.props.match.params.roomCode;
        this.getRoomDetail ();
        this.leaveButtonPressed = this.leaveButtonPressed.bind(this);
        this.updateShowSettings = this.updateShowSettings.bind(this);
    };

    getRoomDetail(){  
        fetch ("/api/room/detail/" + this.roomCode + "/" )
        .then((response) => {
            if (!response.ok){
                this.props.leaveRoomCallBack();
                this.props.history.push('/')
            }
            return response.json()})
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
        .then((_response) =>{
            this.props.leaveRoomCallBack();
            this.props.history.push("/");
        }
        )}

    updateShowSettings(value) {
        this.setState({
            showSettings: value,
        });
    }

    renderSettingsButton() {
        return (
            <Grid item xs = {12} align = "center">
                <Button
                    variant = "contained"
                    color = "primary"
                    onClick = {() => this.updateShowSettings(true)}
                    >
                    Settings
                </Button>
            </Grid>
        )
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
                {this.state.isHost ? this.renderSettingsButton() : null}
                <Grid item xs = {12} align = "center">
                    <Button variant= "contained" color = "secondary" onClick = {this.leaveButtonPressed}>
                        Leave Room
                    </Button>

                </Grid>
            </Grid>
        ); 
    }
}