import solara
import json
import paho.mqtt.client as mqtt

# Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "vedirect/attributes"

# A global variable to hold the latest MQTT message
latest_message = solara.reactive({})

#TODO move to config
bvm_soc = solara.reactive(-1)
bvm_power = solara.reactive(-1)
bvm_time_remaining = solara.reactive(-1)
bvm_voltage = solara.reactive("N/A")
bvm_current = solara.reactive("N/A")
bvm_error_output = solara.reactive("NO Errors")



@solara.component
class VictronMqtt:

    # MQTT Callback Functions
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            client.subscribe(MQTT_TOPIC)
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            latest_message.set(data)

            #### Need to build out seperately
            if "SOC" in data:
                bvm_soc.set(f"{float(data['SOC']) / 10:.1f}")
                # SolaraStore.bvm_soc.set(f"{float(data['SOC']) / 10:.1f}")
            if "V" in data:
                bvm_voltage.set(f"{float(data['V']) / 1000:.2f}")  # Convert voltage to volts
            if "P" in data:
                bvm_power.set(f"{float(data['P']) / 10:.2f}")  # Convert current to amps
            if "TTG" in data:
                bvm_time_remaining.set(f"{float(data['TTG']) }")
            if "I" in data:
                bvm_current.set(f"{float(data['I']) / 10:.2f}")  # Convert current to amps

        except json.JSONDecodeError:
            print("Failed to decode JSON from MQTT message")


    # Initialize and connect the MQTT client
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")

    # Solara Component
    def MQTTDashboard():
        with solara.Column():
            solara.Markdown("# VE.Direct Dashboard")

            if not latest_message.value:
                solara.Info("Waiting for data...")
            else:
                for key, value in latest_message.value.items():
                    solara.Text(f"**{key}**: {value}")


    @solara.component
    def BatteryDial():
        value = bvm_soc.value

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

    @solara.component
    def AmpsDial():
        value = bvm_current.value

        options = {
            "amps":{
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
                    "formatter": '{value} amps',
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

        option, set_option = solara.use_state("amps")
        click_data, set_click_data = solara.use_state(None)
        mouseover_data, set_mouseover_data = solara.use_state(None)
        mouseout_data, set_mouseout_data = solara.use_state(None)

        with solara.VBox() as main:
            solara.FigureEcharts(
                option=options[option], on_click=set_click_data, on_mouseover=set_mouseover_data, on_mouseout=set_mouseout_data, responsive=True
            )

        return main
    @solara.component
    def PowerDial():
        value = bvm_power.value

        options = {
            "power":{
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
                    "formatter": '{value} watts?',
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

        option, set_option = solara.use_state("power")
        click_data, set_click_data = solara.use_state(None)
        mouseover_data, set_mouseover_data = solara.use_state(None)
        mouseout_data, set_mouseout_data = solara.use_state(None)

        with solara.VBox() as main:
            solara.FigureEcharts(
                option=options[option], on_click=set_click_data, on_mouseover=set_mouseover_data, on_mouseout=set_mouseout_data, responsive=True
            )

        return main


    @solara.component
    def TTGText():
        solara.Markdown(f"# {bvm_time_remaining} Minutes")





# **PID**: 0xA381
# **V**: 27264
# **I**: 307     main battery Current
# **P**: 8       W    instatnacous power
# **CE**: -480   mAh Consumed Amp hours
# **SOC**: 996    state of charge
# **TTG**: -1      Minutes, time to go

# **Alarm**: OFF
# **Relay**: OFF
# **AR**: 0
# **BMV**: 712 Smart
# **FW**: 0412
# **MON**: 0


