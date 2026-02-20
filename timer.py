import time

seconds = 5
print(f"Timer set for {seconds} seconds...")
time.sleep(seconds)
print("\a")  # terminal bell
print("Time's up!")
