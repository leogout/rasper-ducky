import board
import digitalio
import storage

NO_STORAGE_PIN = digitalio.DigitalInOut(board.GP15)
NO_STORAGE_PIN.switch_to_input(pull=digitalio.Pull.UP)
no_storage_status = NO_STORAGE_PIN.value


if board.board_id == "raspberry_pi_pico":
    # On Pi Pico, default to USB visible
    no_storage = not no_storage_status
else:
    no_storage = False


if no_storage:
    storage.disable_usb_drive()
