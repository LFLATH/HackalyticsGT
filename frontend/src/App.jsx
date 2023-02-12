import './App.css';
import axios from 'axios';
import SearchBox from './Component/SearchBox';
import SimpleMap from './Component/SimpleMap';
import React, { useState } from 'react';
import Charts from "./Component/Charts"
import Title from './Component/Title';

function App() {
 

    const [center, setCenter] = useState([33.7775, -84.3961]);
    const [data, setData] = useState({});
    function changeLocation(local) {
        let curr_location = {
          long: local[0].geometry.viewport.Ya.hi,
          lat: local[0].geometry.viewport.Ma.hi,
          address: local[0].formatted_address,  
        };
        console.log(process.env.REACT_APP_API_URL);
        axios.post(process.env.REACT_APP_API_URL, curr_location)
        .then(function (response) {
            setData(response.data);
          })
          .catch(function (error) {
            console.log(error);
          });
        setCenter([local[0].geometry.viewport.Ya.hi, local[0].geometry.viewport.Ma.hi]);
    }
  

  return (
    <div>
        <Title/>
        <SearchBox changeLoc={changeLocation} className="input" />
        <SimpleMap location={center} />  
        <div className="charts">
            <Charts data={data} />
        </div> 
    </div>
  );
}

export default App;

