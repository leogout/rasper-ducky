# Rasper Ducky

<p align="center">
  <img src="docs/img/rasper-ducky-logo.png" alt="Rasper Ducky Logo">
</p>

Welcome to the Rasper Ducky project! This project aims to provide a comprehensive, open-source implementation of DuckyScript3, a scripting language used for automating tasks on USB Rubber Ducky devices. My goal is to achieve a 1-to-1 implementation of DuckyScript3, enabling developers to write and execute scripts on a Raspberry Pi Pico. This project is still in its early stages of development, but I'm working hard to add more features and improve the overall experience.

## Features

- **Partial DuckyScript3 Syntax Support**: Parse and execute scripts written in DuckyScript3, including standard commands and syntax.
- **Logical and Assignment Operations**: Support for complex logical expressions and variable assignments.
- **Extensible Architecture**: Easily extend the parser and interpreter to support additional features or custom commands.
- **Raspberry Pi Pico Support**: Execute scripts on a Raspberry Pi Pico 2.
- **Full test suite**: Ensure the implementation is correct and reliable.
- **Open Source**: Contribute to the project and help me improve the implementation.

To contribute, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Getting Started

### Installation on Raspberry Pi Pico 2
#### Install CircuitPython 9.2.0
- Go to the [CircuitPython website](https://circuitpython.org/board/raspberry_pi_pico/) and download the `CircuitPython 9.2.0` firmware for Raspberry Pi Pico 2 using the "DOWNLOAD .UF2 NOW" button.
- Hold the BOOTSEL button on your Raspberry Pi Pico 2 and connect it to your computer using a USB cable. Once `RPI-RP2` appears in the device manager, release the BOOTSEL button.
- Open your `RPI-RP2` drive and drag and drop the downloaded `.UF2` file to the Raspberry Pi Pico 2.
- Once the Raspberry Pi Pico is restarted, it will appear as `CIRCUITPY` in the device manager.

#### Install the rasper-ducky library
- Connect your Raspberry Pi Pico to your computer and copy/paste the content of the `rasper_ducky` folder to the `CIRCUITPY` drive.
- Create a new file named `payload.dd` at the root of the `CIRCUITPY` drive containing your DuckyScript3 script.
- You can try it out with this simple script, which will open a PowerShell window and print "Hello, World!" 3 times, separated by a space:
```plaintext
DEFINE #COUNT 3

FUNCTION open_powershell()
	GUI R
	STRINGLN powershell
END_FUNCTION

FUNCTION hello_world()
	$x = 0
	WHILE ($x < #COUNT)
	    DELAY 500
		STRING Hello, World!
        SPACE
		$x = $x + 1
	END_WHILE
END_FUNCTION

open_powershell()
DELAY 1000
hello_world()
```

## Debugging

To debug the script, connect to the Raspberry Pi Pico 2 using Putty or similar and use the serial console. I've seen ports up to COM8 on my computer so try them all until you find the correct one.
Once connected, you should see the output of the script in the serial console.

## Roadmap

- [ ] Complete the roadmap
- [ ] Complete 1-to-1 DuckyScript3 implementation
 - [ ] WAIT_FOR_BUTTON_PRESS
 - [ ] BUTTON_DEF
 - [ ] LED_R / LED_G (only one green led on the Raspberry Pi Pico 2)
 - [ ] Random characters (RANDOM_LOWERCASE_LETTER, RANDOM_UPPERCASE_LETTER, RANDOM_LETTER, RANDOM_NUMBER, RANDOM_CHAR)
 - [ ] HOLD / RELEASE
 - [ ] RESTART_PAYLOAD / STOP_PAYLOAD
- [ ] Improve error handling and debugging features


## Thanks

- Thanks to [@hak5](https://github.com/hak5) for the original DuckyScript language.
- Thanks to [@dbisu](https://github.com/dbisu) for [Pico-Ducky](https://github.com/dbisu/pico-ducky), which was the starting point for this project.
- Thanks to the team behind [CircuitPython](https://github.com/adafruit/circuitpython) for the amazing work on this firmware and their support.
- Thanks to the rest of the community for making this fun little project possible (AdaFruit, MicroPython, etc.).
