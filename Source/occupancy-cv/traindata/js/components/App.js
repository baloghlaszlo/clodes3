import React from 'react';
import {withRouter} from 'react-router';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import AppBar from 'material-ui/AppBar';
import Drawer from 'material-ui/Drawer';
import MenuItem from 'material-ui/MenuItem';
import Divider from 'material-ui/Divider';
import Subheader from 'material-ui/Subheader';

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {open: false};
    }

    _handleOpenDrawer() {
        this.setState({open: true});
    };

    _pushAndClose(href) {
        return () => {
            this.props.router.push(href);
            this.setState({open: false});
        };
    }

    render() {
        return (
            <MuiThemeProvider>
                <div>
                    <Drawer
                        docked={false}
                        open={this.state.open}
                        onRequestChange={(open) => this.setState({open})}
                    >
                        <Subheader>Label Manually</Subheader>
                        <MenuItem onTouchTap={this._pushAndClose('/label-rects')}>Label Rectangles</MenuItem>
                        <MenuItem onTouchTap={this._pushAndClose('/label-frames')}>Label Frames</MenuItem>
                        <Divider/>
                        <Subheader>Debug</Subheader>
                        <MenuItem onTouchTap={this._pushAndClose('/frames/new')}>Upload Frame</MenuItem>
                        <MenuItem onTouchTap={this._pushAndClose('/frames/last')}>Last Frame</MenuItem>
                        <MenuItem onTouchTap={this._pushAndClose('/stats')}>Statistics</MenuItem>
                    </Drawer>
                    <AppBar
                        title='Face Detector Training'
                        onLeftIconButtonTouchTap={this._handleOpenDrawer.bind(this)}
                    />
                    <div style={{height: 'calc(100vh - 64px)', overflow: 'hidden'}}>
                        {this.props.children}
                    </div>
                </div>
            </MuiThemeProvider>
        );
    }
}

export default withRouter(App);