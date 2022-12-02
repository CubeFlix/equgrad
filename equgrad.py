# equgrad.py
# Python implementation of the symbolic algebra system.

from typing import TypedDict, List
from __future__ import annotations
from string import ascii_letters


class InvalidSymbolName(Exception):

    """The invalid symbol name exception."""


class AlgebraicObject:

    """The base algebraic object."""

    def __init__(self, *args, **kwargs):

        ...

    def __add__(self, other: AlgebraicObject) -> AlgebraicObject:

        ...

    def __sub__(self, other: AlgebraicObject) -> AlgebraicObject:

        ...

    def __mul__(self, other: AlgebraicObject) -> AlgebraicObject:

        ...

    def __neg__(self) -> AlgebraicObject:

        ...

    def __truediv__(self, other: AlgebraicObject) -> AlgebraicObject:
        
        ...

    def __pow__(self, other: AlgebraicObject) -> AlgebraicObject:

        ...

    def simplify(self) -> AlgebraicObject:

        """Simplify the algebraic object. This will expand all factored 
        polynomials and simplify all sums. Rational expressions will be
        individually factored and then simplified."""

        ...

    def factor(self) -> AlgebraicObject:

        """Factor the algebraic object. This will factor all polynomials
        and rational expressions without simplifying them."""

        ...

    def evaluate(self, symbols: dict) -> float:

        """Evaluate the algebraic object. This requires a dict of symbols, 
        which uses the name of the symbol as the key and its float value
        as the value. Returns the final floating point result."""

        ...


class Number(AlgebraicObject):

    """The number object. Derives from the algebraic object. The number object
    implements a basic floating-point number which can be used in other 
    algebraic calculations."""

    value: float

    def __init__(self, value: float):

        """Create the new number object. The value is a floating-point number
        which represents the value of the number."""

        self.value = value

    def __add__(self, other: AlgebraicObject) -> AlgebraicObject:

        return SumType([self, other])

    def __sub__(self, other: AlgebraicObject) -> AlgebraicObject:

        return SumType([self, -other])

    def __mul__(self, other: AlgebraicObject) -> AlgebraicObject:

        return ProductType([self, other])

    def __truediv__(self, other: AlgebraicObject) -> AlgebraicObject:
        
        return QuotientType(self, other)

    def __pow__(self, other: AlgebraicObject) -> AlgebraicObject:

        return PowType(self, other)

    def __neg__(self) -> AlgebraicObject:

        return Number(-self.value)

    def simplify(self) -> AlgebraicObject:

        """Simplify the algebraic object. This will expand all factored 
        polynomials and simplify all sums. Rational expressions will be
        individually factored and then simplified."""

        return self

    def factor(self) -> AlgebraicObject:

        """Factor the algebraic object. This will factor all polynomials
        and rational expressions without simplifying them."""

        return self

    def evaluate(self, symbols: dict) -> float:

        """Evaluate the algebraic object. This requires a dict of symbols, 
        which uses the name of the symbol as the key and its float value
        as the value. Returns the final floating point result."""

        return self


class Symbol(AlgebraicObject):

    """The symbol object. Derives from the algebraic object. Represents a 
    single variable without a value. Can be used in algebraic expressions."""

    name: str

    def __init__(self, name: str):

        """Create the symbol object. The name is a string of length one and
        can be in a-zA-Z."""

        if len(name) != 1 or not name in ascii_letters:
            # Throw an error.
            raise InvalidSymbolName

        self.name = name

    def __add__(self, other: AlgebraicObject) -> AlgebraicObject:

        return SumType([self, other])

    def __sub__(self, other: AlgebraicObject) -> AlgebraicObject:

        return SumType([self, -other])

    def __mul__(self, other: AlgebraicObject) -> AlgebraicObject:

        return ProductType([self, other])

    def __truediv__(self, other: AlgebraicObject) -> AlgebraicObject:
        
        return QuotientType(self, other)

    def __pow__(self, other: AlgebraicObject) -> AlgebraicObject:

        return PowType(self, other)

    def __neg__(self) -> AlgebraicObject:

        return ProductType(Number(-1), self.value)

    def simplify(self) -> AlgebraicObject:

        """Simplify the algebraic object. This will expand all factored 
        polynomials and simplify all sums. Rational expressions will be
        individually factored and then simplified."""

        return self

    def factor(self) -> AlgebraicObject:

        """Factor the algebraic object. This will factor all polynomials
        and rational expressions without simplifying them."""

        return self

    def evaluate(self, symbols: dict) -> float:

        """Evaluate the algebraic object. This requires a dict of symbols, 
        which uses the name of the symbol as the key and its float value
        as the value. Returns the final floating point result."""

        return symbols[self.name]


