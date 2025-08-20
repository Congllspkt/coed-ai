The Java 8 Date and Time API (`java.time` package) revolutionized date and time handling, making it immutable, thread-safe, and much clearer than the old `java.util.Date` and `Calendar` classes.

Three fundamental types of methods you'll frequently use are:

1.  **`getXxx()`**: For retrieving specific components of a date or time (e.g., year, month, day, hour).
2.  **`plusXxx()`**: For adding units of time to a date or time object.
3.  **`minusXxx()`**: For subtracting units of time from a date or time object.

A crucial concept for `plusXxx()` and `minusXxx()` methods is **immutability**. These methods **do not modify the original object**. Instead, they return a *new* `Date-Time` object with the modification applied.

Let's dive into each category with examples.

---

## 1. `getXxx()` Methods

`getXxx()` methods are used to extract specific parts or components from a `LocalDate`, `LocalTime`, `LocalDateTime`, `ZonedDateTime`, or `Instant` object.

### Purpose
To retrieve individual fields like year, month, day, hour, minute, second, day of the week, etc.

### Common `getXxx()` Methods

*   **For `LocalDate`:**
    *   `getYear()`: Returns the year (e.g., 2023).
    *   `getMonth()`: Returns the `Month` enum (e.g., `Month.JANUARY`).
    *   `getMonthValue()`: Returns the month as an `int` (1-12).
    *   `getDayOfMonth()`: Returns the day of the month (1-31).
    *   `getDayOfYear()`: Returns the day of the year (1-366).
    *   `getDayOfWeek()`: Returns the `DayOfWeek` enum (e.g., `DayOfWeek.MONDAY`).
*   **For `LocalTime`:**
    *   `getHour()`: Returns the hour (0-23).
    *   `getMinute()`: Returns the minute (0-59).
    *   `getSecond()`: Returns the second (0-59).
    *   `getNano()`: Returns the nanosecond (0-999,999,999).
*   **For `LocalDateTime` & `ZonedDateTime`:** These objects combine date and time components, so they will have all the `get` methods from both `LocalDate` and `LocalTime`.
*   **Generic `get(TemporalField)`:** For more advanced or generic field retrieval, you can use `get(TemporalField field)`. `ChronoField` is a common implementation of `TemporalField`.

### Example: `getXxx()`

```java
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.LocalDateTime;
import java.time.Month;
import java.time.DayOfWeek;
import java.time.temporal.ChronoField;

public class GetMethodsExample {

    public static void main(String[] args) {

        System.out.println("--- getXxx() Methods Example ---");

        // Input: A specific date and time
        LocalDate specificDate = LocalDate.of(2023, 10, 26);
        LocalTime specificTime = LocalTime.of(14, 35, 50, 123456789);
        LocalDateTime specificDateTime = LocalDateTime.of(2024, 2, 29, 9, 15, 30, 456789000);

        System.out.println("\nInput LocalDate: " + specificDate);
        System.out.println("Input LocalTime: " + specificTime);
        System.out.println("Input LocalDateTime: " + specificDateTime);

        // --- Output for LocalDate ---
        System.out.println("\n--- Output for LocalDate ---");
        System.out.println("Year: " + specificDate.getYear());
        System.out.println("Month (enum): " + specificDate.getMonth());
        System.out.println("Month (value): " + specificDate.getMonthValue());
        System.out.println("Day of Month: " + specificDate.getDayOfMonth());
        System.out.println("Day of Year: " + specificDate.getDayOfYear());
        System.out.println("Day of Week: " + specificDate.getDayOfWeek());
        System.out.println("Week of Year (using ChronoField): " + specificDate.get(ChronoField.ALIGNED_WEEK_OF_YEAR)); // Example of generic get

        // --- Output for LocalTime ---
        System.out.println("\n--- Output for LocalTime ---");
        System.out.println("Hour: " + specificTime.getHour());
        System.out.println("Minute: " + specificTime.getMinute());
        System.out.println("Second: " + specificTime.getSecond());
        System.out.println("Nano: " + specificTime.getNano());

        // --- Output for LocalDateTime ---
        System.out.println("\n--- Output for LocalDateTime ---");
        System.out.println("Year: " + specificDateTime.getYear());
        System.out.println("Month: " + specificDateTime.getMonth());
        System.out.println("Day of Month: " + specificDateTime.getDayOfMonth());
        System.out.println("Hour: " + specificDateTime.getHour());
        System.out.println("Minute: " + specificDateTime.getMinute());
        System.out.println("Second: " + specificDateTime.getSecond());
    }
}
```

