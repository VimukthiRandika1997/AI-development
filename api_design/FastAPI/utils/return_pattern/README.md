# Result Pattern

- Instead of using native Exceptions, we could use this kind of pattern to handle the results of the operations

- Suppose you have a function that might fail (e.g. parsing, database lookup, etc.), Instead of raising, you return a Result.

```python
class User:
    def __init__(self, username: str, age: int):
        self.username = username
        self.age = age

def validate_age(age: int) -> Result[int, str]:
    if age < 0:
        return Result.Err("Age must be non-negative")
    return Result.Ok(age)

def get_user_from_db(user_id: int) -> Result[User, str]:
    # pretend database lookup
    fake_db = {1: User("alice", 30), 2: User("bob", 25)}
    if user_id not in fake_db:
        return Result.Err(f"User with id {user_id} not found")
    return Result.Ok(fake_db[user_id])

def create_user_profile(user_id: int, input_age: int) -> Result[str, str]:
    # First, validate the input age
    return validate_age(input_age).bind(lambda valid_age:
        # Then get the user
        get_user_from_db(user_id).bind(lambda user:
            # Do something with user and valid_age
            Result.Ok(f"User: {user.username}, age: {valid_age}")
        )
    )

# Usage:

res = create_user_profile(1, 20)
if res.is_success:
    print("Success:", res.value)
else:
    print("Failure:", res.error)

res2 = create_user_profile(3, -5)
# Maybe prints "Failure: Age must be non-negative" (validate fails first)
print(res2)

```

## Feature

| Feature          | **map**                                | **bind**                                          |
| ---------------- | -------------------------------------- | ------------------------------------------------- |
| Function returns | **plain value** `U`                    | **Result** `Result[U, E]`                         |
| Nesting          | Wraps automatically in `Result.Ok`     | Does **not** wrap again (avoids `Result[Result]`) |
| Purpose          | Simple transformation of success value | Chain another fallible operation                  |

## Pros and Cons of this approach

### Pros

- Explicit error handling: callers know a function may fail by reading its return type (in type hints).
- Avoid exceptions for control flow, which can improve performance (exceptions are relatively expensive in many languages).
- Easier to chain operations (with bind / map) in a functional style.
- Better testing: you don’t need to assert exceptions but can assert on return values.

### Cons / caveats in Python

- **Verbosity**: you must wrap many functions to return Result rather than letting exceptions bubble.
- **Mixing exceptions and results**: many libraries you call might still throw exceptions (I/O errors, network errors, etc.). You’ll need to catch those and convert to Result.Err or let them propagate.
- **Type hints but not enforce**d: Python is dynamically typed, so your “Result[T, E]” is only as strong as your discipline and optional static checking (e.g. with mypy).
- **Unwrapping mistakes**: you might accidentally call .value on a failure result, which raises a runtime error; you need to guard properly.