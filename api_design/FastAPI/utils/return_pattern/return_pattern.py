"""
Return Pattern instead of Exception

- use `bind` method if you know the next step could be failed and want to chain something
- use `map` method if you want to return the value of a transformation
"""

from typing import Generic, TypeVar, Optional, Callable
from enum import Enum

T = TypeVar("T")   # success type
E = TypeVar("E")   # error type


# ---- Error Types -----------------------------------------------------------

class ErrorType(Enum):
    NotFound   = "not_found"
    Validation = "validation"
    Conflict   = "conflict"
    Unexpected = "unexpected"


class Error:
    """Rich error object that can carry a type and message."""
    def __init__(self, error_type: ErrorType, message: str):
        self.type = error_type
        self.message = message

    def __repr__(self):
        return f"Error({self.type.value}, {self.message!r})"


# ---- Result Type -----------------------------------------------------------

class Result(Generic[T, E]):
    """Either a success with value T or a failure with error E."""

    __slots__ = ("_value", "_error", "_is_success")

    def __init__(self, is_success: bool,
                 value: Optional[T] = None,
                 error: Optional[E] = None):
        self._is_success = is_success
        self._value = value
        self._error = error
        if is_success and error is not None:
            raise ValueError("Success result cannot have an error.")
        if not is_success and value is not None:
            raise ValueError("Failure result cannot have a value.")

    @staticmethod
    def Ok(value: T) -> "Result[T, E]":
        return Result(True, value=value)

    @staticmethod
    def Err(error: E) -> "Result[T, E]":
        return Result(False, error=error)

    @property
    def is_success(self) -> bool: return self._is_success
    @property
    def is_failure(self) -> bool: return not self._is_success

    @property
    def value(self) -> T:
        if not self._is_success:
            raise ValueError("No value in a failure result.")
        return self._value  # type: ignore

    @property
    def error(self) -> E:
        if self._is_success:
            raise ValueError("No error in a success result.")
        return self._error  # type: ignore

    def map(self, fn: Callable[[T], T]) -> "Result[T, E]":
        """Transform value if success; propagate error."""

        if self.is_success:
            try:
                return Result.Ok(fn(self._value))  # type: ignore
            except Exception as exc:
                return Result.Err(Error(ErrorType.Unexpected, str(exc)))  # type: ignore
        return Result.Err(self._error)  # type: ignore

    def bind(self, fn: Callable[[T], "Result[T, E]"]) -> "Result[T, E]":
        """Chain another Result-returning operation."""

        if self.is_failure:
            return Result.Err(self._error)  # type: ignore
        try:
            return fn(self._value)  # type: ignore
        except Exception as exc:
            return Result.Err(Error(ErrorType.Unexpected, str(exc)))  # type: ignore

    def __repr__(self):
        return f"Result.Ok({self._value!r})" if self.is_success \
               else f"Result.Err({self._error!r})"



"""
# How to use this Result Pattern:

# from result_pattern import Result, Error, ErrorType

# - Goal: validat the age -> fetch the usr -> build a profile string
class User:
    def __init__(self, username: str, age: int):
        self.username = username
        self.age = age

def validate_age(age: int) -> Result[int, Error]:
    if age < 0:
        return Result.Err(Error(ErrorType.Validation, "Age must be non-negative"))
    return Result.Ok(age)

def get_user_from_db(user_id: int) -> Result[User, Error]:
    fake_db = {1: User("alice", 30), 2: User("bob", 25)}
    if user_id not in fake_db:
        return Result.Err(Error(ErrorType.NotFound, f"User {user_id} not found"))
    return Result.Ok(fake_db[user_id])

def create_user_profile(user_id: int, input_age: int) -> Result[str, Error]:
    return (
        validate_age(input_age)
        .bind(lambda valid_age: get_user_from_db(user_id)
              .map(lambda user: f"User: {user.username}, age: {valid_age}"))
    )


# - Main execution
print(create_user_profile(1, 25))
# -> Result.Ok('User: alice, age: 25')

print(create_user_profile(3, -5))
# -> Result.Err(Error(validation, 'Age must be non-negative'))

"""