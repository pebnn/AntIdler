import time


# File for detecting login alerts or general alerts such as HC expire or BC expire and others.

# Todo: Run image though checks for each alert type and return click coords for relevant alert type
def detectAlert(win):
    time.sleep(0.5)
    screen = win.capture_as_image() # capture screen as PIL.Image.Image class
    print("image taken")

    # Check pixel rgb values and detect alert type, then return click function for relevant alert type

    alertType = None

    return alertType