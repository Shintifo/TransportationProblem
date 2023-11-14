# Transportation problem solver

<!-- ABOUT THE PROJECT -->
## About The Project
Implementation of solution for the transportation problem using 3 different methods.

a. North-West corner method,
b. Vogel’s approximation method,
c. Russell’s approximation method.


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
For the problem\
#TODO
the input.txt file should look like this:\
#TODO

Running the code:

    python main.py

Output format:
* A vector of decision variables - x
* Maximum (minimum) value of the objective function.

* The string ”The method is not applicable!”
or  The string ”The problem is not balanced!”
or Print (demonstrate) input parameter table (a table constructed using matrix C, vectors S and D).
* 3 vectors of initial basic feasible solution - x
0 using North-West corner method, Vogel’s
approximation method, and Russell’s approximation method

Example output:
    
    #TODO

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