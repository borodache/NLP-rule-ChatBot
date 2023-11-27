from constants import c_minutes_to_measure

import streamlit as st
import time

start_time = None


def start():
    """Start a new timer"""
    global start_time
    if start_time is not None:
        # raise Exception(f"Timer is running. Use .stop() to stop it")
        return

    start_time = time.perf_counter()


def stop():
    """Stop the timer if the elapsed time (in seconds) is bigger then the provided maximum time (minutes_to_measure
    times 60 seconds)"""
    global start_time
    if start_time is None:
        raise Exception(f"Timer is not running. Use .start() to start it")

    elapsed_time = time.perf_counter() - start_time

    if elapsed_time > 60 * c_minutes_to_measure:
        # print("Argument Clinic: Your time is up! GoodBye!!!")
        start_time = None
        st.text("Argument Clinic: Your time is up! GoodBye!!!")
        return True

    return False
