
# TruthLatch Registry Integration Guide

## Purpose
The registry stores validated verification responses and
retrieves them by verification ID.

## Initialise
Create one shared instance when the application starts:

    registry = Registry()

## Register a result

    registry.register(result)

Accepts a dictionary or VerificationResponse model.
Returns a copy of the registered VerificationResponse.

Raises:
- ValueError for malformed results or invalid IDs.
- DuplicateVerificationError for an existing ID.

## Look up a result

    result = registry.lookup(verification_id)

Returns a VerificationResponse copy when found,
or None when the ID is not registered.

Raises ValueError for an invalid ID.

## Count records

    count = len(registry)

## Run tests

    python3 -m unittest tests.test_registry -v

## Limitations
The registry is in-memory and is not persistent.
Records are lost when the application restarts.
Separate application processes do not share records.
