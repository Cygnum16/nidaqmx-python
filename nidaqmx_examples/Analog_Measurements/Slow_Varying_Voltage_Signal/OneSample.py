""".

Python DAQmx API program:
    OneSample

Author:
    Andrés Vega

Example Category:
    Analog Measurement

Description:
    This example demonstrates how to take a single Measurement (Sample) from an
    Analog Input Channel.

Instructions for Running:
    1. Select the Physical Channel to correspond to where your signal is input
    on the DAQ device.
    2. Enter the Minimum and Maximum Voltage Ranges.
    Note: For better accuracy try to match the Input Ranges to the expected
    voltage level of the measured signal.
    Note: Use the Gen Voltage Update example to provide a signal on
    your DAQ device to measure.

Steps:
    1. Create a task.
    2. Create an Analog Input Voltage Channel.
    3. Use the Read function to Measure 1 Sample from 1 Channel on the Data
    Acquistion Card. Set a timeout so an error is returned if the sample is
    not returned in the specified time limit.
    4. Display an error if any.

I/O Connections Overview:
    Make sure your signal input terminal matches the Physical
    Channel I/O Control

"""
# Import needed modules

import nidaqmx
from nidaqmx.constants import TerminalConfiguration
import nidaqmx.errors as DAQmxError
import sys
import os

# Input parameters used for DAQmx channel configuration -----------------------

physical_channel_name = 'cDAQ1Mod2/ai0'
# Maximum and minimum values
range_min = -10.0
range_max = 10.0

# Fixed parameters ------------------------------------------------------------
terminal = TerminalConfiguration.DEFAULT

# Auxiliar functions ----------------------------------------------------------


def exit_application():
    """.

    This function is used to terminate the application in case of an error
    or in case of keyboard interrupt

    """
    print("Application Ended")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)


def print_error_info(error):
    """.

    This function prints out error information

    """
    print("DAQmx error", error.error_code, "occurred")
    print("Cause: ", error.error_type)

# Configure DAQmx Task --------------------------------------------------------


with nidaqmx.Task() as task:
    try:
        # Create Analog Input Channel with the desired settings
        channel_1 = task.ai_channels.add_ai_voltage_chan(physical_channel_name,
                                                         terminal_config= # noqa
                                                         terminal,
                                                         max_val=range_max,
                                                         min_val=range_min)

# Start Task ------------------------------------------------------------------
        task.start()
        # DAQmx read ----------------------------------------------------------
        data = task.read()
        print(data)

    except KeyboardInterrupt:
        # DAQmx Stop Code -----------------------------------------------
        print("Stopping acquisition")
        task.stop()
        print("Task Stopped")
        exit_application()

    # Error handling ----------------------------------------------------------
    except DAQmxError.DaqError as err:
        print_error_info(err)
        task.stop()
        exit_application()