**Input:**
```
A specific date: 2023-10-26
A specific time: 14:35:50.123456789
A specific date-time: 2024-02-29T09:15:30.456789
```

**Output:**
```
--- getXxx() Methods Example ---

Input LocalDate: 2023-10-26
Input LocalTime: 14:35:50.123456789
Input LocalDateTime: 2024-02-29T09:15:30.456789

--- Output for LocalDate ---
Year: 2023
Month (enum): OCTOBER
Month (value): 10
Day of Month: 26
Day of Year: 299
Day of Week: THURSDAY
Week of Year (using ChronoField): 43

--- Output for LocalTime ---
Hour: 14
Minute: 35
Second: 50
Nano: 123456789

--- Output for LocalDateTime ---
Year: 2024
Month: FEBRUARY
Day of Month: 29
Hour: 9
Minute: 15
Second: 30
```

---

## 2. `plusXxx()` Methods

`plusXxx()` methods are used to add specific amounts of time to a `LocalDate`, `LocalTime`, `LocalDateTime`, `ZonedDateTime`, or `Instant` object.

### Purpose
To create a new date or time object that is a certain duration or period after the original.

### Key Principle: Immutability
Remember, these methods **do not change the original object**. They return a *new* object representing the modified date/time.

### Common `plusXxx()` Methods
These methods are available on `LocalDate`, `LocalTime`, `LocalDateTime`, etc., relevant to their capabilities:

*   `plusYears(long yearsToAdd)`
*   `plusMonths(long monthsToAdd)`
*   `plusWeeks(long weeksToAdd)`
*   `plusDays(long daysToAdd)`
*   `plusHours(long hoursToAdd)`
*   `plusMinutes(long minutesToAdd)`
*   `plusSeconds(long secondsToAdd)`
*   `plusNanos(long nanosToAdd)`

### Generic `plus(long amountToAdd, TemporalUnit unit)`
For more flexibility, you can use `plus(long amountToAdd, TemporalUnit unit)`. `ChronoUnit` is the standard implementation of `TemporalUnit`. This allows you to add any unit (days, hours, minutes, etc.) in a generic way.

### Generic `plus(TemporalAmount amount)`
You can also add `Period` (for date-based amounts like years, months, days) or `Duration` (for time-based amounts like hours, minutes, seconds, nanos).

### Example: `plusXxx()`