class SumType(AlgebraicObject):

    """The sum type algebraic object. The sum type represents a sum of 
    AlgebraicObjects."""

    values: List[AlgebraicObject]

    def __init__(self, values: List[AlgebraicObject]):

        """Create the new sum object. The values are a list of 
        AlgebraicObjects."""

        self.values = values

    # TODO: Functions.

    def simplify(self) -> AlgebraicObject:

        """Simplify the algebraic object. This will expand all factored 
        polynomials and simplify all sums. Rational expressions will be
        individually factored and then simplified."""

        # Simplify the values individually.
        simplified_values = []
        for value in self.values:
            simplified_values.append(value.simplify())

        # Look for all the sum types and combine them into a new list.
        # Do this again and again until there are no more sum types.
        combined_values = simplified_values
        while True:
            new_combined_values = combined_values
            for value in combined_values:
                if type(value) == SumType:
                    # Add the list of values to the combined values list.
                    new_combined_values += value.values
            combined_values = new_combined_values

            # Check if there are no more SumTypes.
            no_sum_types = True
            for value in combined_values:
                if type(value) == SumType:
                    no_sum_types = False
            if no_sum_types:
                break

        # Group like terms.
        like_terms = {Number: Number(0)}
        for value in combined_values:
            if type(value) == Number:
                # Number type.
                like_terms[Number] = Number(like_terms[Number].value + value.value)
            elif type(value) == Symbol:
                # Symbol type. Search for a ProductType of a number and the symbol.
                if value in like_terms:
                    # Add the value.
                    like_terms[value] = ProductType([like_terms[value].values[0].value + 1, value])
                else:
                    # Create the new value.
                    like_terms[value] = ProductType([1, value])
            # Skipping over SumType, since we covered that earlier.
            elif type(value) == ProductType:
                # The ProductType should have been simplified already, so we 
                # can assume that the first item is a Number and contains
                # only other symbols or PowTypes. Order the symbols and pows
                # alphabetically.
                pass

    def factor(self) -> AlgebraicObject:

        """Factor the algebraic object. This will factor all polynomials
        and rational expressions without simplifying them."""

        return self

    def evaluate(self, symbols: dict) -> float:

        """Evaluate the algebraic object. This requires a dict of symbols, 
        which uses the name of the symbol as the key and its float value
        as the value. Returns the final floating point result."""

        # Evaluate the values individually.
        value = 0
        for value in self.values:
            value += value.evaluate(symbols)

        return value
    

class ProductType(AlgebraicObject):

    """The product type algebraic object. The product type represents a
    product of AlgebraicObjects."""

    values: List[AlgebraicObject]

    def __init__(self, values: List[AlgebraicObject]):

        self.values = values

    # TODO: Functions.

    def simplify(self) -> AlgebraicObject:

        """Simplify the algebraic object. This will expand all factored 
        polynomials and simplify all sums. Rational expressions will be
        individually factored and then simplified."""

        # Simplify the values individually.
        simplified_values = []
        for value in self.values:
            simplified_values.append(value.simplify())

        # Combine like terms.
        like_terms: LikeTermsDict
        
        # TODO: Finish.

    def factor(self) -> AlgebraicObject:

        """Factor the algebraic object. This will factor all polynomials
        and rational expressions without simplifying them."""

        return self

    def evaluate(self, symbols: dict) -> float:

        """Evaluate the algebraic object. This requires a dict of symbols, 
        which uses the name of the symbol as the key and its float value
        as the value. Returns the final floating point result."""

        # Evaluate the values individually.
        value = 0
        for value in self.values:
            value += value.evaluate(symbols)

        return value


class QuotientType(AlgebraicObject):

    """The quotient type algebraic object. The quotient type represents a
    quotient of AlgebraicObjects."""

    a: AlgebraicObject
    b: AlgebraicObject

    def __init__(self, a: AlgebraicObject, b: AlgebraicObject):

        self.a = a
        self.b = b

    # TODO: Functions.

    def simplify(self) -> AlgebraicObject:

        """Simplify the algebraic object. This will expand all factored 
        polynomials and simplify all sums. Rational expressions will be
        individually factored and then simplified."""
        
        # TODO: Finish.

    def factor(self) -> AlgebraicObject:

        """Factor the algebraic object. This will factor all polynomials
        and rational expressions without simplifying them."""

        return self

    def evaluate(self, symbols: dict) -> float:

        """Evaluate the algebraic object. This requires a dict of symbols, 
        which uses the name of the symbol as the key and its float value
        as the value. Returns the final floating point result."""

        # Evaluate the values individually.
        return self.a.evaluate(symbols) / self.b.evaluate(symbols)


class PowType(AlgebraicObject):

    """The power type algebraic object. The power type represents a
    power of AlgebraicObjects."""

    a: AlgebraicObject
    b: AlgebraicObject

    def __init__(self, a: AlgebraicObject, b: AlgebraicObject):

        self.a = a
        self.b = b

    # TODO: Functions.

    def simplify(self) -> AlgebraicObject:

        """Simplify the algebraic object. This will expand all factored 
        polynomials and simplify all sums. Rational expressions will be
        individually factored and then simplified."""
        
        # TODO: Finish.

    def factor(self) -> AlgebraicObject:

        """Factor the algebraic object. This will factor all polynomials
        and rational expressions without simplifying them."""

        return self

    def evaluate(self, symbols: dict) -> float:

        """Evaluate the algebraic object. This requires a dict of symbols, 
        which uses the name of the symbol as the key and its float value
        as the value. Returns the final floating point result."""

        # Evaluate the values individually.
        return self.a.evaluate(symbols) ** self.b.evaluate(symbols)