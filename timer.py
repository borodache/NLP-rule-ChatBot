import time

# class TimerError(Exception):
#     """A custom exception used to report errors in use of Timer class"""

# class Timer:
#     def __init__(self, minutes: int):
#         self._start_time = None
#         self.minutes_to_measure = minutes

start_time = None
minutes_to_measure = 5


def start():
    """Start a new timer"""
    global start_time
    if start_time is not None:
        raise Exception(f"Timer is running. Use .stop() to stop it")

    start_time = time.perf_counter()


def stop():
    """Stop the timer, and report the elapsed time"""
    global start_time
    if start_time is None:
        raise Exception(f"Timer is not running. Use .start() to start it")

    elapsed_time = time.perf_counter() - start_time

    if elapsed_time > 60 * minutes_to_measure:
        print("Argument Clinic: Your time is up! GoodBye!!!")
        return True

    return False