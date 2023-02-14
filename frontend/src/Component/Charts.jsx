import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { React, PureComponent } from 'react';




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

        var data3 = [];

        for (let i = 0; i < electricity.length; i++) {
            data3.push({
                timestamp: conMili(timestamp[i]),
                electricity: electricity[i],
                hotwater: hotwater[i],
                steam: steam[i],
                chilledwater: chilledwater[i]
            })
        }
        var colors = {
            chilledwater: "#8884d8",
            electricity: "#82ca9d",
            steam: "orange",
            hotwater: "red",
        }
        var meters = Object.keys(colors)
        return (
            <div style={{ width: "100%", height: "400px" }}>
                {
                    meters.map(key => (
                            <ResponsiveContainer width='90%' height={300} key={key}>
                            <LineChart
                                data={data3}
                                margin={{
                                    top: 5,
                                    right: 20,
                                    left: 15,
                                    bottom: 5
                                }}
                            >
                                <Legend />
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="timestamp" tickFormatter={s => s.toISOString().slice(0,7)}/>
                                <YAxis unit={"kW"} domain={['auto', 'auto']} />
                                <Tooltip />
                                
                                <Line
                                    dot={false}
                                    type="monotone"
                                    dataKey={key}
                                    stroke={colors[key]}
                                />
                            </LineChart>
                            </ResponsiveContainer>
                    ))
                }

            </div>

        );
    }
}