```java
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.LocalDateTime;
import java.time.Period;
import java.time.Duration;
import java.time.temporal.ChronoUnit;

public class PlusMethodsExample {

    public static void main(String[] args) {

        System.out.println("--- plusXxx() Methods Example ---");

        // Input: Initial date and time objects
        LocalDate startDate = LocalDate.of(2023, 1, 15);
        LocalTime startTime = LocalTime.of(10, 30, 0);
        LocalDateTime startDateTime = LocalDateTime.of(2023, 10, 26, 14, 0, 0);

        System.out.println("\nInitial LocalDate: " + startDate);
        System.out.println("Initial LocalTime: " + startTime);
        System.out.println("Initial LocalDateTime: " + startDateTime);

        // --- Output for LocalDate.plusXxx() ---
        System.out.println("\n--- Output for LocalDate.plusXxx() ---");
        LocalDate dateAfter3Years = startDate.plusYears(3);
        System.out.println("After 3 years: " + dateAfter3Years); // Original startDate is unchanged

        LocalDate dateAfter2Months = startDate.plusMonths(2);
        System.out.println("After 2 months: " + dateAfter2Months);

        LocalDate dateAfter1Week = startDate.plusWeeks(1);
        System.out.println("After 1 week: " + dateAfter1Week);

        LocalDate dateAfter10Days = startDate.plusDays(10);
        System.out.println("After 10 days: " + dateAfter10Days);

        // Using generic plus(long amount, TemporalUnit unit)
        LocalDate dateAfter50DaysChrono = startDate.plus(50, ChronoUnit.DAYS);
        System.out.println("After 50 days (ChronoUnit): " + dateAfter50DaysChrono);

        // Using generic plus(TemporalAmount amount) with Period
        LocalDate dateAfterPeriod = startDate.plus(Period.ofYears(1).plusMonths(3));
        System.out.println("After 1 year and 3 months (Period): " + dateAfterPeriod);

        // --- Output for LocalTime.plusXxx() ---
        System.out.println("\n--- Output for LocalTime.plusXxx() ---");
        LocalTime timeAfter2Hours = startTime.plusHours(2);
        System.out.println("After 2 hours: " + timeAfter2Hours);

        LocalTime timeAfter15Minutes = startTime.plusMinutes(15);
        System.out.println("After 15 minutes: " + timeAfter15Minutes);

        LocalTime timeAfter30Seconds = startTime.plusSeconds(30);
        System.out.println("After 30 seconds: " + timeAfter30Seconds);

        LocalTime timeAfter500Nanos = startTime.plusNanos(500);
        System.out.println("After 500 nanos: " + timeAfter500Nanos);

        // Using generic plus(long amount, TemporalUnit unit)
        LocalTime timeAfter90MinutesChrono = startTime.plus(90, ChronoUnit.MINUTES);
        System.out.println("After 90 minutes (ChronoUnit): " + timeAfter90MinutesChrono);

        // Using generic plus(TemporalAmount amount) with Duration
        LocalTime timeAfterDuration = startTime.plus(Duration.ofHours(1).plusMinutes(45));
        System.out.println("After 1 hour 45 minutes (Duration): " + timeAfterDuration);

        // --- Output for LocalDateTime.plusXxx() ---
        System.out.println("\n--- Output for LocalDateTime.plusXxx() ---");
        LocalDateTime dateTimeAfter1Year2Days = startDateTime.plusYears(1).plusDays(2); // Chaining methods
        System.out.println("After 1 year and 2 days: " + dateTimeAfter1Year2Days);

        LocalDateTime dateTimeAfter8Hours30Mins = startDateTime.plusHours(8).plusMinutes(30);
        System.out.println("After 8 hours and 30 minutes: " + dateTimeAfter8Hours30Mins);

        // Original objects remain unchanged
        System.out.println("\nOriginal LocalDate (unchanged): " + startDate);
        System.out.println("Original LocalTime (unchanged): " + startTime);
        System.out.println("Original LocalDateTime (unchanged): " + startDateTime);
    }
}
```

**Input:**
```
Initial LocalDate: 2023-01-15
Initial LocalTime: 10:30
Initial LocalDateTime: 2023-10-26T14:00
```

**Output:**
```
--- plusXxx() Methods Example ---

Initial LocalDate: 2023-01-15
Initial LocalTime: 10:30
Initial LocalDateTime: 2023-10-26T14:00

--- Output for LocalDate.plusXxx() ---
After 3 years: 2026-01-15
After 2 months: 2023-03-15
After 1 week: 2023-01-22
After 10 days: 2023-01-25
After 50 days (ChronoUnit): 2023-03-06
After 1 year and 3 months (Period): 2024-04-15

--- Output for LocalTime.plusXxx() ---
After 2 hours: 12:30
After 15 minutes: 10:45
After 30 seconds: 10:30:30
After 500 nanos: 10:30:00.000000500
After 90 minutes (ChronoUnit): 12:00
After 1 hour 45 minutes (Duration): 12:15

--- Output for LocalDateTime.plusXxx() ---
After 1 year and 2 days: 2024-10-28T14:00
After 8 hours and 30 minutes: 2023-10-26T22:30

Original LocalDate (unchanged): 2023-01-15
Original LocalTime (unchanged): 10:30
Original LocalDateTime (unchanged): 2023-10-26T14:00
```

---

## 3. `minusXxx()` Methods

`minusXxx()` methods are used to subtract specific amounts of time from a `LocalDate`, `LocalTime`, `LocalDateTime`, `ZonedDateTime`, or `Instant` object.

### Purpose
To create a new date or time object that is a certain duration or period before the original.

### Key Principle: Immutability
Just like `plusXxx()` methods, `minusXxx()` methods **do not modify the original object**. They return a *new* object representing the modified date/time.

