# DuckyScript3 Instructions Reference

This document provides detailed documentation for all supported DuckyScript3 instructions in RasperDucky, along with examples.

## Table of Contents
- [Variables](#variables)
- [Control Flow](#control-flow)
- [Functions](#functions)
- [Constants](#constants)
- [Keyboard Commands](#keyboard-commands)
- [Operators](#operators)

## Variables

Variables in RasperDucky are global and store integer values. They must start with a `$` symbol.

```duckyscript
# Variable declaration and assignment
$counter = 0
$result = 42

# Arithmetic operations
$sum = $counter + 5
$product = $result * 2
$quotient = $result / 2
$difference = $result - 10

# Using variables in conditions
IF $counter < 10 THEN
    STRING Counter is less than 10
END_IF
```

## Control Flow

### IF Statements

```duckyscript
# Basic if statement
IF $x > 0 THEN
    STRING X is positive
END_IF

# If-else statement
IF $x == 0 THEN
    STRING X is zero
ELSE
    STRING X is not zero
END_IF

# If-else if-else statement
IF $x < 0 THEN
    STRING X is negative
ELSE IF $x == 0 THEN
    STRING X is zero
ELSE
    STRING X is positive
END_IF
```

### WHILE Loops

```duckyscript
# Basic while loop
$count = 0
WHILE ($count < 5)
    STRING Count is: 
    STRING $count
    ENTER
    $count = $count + 1
END_WHILE

# While loop with multiple conditions
WHILE ($x > 0 && $y < 10)
    STRING Processing...
    $x = $x - 1
    $y = $y + 1
END_WHILE
```

## Functions

Functions in RasperDucky don't accept parameters and can't return values. They are useful for organizing code into reusable blocks.

```duckyscript
# Function definition
FUNCTION open_notepad()
    GUI R
    DELAY 500
    STRING notepad
    ENTER
END_FUNCTION

# Function call
open_notepad()

# Function with shared variables
FUNCTION increment_counter()
    $counter = $counter + 1
END_FUNCTION

$counter = 0
increment_counter()
# $counter is now 1
```

## Constants

Constants are defined using the `DEFINE` keyword and must start with a `#` symbol.

```duckyscript
# Define constants
DEFINE #MAX_ATTEMPTS 3
DEFINE #DELAY_MS 500

# Using constants
$attempts = 0
WHILE ($attempts < #MAX_ATTEMPTS)
    STRING password123
    ENTER
    DELAY #DELAY_MS
    $attempts = $attempts + 1
END_WHILE
```

## Keyboard Commands

### Basic Key Commands

```duckyscript
# Single key press
ENTER
SPACE
TAB
ESC
BACKSPACE

# Key combinations
CTRL C
ALT TAB
GUI R
CTRL ALT DEL
```

### Text Input

```duckyscript
# Print text without ENTER
STRING Hello, World!

# Print text with ENTER
STRINGLN Hello, World!

# Delay execution (in milliseconds)
DELAY 1000
```

### Keyboard Layout Configuration

```duckyscript
# Set keyboard layout for Windows French
RD_KBD WIN FR

# Set keyboard layout for Mac UK
RD_KBD MAC UK
```

## Operators

### Arithmetic Operators

```duckyscript
# Basic arithmetic
$result = 10 + 5    # Addition
$result = 10 - 5    # Subtraction
$result = 10 * 5    # Multiplication
$result = 10 / 5    # Division

# Operator precedence
$result = 10 + 2 * 3    # Results in 16 (multiplication first)
$result = (10 + 2) * 3  # Results in 36 (parentheses first)
```

### Comparison Operators

```duckyscript
# Equal to
IF $x == 10 THEN
    STRING Equal
END_IF

# Not equal to
IF $x != 5 THEN
    STRING Not equal
END_IF

# Greater than
IF $x > 0 THEN
    STRING Positive
END_IF

# Less than
IF $x < 0 THEN
    STRING Negative
END_IF

# Greater than or equal to
IF $x >= 10 THEN
    STRING Greater or equal
END_IF

# Less than or equal to
IF $x <= 10 THEN
    STRING Less or equal
END_IF
```

### Logical Operators

```duckyscript
# AND operator
IF ($x > 0 && $y < 10) THEN
    STRING Both conditions are true
END_IF

# OR operator
IF ($x == 0 || $y == 0) THEN
    STRING At least one is zero
END_IF

# NOT operator
IF !($x == 0) THEN
    STRING X is not zero
END_IF
```
