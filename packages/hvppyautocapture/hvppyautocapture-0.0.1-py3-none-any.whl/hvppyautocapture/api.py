from hvppyautocapture.captureregionhelper import CaptureRegionHelper
from hvppyautocapture.engine import Engine


def get_float(message: str):
    while True:
        value = input(message)
        try:
            value = float(value)
            return value
        except ValueError:
            print("Invalid value. Please enter a number.")

def interactive_run():
    first_page = int(input("first page? "))
    last_page = int(input("last page? "))
    capture_region = CaptureRegionHelper().start()
    next_button = input("next page button[right/pagedown/...]? ")
    file_prefix = input("file name prefix? ")
    initial_delay = get_float("initial delay[seconds]? ")
    delay_before_capture = get_float("wait time before each capture?[seconds] ")
    delay_after_capture = get_float("wait time after each capture?[seconds] ")
    
    engine = Engine(
        first_page=first_page,
        last_page=last_page,
        next_button=next_button,
        file_prefix=file_prefix,
        delay_before_capture=delay_before_capture,
        delay_after_capture=delay_after_capture, 
        initial_delay=initial_delay,
        capture_region=capture_region
    )
    
    engine.run()