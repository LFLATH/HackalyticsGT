import GoogleMapReact from 'google-map-react';
import React, { useEffect } from 'react';
import MarkerIcon from './MarkerIcon';
const AnyReactComponent = ({ text }) => <div><MarkerIcon/></div>;

export default function SimpleMap(props){
    const defaultProps = {
    zoom: 17
  };
  useEffect(()=>{
},[props.location]);
  return (
    <div style={{ height: '50vh', width: '100%' }}>
      <GoogleMapReact
        bootstrapURLKeys={{ key: process.env.REACT_APP_GOOGLE_API }}
        defaultZoom={defaultProps.zoom}
        center={(props.location ? props.location:[33.7775, -84.3961])}
      >
    <AnyReactComponent
          lat={props.location[0]}
          lng={props.location[1]}
        />
      </GoogleMapReact>
    </div>
  );
}

