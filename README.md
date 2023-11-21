# Transportation problem solver

<!-- ABOUT THE PROJECT -->
## About The Project
Implementation of solution for the transportation problem using 3 different methods.

1. North-West corner method,
2. Vogel’s approximation method,
3. Russell’s approximation method.


### Built With

* [Python](https://www.python.org/)

<!-- GETTING STARTED -->
## Installation
In terminal run the following:

    git clone git@github.com/Shintifo/TransportationProblem.git
    cd TransportationProblem
    pip install -r requirements.txt


<!-- USAGE EXAMPLES -->
## Usage
Input format:
The input contains:

* A vector of coefficients of supply - S.
* A matrix of coefficients of costs - C.
* A vector of coefficients of demand - D.

Input Example:

| Source    | B1 | B2 | B3 | B4 | Supply |
| --------- | -- | -- | -- | -- | ------ |
| A1        | 2 | 4 | 5 | 3 | 10 |
| A2        | 1 | 2 | 5 | 4 | 7 |
| A3        | 3 | 5 | 2 | 1 | 8 |
| Demand    | 5 | 9 | 8 | 3 | 25 |

the input.txt file should look like this:

    #A vector of coefficients of supply:
    10 7 8
    #A vector of coefficients of demand:
    5 9 8 3
    #A matrix of coefficients of costs:
    2 4 5 3
    1 2 5 4
    3 5 2 1

Running the code:

    python main.py

Output format:

* The string ”The method is not applicable!”
or  The string ”The problem is not balanced!”
or Print (demonstrate) input parameter table (a table constructed using matrix C, vectors S and D).
* 3 vectors of initial basic feasible solution x0 using North-West corner method, Vogel’s
approximation method, and Russell’s approximation method

Example output:

    Initial table:
    ╒═════╤═════╤═════╤═════╤═════╕
    │  1  │  2  │  3  │  4  │  S  │
    ╞═════╪═════╪═════╪═════╪═════╡
    │  2  │  4  │  5  │  3  │ 10  │
    ├─────┼─────┼─────┼─────┼─────┤
    │  1  │  2  │  5  │  4  │  7  │
    ├─────┼─────┼─────┼─────┼─────┤
    │  3  │  5  │  2  │  1  │  8  │
    ├─────┼─────┼─────┼─────┼─────┤
    │  5  │  9  │  8  │  3  │     │
    ╘═════╧═════╧═════╧═════╧═════╛
    North-West:
    [5, 5, 0, 0, 0, 4, 3, 0, 0, 0, 5, 3]
    Vogel rule:
    [5, 2, 0, 3, 0, 7, 0, 0, 0, 0, 8, 0]
    Russel rule:
    [5, 2, 0, 3, 0, 7, 0, 0, 0, 0, 8, 0]

<!---
## Options

-h, --help            show this help message and exit\
-i INPUT, --input INPUT\
                    Set input file path. Default: input.txt\
-l, --log             Set logging. Default: False\
-p PROBLEM, --problem PROBLEM\
                    Set problem type. Possible values: min, max. Default: max\
-a ACCURACY, --accuracy ACCURACY\
                    Set approximation accuracy. Default: 0.001
-->
