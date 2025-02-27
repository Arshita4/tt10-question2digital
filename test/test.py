# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Resetting DUT")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Testing priority encoder behavior")

    # Iterate through all possible input combinations
    for i in range(16):  # Only testing `ui_in` since `uio_in` is unused
        if 15-i<8:
            dut.ui_in.value=1<<(15-i)
        else:
            dut.ui_in.value=0
        # Wait for stable output
        await ClockCycles(dut.clk, 1)

        # Expected output: Binary representation of the highest active bit
        expected_output = 14 - i if i < 15 else 0b11110000  # Default case
    
