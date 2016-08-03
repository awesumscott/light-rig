# light-rig
A light controller framework for building custom DMX lightshows running on a Raspberry Pi

This controller uses the Open Lighting Architecture Python module to control DMX lights from a Raspberry Pi. The
main purpose of this is to provide a fast way of producing lighting effects during stage performances, but it may
be extended in the future to allow for complex animation planning. I have also included a "virtual" mode for testing
the software and configuration files without setting up any hardware, using Tk to draw representations of the light fixtures.

The framework is set up using modules to create lighting effects. Modules represent effects such as Strobe,
Color Fader, Chase, Pulse, and also includes groups of other modules, and transitioning between modules. Each module (and
subsequent downstream modules, if any) are assigned a Fixture Group to update, and each module can apply updates and edit
the previous module's updates. The controller accumulates all of these updates and formats them to send to the lights via
the OLA Python bindings.

There is also a simple menu system included to allow for sending commands from a keyboard, number pad, foot switch, or any
other input device that can send keystrokes. It allows nested menus, passing parameters, and labelling for testing purposes.
