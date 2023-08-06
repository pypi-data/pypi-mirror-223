import time
import pyautogui


class Engine:
    def __init__(
            self, 
            first_page: int,
            last_page: int,
            next_button: str, 
            file_prefix: str, 
            delay_before_capture: float, 
            delay_after_capture: float, 
            initial_delay: float,
            capture_region: tuple[int] = None
        ) -> None:
        self.first_page: int = first_page
        self.last_page: int = last_page
        self.next_button: str = next_button
        self.file_prefix: str = file_prefix
        self.delay_before_capture: float = delay_before_capture
        self.delay_after_capture: float = delay_after_capture
        self.initial_delay: float = initial_delay
        self.capture_region: tuple[int] = capture_region
        
    def count_down_seconds(self, seconds: int):
        if seconds < 0:
            return
        for i in range(seconds, 0, -1):
            print(f"\r{i}...", end="")
            time.sleep(1)
        print()
    
    def count_down_float(self, seconds: float):
        self.count_down_seconds(int(seconds))
        remaining_seconds = seconds - int(seconds)
        time.sleep(remaining_seconds)
        
    def run(self):
        self.count_down_float(int(self.initial_delay))
        
        for page in range(self.first_page, self.last_page + 1):
            ndigits = len(str(self.last_page))
            page_str = str(page).zfill(ndigits)
            time.sleep(self.delay_before_capture)
            file_name = f"{self.file_prefix}{page_str}.png"
            pyautogui.screenshot(file_name, region=self.capture_region)
            time.sleep(self.delay_after_capture)
            if self.next_button:
                pyautogui.press(self.next_button)
            print(f"{page}/{self.last_page} {file_name}")