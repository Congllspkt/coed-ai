The `truncatedTo()` method is a powerful utility within Java 8's Date and Time API (`java.time` package) that allows you to reduce the precision of a temporal object by setting all smaller units to their minimum valid values (typically zero). It's essentially a "floor" operation on the time components.

---

# The `truncatedTo()` method in Java 8

## 1. Introduction

The `truncatedTo()` method is part of the `java.time.temporal.Temporal` interface, which is implemented by many of the core date-time classes in Java 8, such as `Instant`, `LocalDateTime`, `ZonedDateTime`, `LocalTime`, and `OffsetDateTime`.

Its primary purpose is to return a copy of the temporal object with the time truncated to the specified unit. This means that all fields finer than the specified unit will be set to their minimum possible value, which is usually zero (e.g., seconds, milliseconds, microseconds, nanoseconds).

## 2. Applicable Classes

You'll find the `truncatedTo()` method on the following common `java.time` classes:

*   `java.time.Instant`
*   `java.time.LocalDateTime`
*   `java.time.ZonedDateTime`
*   `java.time.LocalTime`
*   `java.time.OffsetDateTime`
*   `java.time.OffsetTime`

**Note:** `LocalDate` does not have a `truncatedTo()` method because it only represents a date (year, month, day) and does not contain time components that can be truncated.

## 3. Method Signature

```java
public T truncatedTo(java.time.temporal.TemporalUnit unit)
```

*   `T`: Represents the type of the temporal object on which the method is called. For instance, if you call it on a `LocalDateTime`, it will return a `LocalDateTime`.
*   `unit`: A `TemporalUnit` enum representing the unit to which the temporal object should be truncated. The most common implementation of `TemporalUnit` is `java.time.temporal.ChronoUnit`.

## 4. Parameters

