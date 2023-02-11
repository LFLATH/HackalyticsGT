import React from 'react';
import ReactDOM from 'react-dom';
import { PropTypes } from 'prop-types';
const google = window.google;

export default class SearchBox extends React.Component {
  static propTypes = {
    placeholder: PropTypes.string,
    onPlacesChanged: PropTypes.func
  }
  _handleKeyDown = (e) => {
    if (e.key === 'Enter') {
        this.props.changeLoc(this.searchBox.getPlaces());
        
    }
  }
  render() {
    return <input ref="input" {...this.props} onKeyDown={this._handleKeyDown} type="text"/>;
  }
  onPlacesChanged = () => {
    if (this.props.onPlacesChanged) {
      this.props.onPlacesChanged(this.searchBox.getPlaces());
    }
  }
  componentDidMount() {
    var input = ReactDOM.findDOMNode(this.refs.input);
    this.searchBox = new google.maps.places.SearchBox(input);
    this.searchBox.addListener('places_changed', this.onPlacesChanged);
  }
  componentWillUnmount() {
    // https://developers.google.com/maps/documentation/javascript/events#removing
    google.maps.event.clearInstanceListeners(this.searchBox);
  }
}