import './App.css';
import SearchBox from './Component/SearchBox';
import SimpleMap from './Component/SimpleMap';
function App() {
    let curr_location;
    function changeLocation(local) {
        curr_location = [local[0].formatted_address, local[0].geometry.viewport.Ma.hi, local[0].geometry.viewport.Ya.hi];
        console.log(local);
        console.log(local[0].formatted_address);
        console.log(local[0].geometry.viewport.Ma.hi);
        console.log(local[0].geometry.viewport.Ya.hi);
        sendLocal(curr_location);
    }

    function sendLocal(data) {
        fetch('IP_GOES_HERE', {
            method: 'POST', 
            mode: 'cors', 
            body: JSON.stringify(data) 

        })
    }

  return (
    <div>
        <SearchBox changeLoc={changeLocation} className="input" />
        <SimpleMap location={curr_location} />      
    </div>
  );
}

export default App;