### Common `minusXxx()` Methods
These methods mirror the `plusXxx()` methods:

*   `minusYears(long yearsToSubtract)`
*   `minusMonths(long monthsToSubtract)`
*   `minusWeeks(long weeksToSubtract)`
*   `minusDays(long daysToSubtract)`
*   `minusHours(long hoursToSubtract)`
*   `minusMinutes(long minutesToSubtract)`
*   `minusSeconds(long secondsToSubtract)`
*   `minusNanos(long nanosToSubtract)`

### Generic `minus(long amountToSubtract, TemporalUnit unit)`
Allows generic subtraction using `ChronoUnit`.

### Generic `minus(TemporalAmount amount)`
Allows subtraction using `Period` or `Duration`.

### Example: `minusXxx()`

```java
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.LocalDateTime;
import java.time.Period;
import java.time.Duration;
import java.time.temporal.ChronoUnit;

public class MinusMethodsExample {

    public static void main(String[] args) {

        System.out.println("--- minusXxx() Methods Example ---");

        // Input: Initial date and time objects
        LocalDate startDate = LocalDate.of(2024, 5, 20);
        LocalTime startTime = LocalTime.of(18, 0, 0);
        LocalDateTime startDateTime = LocalDateTime.of(2024, 3, 15, 12, 0, 0);

        System.out.println("\nInitial LocalDate: " + startDate);
        System.out.println("Initial LocalTime: " + startTime);
        System.out.println("Initial LocalDateTime: " + startDateTime);

        // --- Output for LocalDate.minusXxx() ---
        System.out.println("\n--- Output for LocalDate.minusXxx() ---");
        LocalDate dateBefore2Years = startDate.minusYears(2);
        System.out.println("Before 2 years: " + dateBefore2Years);

        LocalDate dateBefore1Month = startDate.minusMonths(1);
        System.out.println("Before 1 month: " + dateBefore1Month);

        LocalDate dateBefore3Weeks = startDate.minusWeeks(3);
        System.out.println("Before 3 weeks: " + dateBefore3Weeks);

        LocalDate dateBefore7Days = startDate.minusDays(7);
        System.out.println("Before 7 days: " + dateBefore7Days);

        // Using generic minus(long amount, TemporalUnit unit)
        LocalDate dateBefore60DaysChrono = startDate.minus(60, ChronoUnit.DAYS);
        System.out.println("Before 60 days (ChronoUnit): " + dateBefore60DaysChrono);

        // Using generic minus(TemporalAmount amount) with Period
        LocalDate dateBeforePeriod = startDate.minus(Period.ofYears(1).plusMonths(2));
        System.out.println("Before 1 year and 2 months (Period): " + dateBeforePeriod);

        // --- Output for LocalTime.minusXxx() ---
        System.out.println("\n--- Output for LocalTime.minusXxx() ---");
        LocalTime timeBefore3Hours = startTime.minusHours(3);
        System.out.println("Before 3 hours: " + timeBefore3Hours);

        LocalTime timeBefore45Minutes = startTime.minusMinutes(45);
        System.out.println("Before 45 minutes: " + timeBefore45Minutes);

        LocalTime timeBefore10Seconds = startTime.minusSeconds(10);
        System.out.println("Before 10 seconds: " + timeBefore10Seconds);

        // Using generic minus(long amount, TemporalUnit unit)
        LocalTime timeBefore120MinutesChrono = startTime.minus(120, ChronoUnit.MINUTES);
        System.out.println("Before 120 minutes (ChronoUnit): " + timeBefore120MinutesChrono);

        // Using generic minus(TemporalAmount amount) with Duration
        LocalTime timeBeforeDuration = startTime.minus(Duration.ofHours(2).plusSeconds(30));
        System.out.println("Before 2 hours 30 seconds (Duration): " + timeBeforeDuration);

        // --- Output for LocalDateTime.minusXxx() ---
        System.out.println("\n--- Output for LocalDateTime.minusXxx() ---");
        LocalDateTime dateTimeBefore6Months4Days = startDateTime.minusMonths(6).minusDays(4); // Chaining
        System.out.println("Before 6 months and 4 days: " + dateTimeBefore6Months4Days);

        LocalDateTime dateTimeBefore1Hour15Mins = startDateTime.minusHours(1).minusMinutes(15);
        System.out.println("Before 1 hour and 15 minutes: " + dateTimeBefore1Hour15Mins);

        // Original objects remain unchanged
        System.out.println("\nOriginal LocalDate (unchanged): " + startDate);
        System.out.println("Original LocalTime (unchanged): " + startTime);
        System.out.println("Original LocalDateTime (unchanged): " + startDateTime);
    }
}
```

