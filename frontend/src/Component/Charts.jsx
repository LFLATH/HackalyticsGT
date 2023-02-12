import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import {React, PureComponent} from 'react';




  export default class Example extends PureComponent {
    render() {
        let timestamp = [];
        let electricity = [];
        let hotwater = [];
        let steam = [];
        let chilledwater = [];
        timestamp = Object.values((this.props.data.timestamp) ? this.props.data.timestamp : {});
        electricity = Object.values((this.props.data.electricity) ? this.props.data.electricity : {});
        hotwater = Object.values((this.props.data.hotwater) ? this.props.data.hotwater : {});
        steam = Object.values((this.props.data.steam) ? this.props.data.steam : {});
        chilledwater = Object.values((this.props.data.chilledwater) ? this.props.data.chilledwater : {});

        function conMili(secs) {
            var t = new Date(1970, 0, 1); // Epoch
            t.setTime(secs * 1000);
            return t; 
        }

        var data3 =[];

        for (let i = 0; i < electricity.length; i++) {
            data3.push({
                timestamp: conMili(timestamp[i]), 
                electricity: electricity[i],
                hotwater: hotwater[i],
                steam: steam[i],
                chilledwater: chilledwater[i]
            })
        }
      return (
        <div style={{display:"flex", justifyContent:"space-around"}}>
            <LineChart
                width={350}
                height={300}
                data={data3}
                margin={{
                    top: 5,
                    right: 20,
                    left: 15,
                    bottom: 5
                }}
                >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis unit={"kW"} domain={['auto', 'auto']} />
                <Tooltip />
                <Legend />
                <Line
                    dot={false}
                    type="monotone"
                    dataKey="chilledwater"
                    stroke="#8884d8"
                /> 
            </LineChart>
            <LineChart
                width={350}
                height={300}
                data={data3}
                margin={{
                    top: 5,
                    right: 20,
                    left: 15,
                    bottom: 5
                }}
                >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis unit={"kW"} domain={['auto', 'auto']} />
                <Tooltip />
                <Legend />
                <Line dot={false} type="monotone" dataKey="electricity" stroke="#82ca9d" />
                
            </LineChart>


            <LineChart
                width={350}
                height={300}
                data={data3}
                margin={{
                    top: 5,
                    right: 20,
                    left: 15,
                    bottom: 5
                }}
                >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis unit={"kW"} domain={['auto', 'auto']} />
                <Tooltip />
                <Legend />
                <Line dot={false} type="monotone" dataKey="steam" stroke="orange" />
                
            </LineChart>

               <LineChart
                width={350}
                height={300}
                data={data3}
                margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5
                }}
                >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis unit={"kW"} type="number" domain={['auto', 'auto']} />
                <Tooltip />
                <Legend />
                <Line dot={false}type="monotone" dataKey="hotwater" stroke="red" />
                
            </LineChart>

            
        </div>
      );
    }
  }




 
 