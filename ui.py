import solara
import qwiic_relay
import busio
from database import DatabaseManager
from config import Config
from config import SolaraStore
from sensors import SensorManager


@solara.component
class SensorDisplay:
    def __init__(self):
        self.sensor_manager = SensorManager()

    @solara.component
    def SnapshotButton():
        #db_manager = DatabaseManager(Config.DB_FILE)
        # recorded_data, columns = db_manager.fetch_records('snapshots')
        sensor_manager = SensorManager()

        with solara.Column():
            solara.Button("Take Snapshot", on_click=sensor_manager.take_snapshot)  # Pass the function here
            solara.Markdown(f"Numb of Snapshots: { SolaraStore.numb_snapshots.value }")

    @solara.component
    def DistanceComponent():
        with solara.Column():
            solara.Button("Measure Distance", on_click=SensorManager.measure_distance)
            solara.Markdown(f"Distance: {SolaraStore.distance_value.value if SolaraStore.distance_value.value else 'N/A'} cm")



    @solara.component
    def RelayButton():
        plug_relay = qwiic_relay.QwiicRelay(Config.RELAY_ADDRESS)

        if plug_relay.begin() == False:
            solara.Error("The Qwiic Relay isn't connected to the system. Please check your connection")
            return
        def toggle_relay():

            if not plug_relay.begin():
                print("Relay initialization failed.")
                return

            if SolaraStore.state_relay.value:  # Check current value
                plug_relay.set_relay_off()
            else:
                plug_relay.set_relay_on()

            # Update the reactive variable
            SolaraStore.state_relay.set(not SolaraStore.state_relay.value)

        with solara.Column():
            solara.Button("Toggle Relay", on_click=toggle_relay)
            solara.Markdown(f"Relay is currently: {'ON' if SolaraStore.state_relay.value else 'OFF'}")



    @solara.component
    def CombinedGraph():
        db_manager = DatabaseManager()
        recorded_data, columns = db_manager.fetch_records('snapshots')
        timestamps = [row[1] for row in recorded_data]  # Extract timestamps
        temperatures = [row[2] for row in recorded_data]  # Extract temperatures
        gallons = [row[3] for row in recorded_data]  # Extract temperatures
        # relay_on_temp = [st.session_state['relay_temp_on']] * len(recorded_data)
        # relay_off_temp = [st.session_state['relay_temp_off']] * len(recorded_data)
        colors = ['#5470C6', '#91CC75', '#EE6666']
        options = {
            #https://echarts.apache.org/en/option.html#series-line.markLine
            #"color": colors,

            "bars": {
                "title": {"text": "Water and Temperature"},
                "tooltip": {},
                "legend": {"data": ["sales"]},
                "xAxis": {"type": "category","data": timestamps},
                "yAxis": [{
                      "type": 'value',
                      "name": 'Water',
                      "position": 'right',
                      "alignTicks": True,
                      "offset": 80,
                      "axisLine": {
                        "show": True,
                        "lineStyle": {
                          "color": "blue"
                        }
                      },
                      "axisLabel": {
                        "formatter": '{value} gal'
                      }
                    },
                    {
                      "type": 'value',
                      "name": 'Temperature',
                      "position": 'left',
                      "alignTicks": True,
                      "axisLine": {
                        "show": True,
                        "lineStyle": {
                          "color": "purple"
                        }
                      },
                      "axisLabel": {
                        "formatter": '{value} °C'
                      }
                    }
                ],

                "emphasis": {"itemStyle": {"shadowBlur": 10, "shadowOffsetX": 0, "shadowColor": "rgba(0, 0, 0, 0.5)"}},
                "series": [
                    {
                        "name": "Gallons",
                        "yAxisIndex": 0,
                        "type": "line",
                        "smooth": True,
                        "data": gallons,
                        "universalTransition": True,
                        #"color": 'blue',
                        "areaStyle":{},
                    },
                    {
                        "name": "Temperature",
                        "type": "line",
                        "color": 'orange',
                        "yAxisIndex": 1,
                        "markLine": {
                            "data": [{
                                "type": "average",
                                "lineStyle": {
                                    "color": 'dkgrey'
                                },
                            },{
                                "name": 'TBD Relay on Temp',
                                "yAxis": SolaraStore.relay_temp_on.value,
                                "lineStyle": {
                                    "color": 'red'
                                },
                            },{
                                "name": 'Relay off Temp',
                                "yAxis": SolaraStore.relay_temp_off.value,
                                "lineStyle": {
                                    "color": 'green'
                                },
                            },
                            ],
                            "silent": True
                        },
                        "smooth": True,
                        "data": temperatures,
                        "universalTransition": True,
                    }
                ],

            }
        }

        option, set_option = solara.use_state("bars")
        click_data, set_click_data = solara.use_state(None)
        mouseover_data, set_mouseover_data = solara.use_state(None)
        mouseout_data, set_mouseout_data = solara.use_state(None)

        with solara.VBox() as main:
            solara.FigureEcharts(
                option=options[option], on_click=set_click_data, on_mouseover=set_mouseover_data, on_mouseout=set_mouseout_data, responsive=True
            )


        return main


    @solara.component
    def PowerCombinedChart():
        db_manager = DatabaseManager()
        recorded_data, columns = db_manager.fetch_records('snapshots')
        timestamps = [row[1] for row in recorded_data]  # Extract timestamps
        temperatures = [row[2] for row in recorded_data]  # Extract temperatures
        gallons = [row[3] for row in recorded_data]  # Extract temperatures

        colors = ['#5470C6', '#91CC75', '#EE6666']
        options = {
            #https://echarts.apache.org/en/option.html#series-line.markLine

            "bars": {
                "title": {"text": "Solar Amps"},
                "tooltip": {},
                "legend": {"data": ["sales"]},
                "xAxis": {"type": "category","data": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']},
                "yAxis": [{
                      "type": 'value',
                      "name": 'Amps',
                      "position": 'right',
                      "alignTicks": True,
                      "offset": 80,
                      "axisLine": {
                        "show": True,
                        "lineStyle": {
                          "color": "grey"
                        }
                      },
                      "axisLabel": {
                        "formatter": '{value} Amps'
                      }
                    },
                    {
                      "type": 'value',
                      "name": 'Battey',
                      "position": 'left',
                      "alignTicks": True,
                      "axisLine": {
                        "show": True,
                        "lineStyle": {
                          "color": "grey"
                        }
                      },
                      "axisLabel": {
                        "formatter": '{value} %'
                      }
                    }
                ],

                "emphasis": {"itemStyle": {"shadowBlur": 10, "shadowOffsetX": 0, "shadowColor": "rgba(0, 0, 0, 0.5)"}},
                "series": [
                    {
                        "name": "Gallons",
                        "yAxisIndex": 0,
                        "type": "bar",
                        "smooth": True,
                        "data": [
                            20.0, 24.9, -7.0, -10, -2.6, 56.7, 235.6, 162.2, 132.6, 120.0, 16.4, 13.3
                          ],
                        "universalTransition": True,
                        "color": 'orange',
                        "areaStyle":{},
                    },
                    {
                        "name": "Temperature",
                        "type": "line",
                        "color": "red",
                        "yAxisIndex": 1,

                        "smooth": False,
                        "data": [
                            90.6, 50.9, 90.0, 98.4, 78.7, 70.7, 75.6, 82.2, 48.7, 18.8, 16.0, 20.3
                          ],
                        "universalTransition": True,
                    }
                ],

            }
        }

        option, set_option = solara.use_state("bars")
        click_data, set_click_data = solara.use_state(None)
        mouseover_data, set_mouseover_data = solara.use_state(None)
        mouseout_data, set_mouseout_data = solara.use_state(None)

        with solara.VBox() as main:
            solara.FigureEcharts(
                option=options[option], on_click=set_click_data, on_mouseover=set_mouseover_data, on_mouseout=set_mouseout_data, responsive=True
            )


        return main


    @solara.component
    def BatteryDial():
        value = 98

        options = {
            "guage":{
            "series": [
            {
                "type": 'gauge',
                "axisLine": {
                    "lineStyle": {
                        "width": 30,
                        "color": [
                            [0.3, '#A62639'],
                            [0.7, '#C96939'],
                            [1, '#1D523D']
                        ]
                    }
                },
                "pointer": {
                    "itemStyle": {
                        "color": 'auto'
                    }
                },
                "axisTick": {
                    "distance": -30,
                    "length": 8,
                    "lineStyle": {
                        "color": '#343232',
                        "width": 2
                    }
                },
                "splitLine": {
                    "distance": -30,
                    "length": 30,
                    "lineStyle": {
                    "color": '#343232',
                        "width": 4
                    }
                },
                "axisLabel": {
                    "color": 'inherit',
                    "distance": 40,
                    "fontSize": 20
                },
                "detail": {
                    "valueAnimation": True,
                    "formatter": '{value} %',
                    "color": 'inherit'
                },
                "data": [
                    {
                    "value": value
                    }
                ]
            }
            ]
            }
        }


        option, set_option = solara.use_state("guage")
        click_data, set_click_data = solara.use_state(None)
        mouseover_data, set_mouseover_data = solara.use_state(None)
        mouseout_data, set_mouseout_data = solara.use_state(None)

        with solara.VBox() as main:
            solara.FigureEcharts(
                option=options[option], on_click=set_click_data, on_mouseover=set_mouseover_data, on_mouseout=set_mouseout_data, responsive=True
            )


        return main
