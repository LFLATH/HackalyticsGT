import './App.css';
import axios from 'axios';
import SearchBox from './Component/SearchBox';
import SimpleMap from './Component/SimpleMap';
import React, { useState } from 'react';
import Charts from "./Component/Charts"
import Title from './Component/Title';
import BuildingInfo from './Component/BuildingInfo'

function App() {


  const [center, setCenter] = useState([33.7775, -84.3961]);
  const [data, setData] = useState({});
  const [buildingData, setBuildingData] = useState(undefined);
  const [foundBuildingData, setFoundBuildingData] = useState(false);
  const [loading, setLoading] = useState(false);
  function changeLocation(local) {
    let curr_location = {
      long: local[0].geometry.viewport.Ya.hi,
      lat: local[0].geometry.viewport.Ma.hi,
      address: local[0].formatted_address,
    };
    setLoading(true);
    axios.post(process.env.REACT_APP_API_URL, curr_location)
      .then(function (response) {
        setData(response.data.predictions);
        setBuildingData(response.data.buildingData);
        setFoundBuildingData(response.data.foundBuildingData);
        setLoading(false);
      })
      .catch(function (error) {
        alert(error);
        setLoading(false);
      });
    setCenter([local[0].geometry.viewport.Ya.hi, local[0].geometry.viewport.Ma.hi]);
  }


  return (
    <div>
      <Title />
      <SearchBox changeLoc={changeLocation} className="input" />
      <div class="flex-container">
        <div class="flex-child">
          <SimpleMap location={center} />
        </div>
        <BuildingInfo data={buildingData} foundBuildingData={foundBuildingData} buildingData={buildingData} loading={loading}/>
      </div>

      <div className="charts">
        <Charts data={data} />
      </div>
    </div>
  );
}

export default App;