*   **`unit` (Type: `TemporalUnit`)**: This parameter specifies the level of precision you want to retain. All units smaller than this specified unit will be set to zero or their minimum equivalent.

    For time-based truncations, you typically use `ChronoUnit` values like:
    *   `ChronoUnit.NANOS` (no change, as it's the finest unit)
    *   `ChronoUnit.MICROS`
    *   `ChronoUnit.MILLIS`
    *   `ChronoUnit.SECONDS`
    *   `ChronoUnit.MINUTES`
    *   `ChronoUnit.HOURS`
    *   `ChronoUnit.HALF_DAYS`
    *   `ChronoUnit.DAYS`

    Units like `WEEKS`, `MONTHS`, `YEARS`, etc., are generally not supported for truncation on time-based objects and will result in an `UnsupportedTemporalTypeException`. Truncation primarily applies to the time components (hour, minute, second, nanosecond). When you truncate to `DAYS`, it means the time part (hour, minute, second, nano) becomes `00:00:00.000000000`.

## 5. Return Value

*   A `T` (a new temporal object of the same type as the original) representing the truncated date-time. The original object remains unchanged as these classes are immutable.

## 6. How it Works (Detailed Explanation)

When you call `truncatedTo(unit)`, the method effectively "floors" the time component of the date-time to the beginning of the specified unit.

Let's take `LocalDateTime` as an example: `2023-10-26T15:34:56.789123456`

*   **`truncatedTo(ChronoUnit.SECONDS)`**:
    *   Sets nanosecond, microsecond, and millisecond fields to `0`.
    *   Result: `2023-10-26T15:34:56.000000000`

*   **`truncatedTo(ChronoUnit.MINUTES)`**:
    *   Sets second, nanosecond, microsecond, and millisecond fields to `0`.
    *   Result: `2023-10-26T15:34:00.000000000`

*   **`truncatedTo(ChronoUnit.HOURS)`**:
    *   Sets minute, second, nanosecond, microsecond, and millisecond fields to `0`.
    *   Result: `2023-10-26T15:00:00.000000000`

*   **`truncatedTo(ChronoUnit.DAYS)`**:
    *   Sets hour, minute, second, nanosecond, microsecond, and millisecond fields to `0`.
    *   Result: `2023-10-26T00:00:00.000000000`

**Key Characteristics:**

*   **No Rounding:** It *truncates*, it does *not* round. Any precision finer than the specified unit is simply discarded (set to zero). For example, `15:59:59` truncated to `HOURS` becomes `15:00:00`, not `16:00:00`.
*   **Immutability:** Like all `java.time` objects, `truncatedTo()` returns a *new* object with the modified value. The original object remains unchanged.
*   **`UnsupportedTemporalTypeException`**: If you provide a `TemporalUnit` that is not supported for truncation by the specific temporal type (e.g., trying to truncate a `LocalDateTime` to `ChronoUnit.MONTHS`), it will throw this exception.

---

## 7. Examples

Let's illustrate with practical Java code examples.

```java
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.Month;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.time.temporal.ChronoUnit;
import java.time.temporal.UnsupportedTemporalTypeException;

public class TruncatedToExample {

    public static void main(String[] args) {

        // --- Example 1: LocalDateTime ---
        System.out.println("--- LocalDateTime Examples ---");
        LocalDateTime originalLDT = LocalDateTime.of(2023, Month.OCTOBER, 26, 15, 34, 56, 789123456);

        System.out.println("Original LocalDateTime: " + originalLDT);
        // Input: 2023-10-26T15:34:56.789123456

        LocalDateTime truncatedToSeconds = originalLDT.truncatedTo(ChronoUnit.SECONDS);
        System.out.println("Truncated to SECONDS:   " + truncatedToSeconds);
        // Output: 2023-10-26T15:34:56

        LocalDateTime truncatedToMinutes = originalLDT.truncatedTo(ChronoUnit.MINUTES);
        System.out.println("Truncated to MINUTES:   " + truncatedToMinutes);
        // Output: 2023-10-26T15:34:00

        LocalDateTime truncatedToHours = originalLDT.truncatedTo(ChronoUnit.HOURS);
        System.out.println("Truncated to HOURS:     " + truncatedToHours);
        // Output: 2023-10-26T15:00:00

        LocalDateTime truncatedToDays = originalLDT.truncatedTo(ChronoUnit.DAYS);
        System.out.println("Truncated to DAYS:      " + truncatedToDays);
        // Output: 2023-10-26T00:00:00

        System.out.println("\n");

        // --- Example 2: Instant ---
        System.out.println("--- Instant Examples ---");
        Instant originalInstant = Instant.parse("2023-10-26T15:34:56.789123456Z");

        System.out.println("Original Instant: " + originalInstant);
        // Input: 2023-10-26T15:34:56.789123456Z

        Instant truncatedInstantToMillis = originalInstant.truncatedTo(ChronoUnit.MILLIS);
        System.out.println("Truncated to MILLIS: " + truncatedInstantToMillis);
        // Output: 2023-10-26T15:34:56.789Z

        Instant truncatedInstantToSeconds = originalInstant.truncatedTo(ChronoUnit.SECONDS);
        System.out.println("Truncated to SECONDS: " + truncatedInstantToSeconds);
        // Output: 2023-10-26T15:34:56Z

        System.out.println("\n");

        // --- Example 3: LocalTime ---
        System.out.println("--- LocalTime Examples ---");
        LocalTime originalLT = LocalTime.of(10, 20, 30, 987654321);

        System.out.println("Original LocalTime: " + originalLT);
        // Input: 10:20:30.987654321

        LocalTime truncatedLTToMinutes = originalLT.truncatedTo(ChronoUnit.MINUTES);
        System.out.println("Truncated to MINUTES: " + truncatedLTToMinutes);
        // Output: 10:20:00

        LocalTime truncatedLTToHours = originalLT.truncatedTo(ChronoUnit.HOURS);
        System.out.println("Truncated to HOURS:   " + truncatedLTToHours);
        // Output: 10:00:00

        System.out.println("\n");

        // --- Example 4: ZonedDateTime ---
        System.out.println("--- ZonedDateTime Example ---");
        ZonedDateTime originalZDT = ZonedDateTime.of(2024, 1, 15, 23, 59, 59, 123456789, ZoneOffset.UTC);

        System.out.println("Original ZonedDateTime: " + originalZDT);
        // Input: 2024-01-15T23:59:59.123456789Z

        ZonedDateTime truncatedZDTToHours = originalZDT.truncatedTo(ChronoUnit.HOURS);
        System.out.println("Truncated to HOURS:     " + truncatedZDTToHours);
        // Output: 2024-01-15T23:00:00Z

        System.out.println("\n");

        // --- Example 5: Unsupported Unit ---
        System.out.println("--- Unsupported Unit Example ---");
        try {
            LocalDateTime willThrowError = originalLDT.truncatedTo(ChronoUnit.MONTHS);
            System.out.println("This line will not be reached: " + willThrowError);
        } catch (UnsupportedTemporalTypeException e) {
            System.out.println("Caught expected exception: " + e.getMessage());
            // Output: Caught expected exception: Unsupported unit: Months
        }
    }
}
```

**Output of the Examples:**

```
--- LocalDateTime Examples ---
Original LocalDateTime: 2023-10-26T15:34:56.789123456
Truncated to SECONDS:   2023-10-26T15:34:56
Truncated to MINUTES:   2023-10-26T15:34:00
Truncated to HOURS:     2023-10-26T15:00:00
Truncated to DAYS:      2023-10-26T00:00:00


--- Instant Examples ---
Original Instant: 2023-10-26T15:34:56.789123456Z
Truncated to MILLIS: 2023-10-26T15:34:56.789Z
Truncated to SECONDS: 2023-10-26T15:34:56Z


--- LocalTime Examples ---
Original LocalTime: 10:20:30.987654321
Truncated to MINUTES: 10:20:00
Truncated to HOURS:   10:00:00


--- ZonedDateTime Example ---
Original ZonedDateTime: 2024-01-15T23:59:59.123456789Z
Truncated to HOURS:     2024-01-15T23:00:00Z


--- Unsupported Unit Example ---
Caught expected exception: Unsupported unit: Months
```