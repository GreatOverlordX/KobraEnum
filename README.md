# KobraEnum

## Ophio.py

The name is inspired in the _Ophiophagus hannah_ also known as "King Cobra"
due to its exceptional skills for reconnaissance in its hunting process.

This is a system Enumeration Tool on `Python`.
Necessary libraries -> `psutil` -> run `pip install psutil` to install it.

## Usage

- To get the system information:

```zsh
python3 ophio.py -s
```

- To get the network information:

```zsh
python3 ophio.py -n
```

- To check the installed packages:

```zsh
python3 ophio.py -p
```

- Check the packages version/details:

```zsh
python3 ophio.py -p -v
```

- Check _ONLY_ the packages count:

```zsh
python3 ophio.py -p -c
```

- To run all the flags & get all the information:

```zsh
python3 ophio.py -s -n -p -v
```

Run the `-h` or `--help` command, so you can see the options.

