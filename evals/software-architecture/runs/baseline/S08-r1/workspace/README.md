# HeatingLib

A Modelica library that heats one room: `Room` stores and loses heat, `Thermostat` sets the
heating power from the measured temperature, `System` connects them.

Check the library with OpenModelica:

```sh
omc tests/check.mos
```

The architecture is described in [docs/architecture/arc42.md](docs/architecture/arc42.md).
