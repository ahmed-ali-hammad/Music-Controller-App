import React, { Component } from "react";
import RoomJoinPage from "./RoomJoinPage";
import CreatRoomPage from "./CreatRoomPage";
import Room from "./Room";
import { Grid, Button, ButtonGroup, Typography } from "@material-ui/core";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    Redirect,
} from "react-router-dom";


export default class  HomePage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            roomCode: null,
        }
    }

    async componentDidMount(){
        fetch ("/api/room/user/in/")
        .then((response) => response.json())
        .then((data) => { this.setState({roomCode: data.code}) });
    }

    renderHomePage(){
        return (
            <Grid container spacing = {3}>
                <Grid item xs = {12} align = "center">
                    <Typography variant = "h3" compact = "h3">
                        House Party
                    </Typography>
                </Grid>
                <Grid item xs = {12} align = "center">
                    <ButtonGroup disableElevation variant = "contained" color = "primary">
                        <Button color = "primary" to = "/join" component = {Link} >
                            Join a Room
                        </Button>
                        <Button color = "secondary" to = "/create" component = {Link}>
                            Create A Room
                        </Button>
                    </ButtonGroup>
                </Grid>
            </Grid>
        )
    }

    render() {
        return (
            <Router>
                <Switch>
                    <Route 
                        exactpath="/"
                        render = {() =>{
                            return this.state.roomCode ? (
                                <Redirect to = {`/room/${this.state.roomCode}`} />
                            ) : (
                                this.renderHomePage()
                            );
                        }}
                    />
                    <Route path="/join" component={RoomJoinPage} />
                    <Route path="/create" component={CreatRoomPage} />
                    <Route path= "/room/:roomCode" component = {Room} />
                </Switch>
            </Router>
        );
    }
}