**Input:**
```
Initial LocalDate: 2024-05-20
Initial LocalTime: 18:00
Initial LocalDateTime: 2024-03-15T12:00
```

**Output:**
```
--- minusXxx() Methods Example ---

Initial LocalDate: 2024-05-20
Initial LocalTime: 18:00
Initial LocalDateTime: 2024-03-15T12:00

--- Output for LocalDate.minusXxx() ---
Before 2 years: 2022-05-20
Before 1 month: 2024-04-20
Before 3 weeks: 2024-04-29
Before 7 days: 2024-05-13
Before 60 days (ChronoUnit): 2024-03-21
Before 1 year and 2 months (Period): 2023-03-20

--- Output for LocalTime.minusXxx() ---
Before 3 hours: 15:00
Before 45 minutes: 17:15
Before 10 seconds: 17:59:50
Before 120 minutes (ChronoUnit): 16:00
Before 2 hours 30 seconds (Duration): 15:59:30

--- Output for LocalDateTime.minusXxx() ---
Before 6 months and 4 days: 2023-09-11T12:00
Before 1 hour and 15 minutes: 2024-03-15T10:45

Original LocalDate (unchanged): 2024-05-20
Original LocalTime (unchanged): 18:00
Original LocalDateTime (unchanged): 2024-03-15T12:00
```

---

## Important Considerations

1.  **Immutability:** This is the most crucial concept. Always remember that `plusXxx()` and `minusXxx()` methods return *new* objects. If you forget to assign the result to a variable, your date/time object will not change.
    ```java
    LocalDate date = LocalDate.of(2023, 1, 1);
    date.plusDays(10); // This result is discarded! 'date' is still 2023-01-01
    System.out.println(date); // Output: 2023-01-01

    LocalDate newDate = date.plusDays(10); // Correct way to use it
    System.out.println(newDate); // Output: 2023-01-11
    ```
2.  **`TemporalUnit` and `ChronoUnit`:**
    *   `TemporalUnit` is an interface for a unit of date-time, like "days" or "hours".
    *   `ChronoUnit` is an enum that implements `TemporalUnit` and provides a comprehensive set of standard units: `YEARS`, `MONTHS`, `WEEKS`, `DAYS`, `HOURS`, `MINUTES`, `SECONDS`, `MILLIS`, `MICROS`, `NANOS`, `DECADES`, `CENTURIES`, `MILLENNIA`, `ERAS`.
3.  **`Duration` vs. `Period`:**
    *   **`Period`**: Represents a quantity of time in terms of years, months, and days. It's suitable for human-scale durations (e.g., "3 years, 2 months, and 5 days"). It handles date-specific rules like leap years and varying month lengths.
    *   **`Duration`**: Represents a quantity of time in terms of hours, minutes, seconds, and nanoseconds. It's suitable for machine-scale or precise time differences (e.g., "2 hours, 30 minutes, 15 seconds").
    *   Use `plus(Period)` or `minus(Period)` for `LocalDate` and `LocalDateTime` when dealing with year/month/day adjustments.
    *   Use `plus(Duration)` or `minus(Duration)` for `LocalTime`, `LocalDateTime`, and `Instant` when dealing with hour/minute/second/nano adjustments.
4.  **Method Chaining:** The immutability and consistent return types (the new modified object) allow for elegant method chaining:
    ```java
    LocalDateTime futureDateTime = LocalDateTime.now()
                                                .plusYears(1)
                                                .plusMonths(2)
                                                .minusHours(5)
                                                .plusSeconds(30);
    ```

The Java 8 Date and Time API provides a powerful and intuitive way to handle dates and times, and mastering `get`, `plus`, and `minus` methods is fundamental to using it effectively.