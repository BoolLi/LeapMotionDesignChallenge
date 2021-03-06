""" CSCI204 Stack lab """
from stack import MyStack
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

stack = MyStack()

RESOLUTION = 30

def printShit():
	print "shit"

def translate( expression ):
    """ Translates the given simple infix arithmetic expression to postfix
        notation. Returns the result as a string.

        Examine each number and operator in the input.
            If it's a number, add it to the output.
            Else if its an operator, handle it
            Else it was an error
        Empty the stack onto the output
    """
    output = ""
    emptyStack()

    for ch in expression:
        if isNumber( ch ) or isVar( ch ):
            output += ch
        elif ch == '(':
            stack.push(ch)
        elif ch == ')':
            while not stack.isEmpty() and stack.peek() != '(':
                output += stack.pop()
            if stack.peek() == '(':
                stack.pop()
            elif stack.peek() == ')':
                raise ParensMismatchException()
            else:
                raise ParensMismatchException()
        elif isOperator( ch ):
            output += handleOperator( ch )
        else:
            raise IllegalExpressionException()
    output += emptyStack() 
    return output

def emptyStack():
    """ Empties the stack while collecting each element as it is removed.
        Returns the collected elements. """
    elements = ""
    while not stack.isEmpty():
        if isOperator(stack.peek()):
            elements += stack.pop()
        elif stack.peek() == '(':
            raise ParensMismatchException()
        else:
            stack.pop()
    return elements

def isNumber( ch ):
    """ Is the given character a number? """
    return (ch >= '0' and ch <= '9')

def isOperator( ch ):
    """ Is the given character an operator? """
    return ch == '+' or ch == '-' or ch == '*' or ch == '/' or ch == '^'

def isX( ch ):
    """ Is the given character an x?"""
    return ch == 'x' or ch == 'X'

def isY( ch ):
    """ Is the given character an x?"""
    return ch == 'y' or ch == 'Y'

def isVar( ch ):
    return isX(ch) or isY(ch)

def handleOperator( operator ):
    """ Pops all operators of the same or greater precedence as the given
	operator from the stack and then pushes the given operator. """
    elements = popHigherPrecedenceOps( operator )
    stack.push( operator )
    return elements

def popHigherPrecedenceOps( operator ):
    """ Pops operators that have precedence >= the given operator. """
    elements = ""
    while (not stack.isEmpty()) and isTopHigherPrecedence( operator ) and stack.peek() != '(':
        elements += stack.pop()
    return elements

def isTopHigherPrecedence( operator ):
    """ Does the operator on the stack top have precedence >= to the
        given operator?
        
        Convert operators into levels of precedence.
        Lower levels indicate lower precedence.
        Additive operators (+ -) are level 0.
        Multiplicative operators (* /) are level 1.
        Then compare the level
    """
    top = stack.peek() 

    
    if operator == '+' or operator == '-':
        opLevel = 0
    elif operator == '*' or operator == '/':
        opLevel = 1
    else:
        opLevel = 2

    if top == '+' or top == '-':
        topLevel = 0
    elif top == '*' or top == '/':
        topLevel = 1
    else:
        topLevel = 2

    return topLevel >= opLevel

def transfer_to_postfix( expression , x, y):
    """computes the answer to a postfix expression
    """
    emptyStack()
    output = ""
    for ch in expression:
        if isNumber(ch):
            stack.push(str(ch))
        elif isX(ch):
            stack.push(x)
        elif isY(ch):
            stack.push(y)
        else:
            right_operator = float(stack.pop())
            left_operator = float(stack.pop())
            if ch == '^':
                output = left_operator ** right_operator
            elif ch == '+':
                output = left_operator + right_operator
            elif ch == '-':
                output = left_operator - right_operator
            elif ch == '*':
                output = left_operator * right_operator
            elif ch == '/':
                output = left_operator / right_operator
            stack.push(output)
    return stack.pop()

class IllegalExpressionException( BaseException ):
    pass

class ParensMismatchException( BaseException ):
    pass

def main():
    print( "Enter 'quit' to end this program" )
    begin = int(raw_input( "Enter the beginning of your range: " ));
    end = int(raw_input ( "Enter the end of the range: " ));
    X = np.linspace(begin, end, RESOLUTION)
    Y = np.linspace(begin, end, RESOLUTION)
    Z = np.zeros((RESOLUTION,RESOLUTION))
    while True:
        infix = raw_input( "Enter a expression for Z(x,y): " )
        if infix == "quit": sys.exit()
        try:
            postfix = translate( infix )
            print( infix + " ==> " + postfix )
            break
        except IllegalExpressionException:
            print("Error. Illegal operator.")
        except ParensMismatchException:
            print("Error. Mismatsched parenthesis.")

    for i in range(RESOLUTION):
        for j in range(RESOLUTION):
            Z[i][j] = transfer_to_postfix( postfix, X[i], Y[j] )

    X,Y = np.meshgrid(X,Y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap = "Oranges_r", linewidth=0, antialiased=True)
    plt.show()
