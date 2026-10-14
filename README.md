# C++ Module 01 — Memory Allocation, Pointers to Members, References and Switch Statements

A collection of exercises from the **42 C++ curriculum**, implemented in **C++98**. This module introduces object lifetime, stack and heap allocation, references, pointers, file I/O, pointers to member functions, and `switch` statements.

## Exercises

| Exercise | Name | Main concepts |
| --- | --- | --- |
| `ex00` | BraiiiiiiinnnzzzZ | Stack vs. heap allocation, constructors and destructors |
| `ex01` | Moar brainz! | Dynamic arrays, `new[]` and `delete[]` |
| `ex02` | HI THIS IS BRAIN | Pointer and reference syntax, addresses and values |
| `ex03` | Unnecessary violence | References vs. pointers as class members |
| `ex04` | Sed is for losers | File streams, string searching and replacement |
| `ex05` | Harl 2.0 | Pointers to non-static member functions |
| `ex06` | Harl filter | `switch` and log-level filtering |

`ex06` is optional in the original assignment.

## Requirements

- A C++ compiler supporting **C++98**
- `make`

The provided Makefiles use:

```sh
c++ -Wall -Wextra -Werror -std=c++98
```

## Build and run

Each exercise is compiled independently from its own directory:

```sh
cd ex03
make
./violence
```

For the exercises with provided implementations:

### ex03 — Unnecessary violence

```sh
cd ex03
make
./violence
```

`HumanA` holds a `Weapon&` because it must be armed from construction. `HumanB` holds a `Weapon*` because it may initially have no weapon. Both refer to the original `Weapon`, so changes made through `setType()` are visible during later attacks.

### ex04 — Sed is for losers

```sh
cd ex04
make
./replace input.txt old new
```

The program writes the modified content to `input.txt.replace` without changing `input.txt`. Replacement is implemented using `std::string::find()` and `substr()`; `std::string::replace()` is prohibited by the assignment. An empty search string is rejected.

If `test_ex04.py` is present alongside the Makefile, run:

```sh
python3 test_ex04.py
```

### ex05 — Harl 2.0

```sh
cd ex05
make
./harl
```

The `Harl` class selects `DEBUG`, `INFO`, `WARNING`, or `ERROR` handlers through an array of **pointers to member functions**, rather than a long `if/else if` chain.

### ex06 — Harl filter

```sh
cd ex06
make
./harlFilter WARNING
```

The filter prints messages at the requested level and all higher levels. For `WARNING`, it prints `WARNING` and `ERROR`. Unknown levels produce the default message.

## Makefile targets

| Command | Action |
| --- | --- |
| `make` | Build the executable |
| `make clean` | Remove object files |
| `make fclean` | Remove object files and the executable |
| `make re` | Rebuild from scratch |

## Key takeaways

- Use **stack allocation** for objects whose lifetime is limited to the current scope; use **heap allocation** when dynamically managed lifetime is required.
- A **reference** must bind to an object when initialized and cannot be reseated. A **pointer** can be null or redirected to another object.
- A **non-static member function pointer** must be invoked through an object (using `.*`) or an object pointer (using `->*`).
- `switch` dispatches on integral or enumeration values; without `break`, execution continues into the next case.

The project targets the 42 C++ Module 01 requirements, including C++98 compatibility.
