# import solara
# from vedirect import VEDirect
# import threading
# import time
# from config import Config
# from config import SolaraStore


# @solara.component
# def RealTimePower():
#     victron_poll_internal   = Config.VICTRON_POLL_INTERVAL
#     is_running              = solara.reactive(False)  # Track if updates are running

#     def fetch_data():
#         # print(f"-----------------------------------9999 {is_running.value}")
#         try:
#             ve = VEDirect("/dev/ttyUSB0", 60)  # Initialize VEDirect with the correct serial port
#             # print(f"-----------------------------------3 {is_running.value}")
#             while is_running.value == True:
#                 # print("-----------------------------------4")
#                 try:
#                     data = ve.read_data_single()  # Fetch one packet of data

#                     print(data)
#                     # set_attributes(data)  # Store all attributes dynamically
#                     # attributes.set(data)
#                     # Extract specific attributes for display
#                     if "SOC" in data:
#                         SolaraStore.bvm_soc.set(f"{float(data['SOC']) / 10:.1f}")
#                     if "V" in data:
#                         SolaraStore.bvm_voltage.set(f"{float(data['V']) / 1000:.2f}")  # Convert voltage to volts
#                     if "I" in data:
#                         SolaraStore.bvm_current.set(f"{float(data['I']) / 1000:.2f}")  # Convert current to amps
#                 except Exception as e:
#                     SolaraStore.bvm_error_output.set(f"Error reading data: {e}")
#                 time.sleep(victron_poll_internal)
#         except Exception as e:
#             SolaraStore.bvm_error_output.set(f"Error initializing VEDirect: {e}")
#             is_running.set(False)

#     def start_reading():
#         if is_running.value == False:
#             # print("<<<<<<<<<<<<<<<,1")
#             is_running.set(True)
#             thread = threading.Thread(target=fetch_data, daemon=True)
#             # print("<<<<<<<<<<<<<<<,2")
#             thread.start()
#             # print("<<<<<<<<<<<<<<<,3")

#     def stop_reading():
#         is_running.set(False)
#         reset_states()

#     def reset_states():
#         SolaraStore.bvm_soc.set(-1)
#         SolaraStore.bvm_voltage.set("N/A")
#         SolaraStore.bvm_current.set("N/A")
#         SolaraStore.bvm_error_output.set("NO Errors")
#         SolaraStore.bvm_attributes.set({})

#     return solara.Column(
#         [
#             solara.Button("Start Reading", on_click=start_reading),
#             solara.Button("Stop Reading", on_click=stop_reading),
#             solara.Markdown("### Real-Time Data"),
#             solara.Markdown(f"**SOC:** {SolaraStore.bvm_soc.value} %"),
#             solara.Markdown(f"**Voltage:** {SolaraStore.bvm_voltage.value} Volts"),
#             solara.Markdown(f"**Current:** {SolaraStore.bvm_current.value} Amps"),
#             # solara.Markdown("### All Attributes:"),
#             # # solara.Markdown(f"{attributes}"),  # Display all attributes as a dictionary
#             solara.Markdown(SolaraStore.bvm_error_output.value, style="color:red"),  # Display errors
#         ]
#     )



# # import solara
# # from vedirect import VEDirect


# # class Victron:
# #     def __init__(self):
# #         try:
# #             print("-----------------")
# #         except Exception as e:
# #             solara.Error("Couldnt Setup VEDirect")



# #     @solara.component
# #     def RealTimePower():
# #         voltage, set_voltage = solara.use_state("N/A")
# #         current, set_current = solara.use_state("N/A")
# #         soc, set_soc = solara.use_state("N/A")
# #         error_output, set_error_output = solara.use_state("")

# #         def start_reading():
# #             try:
# #                 ve = VEDirect("/dev/ttyUSB0", 60)

# #                 def handle_data(packet):

# #                     # Extract specific attributes from the packet
# #                     if "V" in packet:  # Replace "V" with the actual key for voltage
# #                         set_voltage(f"{float(packet['V']) / 1000:.2f} V")  # Example conversion to volts
# #                     if "I" in packet:  # Replace "I" with the actual key for current
# #                         set_current(f"{float(packet['I']) / 1000:.2f} A")  # Example conversion to amps
# #                     if "SOC" in packet:  # Replace "I" with the actual key for current
# #                         set_soc(f"{float(packet['SOC']) / 10:.2f} %")  # Example conversion to amps

# #                 ve.read_data_callback(handle_data)
# #             except Exception as e:
# #                 set_error_output(f"Error: {e}")

# #         return solara.Column(
# #             [
# #                 solara.Button("Start Reading", on_click=start_reading),
# #                 solara.Markdown("### SOC:"),
# #                 solara.Markdown(soc),  # Display voltage
# #                 solara.Markdown("### Voltage:"),
# #                 solara.Markdown(voltage),  # Display voltage
# #                 solara.Markdown("### Current:"),
# #                 solara.Markdown(current),  # Display current
# #                 solara.Markdown(error_output, style="color:red"),  # Display errors
# #             ]
# #         )