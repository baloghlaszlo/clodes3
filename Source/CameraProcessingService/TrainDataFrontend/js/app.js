import React from 'react';
import ReactDOM from 'react-dom';
import {applyMiddleware, createStore, combineReducers} from 'redux';
import {Provider} from 'react-redux';
import {IndexRoute, Router, Route, browserHistory} from 'react-router';
import {syncHistoryWithStore, routerReducer} from 'react-router-redux';
import createSagaMiddleware from 'redux-saga';

import reducers from './reducers';
import App from './components/App';
import Home from './components/Home';
import LabelImagePage from './components/LabelImagePage';
import trainDataFrontendSaga from './sagas';
import {rectLabelerOpened, frameLabelerOpened, labelerClosed} from './actions';

const sagaMiddleware = createSagaMiddleware();
const store = createStore(
    combineReducers({
        ...reducers,
        routing: routerReducer
    }),
    applyMiddleware(sagaMiddleware)
);
sagaMiddleware.run(trainDataFrontendSaga);

const history = syncHistoryWithStore(browserHistory, store);

import injectTapEventPlugin from 'react-tap-event-plugin';
injectTapEventPlugin();
ReactDOM.render(
    <Provider store={store}>
        <Router history={history}>
            <Route path='/' component={App}>
                <IndexRoute component={Home}/>
                <Route
                    path='label-rects'
                    component={LabelImagePage}
                    onEnter={() => store.dispatch(rectLabelerOpened())}
                    onLeave={() => store.dispatch(labelerClosed())}
                />
                <Route
                    path='label-frames'
                    component={LabelImagePage}
                    onEnter={() => store.dispatch(frameLabelerOpened())}
                    onLeave={() => store.dispatch(labelerClosed())}
                />
            </Route>
        </Router>
    </Provider>,
    document.getElementById('content')
);