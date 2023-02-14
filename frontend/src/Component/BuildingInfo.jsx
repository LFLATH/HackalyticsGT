import { React, PureComponent } from 'react';




export default class BuildingInfo extends PureComponent {

    innerRender = () => {
        if (this.props.loading) {
            return (
                <div>
                    Loading...
                </div>
            )
        }
        else if (!this.props.data) {
            return (
                <div>
                    Enter a building query and press enter in the search box. Building data will be shown here.
                </div>
            )
        } else {
            if (!this.props.foundBuildingData || !this.props.buildingData) {
                return (
                    <div>
                        Detailed information was not found for this building.
                    </div>
                )
            } else {
                return (
                    <div>
                        <div>
                        # Floors: {this.props.buildingData.floor_count}
                        </div>
                        <div>
                        Primary use: {this.props.buildingData.primary_use}
                        </div>
                        <div>
                        Building Area: {this.props.buildingData.square_feet} sqft
                        </div>
                        <div>
                        Year Built: {this.props.buildingData.year_built}
                        </div>
                    </div>
                )
            }
        }
    }

    render() {
        return (
            <div class="flex-child" style={{ width: "min-content" }}>
                <h2>Building Information</h2>
                {this.innerRender()}
            </div>
        )
    }
}