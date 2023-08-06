import time

last_call_time = time.time()


def speedlimit(milliseconds):
    """
    Slows down a loop by pausing for a given number of milliseconds since the last call.

    Parameters:
        milliseconds (float): Number of milliseconds to limit the loop's speed.

    Returns:
        None
    """
    global last_call_time
    current_time = time.time()
    loop_time = (current_time - last_call_time) * 1000  # Convert to milliseconds
    # TODO Add randomize time ability
    if loop_time < milliseconds:
        time.sleep((milliseconds - loop_time) / 1000)  # Convert back to seconds

    last_call_time = time.time()
