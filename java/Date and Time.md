This guide will provide a detailed explanation of handling dates and times in Java, covering both the legacy API (`java.util.*`) and the modern, recommended `java.time` API (introduced in Java 8), complete with examples demonstrating input and output.

---

# Date and Time in Java

## Table of Contents

1.  [Introduction](#1-introduction)
2.  [Legacy Date and Time API (Pre-Java 8)](#2-legacy-date-and-time-api-pre-java-8)
    *   `java.util.Date`
    *   `java.util.Calendar`
    *   Why avoid them?
3.  [Modern Date and Time API (`java.time` - Java 8+)](#3-modern-date-and-time-api-javatime---java-8)
    *   Key Advantages
    *   Core Classes
        *   `LocalDate`
        *   `LocalTime`
        *   `LocalDateTime`
        *   `Instant`
        *   `ZonedDateTime`
        *   `Duration`
        *   `Period`
        *   `ZoneId` and `ZoneOffset`
    *   Formatting and Parsing with `DateTimeFormatter`
    *   Converting Between `java.util` and `java.time`
    *   Working with Databases (`java.sql.*` and `java.time`)
4.  [Best Practices](#4-best-practices)

---

## 1. Introduction

Handling dates and times is a common task in software development, but it's notoriously complex due to time zones, daylight saving changes, leap years, and different cultural formats. Java has evolved its approach to date and time handling significantly.

*   **Legacy API (Java 7 and earlier):** Primarily `java.util.Date` and `java.util.Calendar`. These APIs are known for their design flaws, mutability, and thread-safety issues.
*   **Modern API (Java 8 and later):** The `java.time` package (JSR-310) provides a robust, immutable, and thread-safe API that addresses the shortcomings of the legacy API. It's heavily inspired by Joda-Time.

**It is highly recommended to use the `java.time` API for all new development.**

---

## 2. Legacy Date and Time API (Pre-Java 8)

While largely deprecated in favor of `java.time`, it's important to understand the legacy APIs for working with older codebases.

### `java.util.Date`

Represents a specific instant in time, with millisecond precision. It's mutable and not timezone-aware in a meaningful way (its `toString()` uses the JVM's default timezone, but the underlying value is milliseconds since the epoch).

**Example: Basic `Date` Usage**

```java
import java.util.Date;

public class LegacyDateExample {
    public static void main(String[] args) {
        // 1. Get current date and time
        Date currentDate = new Date();
        System.out.println("--- java.util.Date Example ---");
        System.out.println("Current Date (Raw): " + currentDate);

        // 2. Get time in milliseconds since epoch (January 1, 1970, 00:00:00 GMT)
        long milliseconds = currentDate.getTime();
        System.out.println("Milliseconds since epoch: " + milliseconds);

        // 3. Create a Date from milliseconds
        Date epochDate = new Date(0); // Epoch start
        System.out.println("Epoch Start Date: " + epochDate);

        // Input: milliseconds from epoch
        long futureMillis = System.currentTimeMillis() + (1000L * 60 * 60 * 24 * 7); // One week from now
        Date futureDate = new Date(futureMillis);
        System.out.println("Date one week from now: " + futureDate);
    }
}
```

**Output (will vary based on execution time and JVM's default timezone):**

```
--- java.util.Date Example ---
Current Date (Raw): Sun Apr 21 15:30:00 CEST 2024
Milliseconds since epoch: 1713706200000
Epoch Start Date: Thu Jan 01 01:00:00 CET 1970
Date one week from now: Sun Apr 28 15:30:00 CEST 2024
```

### `java.util.Calendar`

A more abstract class for converting between a `Date` object and a set of integer fields (like year, month, day of month, hour). It's also mutable and complex to use.

**Example: Basic `Calendar` Usage**

```java
import java.util.Calendar;
import java.util.Date;

public class LegacyCalendarExample {
    public static void main(String[] args) {
        System.out.println("\n--- java.util.Calendar Example ---");

        // 1. Get a Calendar instance (usually represents current date/time)
        Calendar calendar = Calendar.getInstance();
        System.out.println("Current Calendar Date: " + calendar.getTime()); // Convert to Date for printing

        // 2. Set specific date/time fields
        // Input: Year, Month (0-indexed!), Day, Hour, Minute, Second
        calendar.set(2023, Calendar.DECEMBER, 25, 10, 30, 0); // December is 11, but Calendar.DECEMBER is 11.
        System.out.println("Set Date (Dec 25, 2023 10:30:00): " + calendar.getTime());

        // 3. Add or subtract time
        // Input: Adding days
        calendar.add(Calendar.DAY_OF_MONTH, 10); // Add 10 days
        System.out.println("Date after adding 10 days: " + calendar.getTime());

        // Input: Subtracting months
        calendar.add(Calendar.MONTH, -2); // Subtract 2 months
        System.out.println("Date after subtracting 2 months: " + calendar.getTime());

        // 4. Get specific fields
        System.out.println("Year: " + calendar.get(Calendar.YEAR));
        // Calendar.MONTH is 0-indexed (January is 0)
        System.out.println("Month (0-indexed): " + calendar.get(Calendar.MONTH));
        System.out.println("Day of Month: " + calendar.get(Calendar.DAY_OF_MONTH));
        System.out.println("Hour of Day (24-hour): " + calendar.get(Calendar.HOUR_OF_DAY));
    }
}
```

**Output (will vary based on execution time and JVM's default timezone):**

```
--- java.util.Calendar Example ---
Current Calendar Date: Sun Apr 21 15:30:00 CEST 2024
Set Date (Dec 25, 2023 10:30:00): Mon Dec 25 10:30:00 CET 2023
Date after adding 10 days: Thu Jan 04 10:30:00 CET 2024
Date after subtracting 2 months: Mon Nov 04 10:30:00 CET 2023
Year: 2023
Month (0-indexed): 10
Day of Month: 4
Hour of Day (24-hour): 10
```

### Why avoid them?

*   **Mutability:** `Date` and `Calendar` objects can be changed after creation, leading to unexpected side effects in multi-threaded environments or when objects are shared.
*   **Not Thread-Safe:** Mutability makes them not thread-safe.
*   **Poor Design:**
    *   `Date` represents an instant but its `toString()` and many constructors imply a specific timezone.
    *   `Calendar` has confusing field numbering (e.g., months are 0-indexed).
    *   Lack of clear separation between date, time, and timezone concepts.
    *   Hard to perform complex calculations (e.g., "next Tuesday").

---

## 3. Modern Date and Time API (`java.time` - Java 8+)

The `java.time` package (often called the "JSR-310" API) provides a comprehensive and well-designed set of classes for handling dates and times.

### Key Advantages

*   **Immutability:** All classes in `java.time` are immutable. Operations like adding days return a *new* object, leaving the original unchanged. This makes them inherently thread-safe.
*   **Clear Separation of Concerns:** Distinct classes for date only, time only, date-time without timezone, date-time with timezone, etc.
*   **Fluent API:** Method chaining makes code readable and concise (e.g., `localDate.plusDays(5).minusMonths(1)`).
*   **Improved Clarity:** Field values are more intuitive (e.g., months are 1-12).
*   **Better Performance:** Generally more performant than `Calendar`.
*   **Comprehensive:** Covers a wide range of use cases from simple date arithmetic to complex timezone conversions.

### Core Classes

#### `LocalDate`

Represents a date without time or timezone. (e.g., "2024-04-21")

**Example: `LocalDate`**

```java
import java.time.LocalDate;
import java.time.Month;
import java.time.DayOfWeek;

public class LocalDateExample {
    public static void main(String[] args) {
        System.out.println("--- LocalDate Example ---");

        // 1. Get current date
        LocalDate today = LocalDate.now();
        System.out.println("Today's Date: " + today);
        // Output: Today's Date: 2024-04-21 (assuming current date)

        // 2. Create a specific date
        // Input: Year, Month (enum), Day
        LocalDate independenceDay = LocalDate.of(1776, Month.JULY, 4);
        System.out.println("Independence Day: " + independenceDay);
        // Output: Independence Day: 1776-07-04

        // Input: Year, Month (int), Day
        LocalDate newYear2025 = LocalDate.of(2025, 1, 1);
        System.out.println("New Year 2025: " + newYear2025);
        // Output: New Year 2025: 2025-01-01

        // 3. Parse a date string
        // Input: String "YYYY-MM-DD"
        LocalDate parsedDate = LocalDate.parse("2020-01-20");
        System.out.println("Parsed Date: " + parsedDate);
        // Output: Parsed Date: 2020-01-20

        // 4. Manipulate dates (returns new LocalDate objects)
        LocalDate nextWeek = today.plusWeeks(1);
        System.out.println("Date next week: " + nextWeek);
        // Output: Date next week: 2024-04-28

        LocalDate previousMonth = today.minusMonths(1);
        System.out.println("Date last month: " + previousMonth);
        // Output: Date last month: 2024-03-21

        LocalDate firstDayOfNextYear = today.plusYears(1).withDayOfYear(1);
        System.out.println("First day of next year: " + firstDayOfNextYear);
        // Output: First day of next year: 2025-01-01

        // 5. Get date information
        System.out.println("Year: " + today.getYear());
        System.out.println("Month: " + today.getMonth()); // Enum: APRIL
        System.out.println("Day of Month: " + today.getDayOfMonth());
        System.out.println("Day of Week: " + today.getDayOfWeek()); // Enum: SUNDAY
        System.out.println("Is Leap Year: " + today.isLeapYear());

        // 6. Compare dates
        System.out.println("Is today before parsedDate? " + today.isBefore(parsedDate)); // Output: false
        System.out.println("Is today after newYear2025? " + today.isAfter(newYear2025));  // Output: true
        System.out.println("Is today equal to itself? " + today.isEqual(LocalDate.now())); // Output: true (if called instantly)
    }
}
```

#### `LocalTime`

Represents a time without date or timezone. (e.g., "10:30:45.123")

**Example: `LocalTime`**

```java
import java.time.LocalTime;
import java.time.temporal.ChronoUnit;

public class LocalTimeExample {
    public static void main(String[] args) {
        System.out.println("\n--- LocalTime Example ---");

        // 1. Get current time
        LocalTime now = LocalTime.now();
        System.out.println("Current Time: " + now);
        // Output: Current Time: 15:30:45.123456789 (approx)

        // 2. Create a specific time
        // Input: Hour, Minute, Second, Nanosecond
        LocalTime wakeUpTime = LocalTime.of(7, 0, 0); // 7:00:00
        System.out.println("Wake Up Time: " + wakeUpTime);
        // Output: Wake Up Time: 07:00

        LocalTime meetingTime = LocalTime.of(14, 30, 0, 500_000_000); // 14:30:00.500
        System.out.println("Meeting Time: " + meetingTime);
        // Output: Meeting Time: 14:30:00.500

        // 3. Parse a time string
        // Input: String "HH:MM:SS" or "HH:MM:SS.NNN"
        LocalTime parsedTime = LocalTime.parse("23:59:59");
        System.out.println("Parsed Time: " + parsedTime);
        // Output: Parsed Time: 23:59:59

        // 4. Manipulate times
        LocalTime twoHoursLater = now.plus(2, ChronoUnit.HOURS);
        System.out.println("Two hours later: " + twoHoursLater);

        LocalTime tenMinutesAgo = now.minusMinutes(10);
        System.out.println("Ten minutes ago: " + tenMinutesAgo);

        // 5. Get time information
        System.out.println("Hour: " + now.getHour());
        System.out.println("Minute: " + now.getMinute());
        System.out.println("Second: " + now.getSecond());
        System.out.println("Nanosecond: " + now.getNano());

        // 6. Compare times
        System.out.println("Is wakeUpTime before meetingTime? " + wakeUpTime.isBefore(meetingTime)); // Output: true
        System.out.println("Is now after parsedTime? " + now.isAfter(parsedTime)); // Output: false (if now is afternoon)
    }
}
```

#### `LocalDateTime`

Represents a date and time without timezone information. (e.g., "2024-04-21T15:30:45")

**Example: `LocalDateTime`**

```java
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.Month;

public class LocalDateTimeExample {
    public static void main(String[] args) {
        System.out.println("\n--- LocalDateTime Example ---");

        // 1. Get current date and time
        LocalDateTime currentDateTime = LocalDateTime.now();
        System.out.println("Current DateTime: " + currentDateTime);
        // Output: Current DateTime: 2024-04-21T15:30:45.123456789 (approx)

        // 2. Create a specific date and time
        LocalDateTime christmasEve = LocalDateTime.of(2024, Month.DECEMBER, 24, 20, 0, 0);
        System.out.println("Christmas Eve 2024: " + christmasEve);
        // Output: Christmas Eve 2024: 2024-12-24T20:00

        // 3. Combine LocalDate and LocalTime
        LocalDate date = LocalDate.of(2023, 10, 26);
        LocalTime time = LocalTime.of(9, 15);
        LocalDateTime combinedDateTime = LocalDateTime.of(date, time);
        System.out.println("Combined DateTime: " + combinedDateTime);
        // Output: Combined DateTime: 2023-10-26T09:15

        // 4. Parse a date-time string
        // Input: String "YYYY-MM-DDTHH:MM:SS" (T is standard separator)
        LocalDateTime parsedDateTime = LocalDateTime.parse("2022-05-15T12:00:00");
        System.out.println("Parsed DateTime: " + parsedDateTime);
        // Output: Parsed DateTime: 2022-05-15T12:00:00

        // 5. Manipulate date and time
        LocalDateTime futureDateTime = currentDateTime.plusDays(5).minusHours(3);
        System.out.println("Future DateTime: " + futureDateTime);

        // 6. Extract date and time components
        System.out.println("Date component: " + currentDateTime.toLocalDate());
        System.out.println("Time component: " + currentDateTime.toLocalTime());

        // 7. Compare
        System.out.println("Is currentDateTime before christmasEve? " + currentDateTime.isBefore(christmasEve)); // Output: true
    }
}
```

#### `Instant`

Represents a point in time on the timeline, often used for machine timestamps. It is essentially a numeric timestamp (milliseconds or nanoseconds since the epoch) and is always in UTC.

**Example: `Instant`**

```java
import java.time.Instant;
import java.time.Duration;
import java.time.ZoneId;
import java.time.ZonedDateTime;

public class InstantExample {
    public static void main(String[] args) {
        System.out.println("\n--- Instant Example ---");

        // 1. Get current instant (UTC)
        Instant now = Instant.now();
        System.out.println("Current Instant (UTC): " + now);
        // Output: Current Instant (UTC): 2024-04-21T13:30:45.123456789Z (Z indicates UTC/Zulu time)

        // 2. Create an instant from epoch milliseconds
        // Input: long milliseconds
        Instant fromEpochMilli = Instant.ofEpochMilli(System.currentTimeMillis());
        System.out.println("Instant from epoch millis: " + fromEpochMilli);

        // 3. Get milliseconds/seconds from an Instant
        System.out.println("Epoch Millis from Instant: " + now.toEpochMilli());
        System.out.println("Epoch Seconds from Instant: " + now.getEpochSecond());

        // 4. Manipulate Instant
        Instant fiveMinutesLater = now.plus(Duration.ofMinutes(5));
        System.out.println("Instant five minutes later: " + fiveMinutesLater);

        // 5. Convert Instant to ZonedDateTime (needs a timezone)
        ZonedDateTime zdt = now.atZone(ZoneId.systemDefault());
        System.out.println("Instant converted to ZonedDateTime (system default): " + zdt);
        // Output: Instant converted to ZonedDateTime (system default): 2024-04-21T15:30:45.123456789+02:00[Europe/Berlin]
    }
}
```

#### `ZonedDateTime`

Represents a complete date, time, and timezone. This is crucial for applications that need to deal with different time zones or daylight saving changes accurately.

**Example: `ZonedDateTime`**

```java
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;

public class ZonedDateTimeExample {
    public static void main(String[] args) {
        System.out.println("\n--- ZonedDateTime Example ---");

        // 1. Get current ZonedDateTime (using system default timezone)
        ZonedDateTime nowInSystemZone = ZonedDateTime.now();
        System.out.println("Current ZonedDateTime (System Default): " + nowInSystemZone);
        // Output: Current ZonedDateTime (System Default): 2024-04-21T15:30:45.123456789+02:00[Europe/Berlin]

        // 2. Create a ZonedDateTime for a specific timezone
        ZoneId newYorkZone = ZoneId.of("America/New_York");
        ZonedDateTime nowInNewYork = ZonedDateTime.now(newYorkZone);
        System.out.println("Current ZonedDateTime (New York): " + nowInNewYork);
        // Output: Current ZonedDateTime (New York): 2024-04-21T09:30:45.123456789-04:00[America/New_York]

        // 3. Create ZonedDateTime from LocalDateTime and ZoneId
        LocalDateTime localDT = LocalDateTime.of(2024, 7, 4, 12, 0); // Noon, July 4th, 2024
        ZonedDateTime nyIndependenceDay = ZonedDateTime.of(localDT, newYorkZone);
        System.out.println("NY Independence Day: " + nyIndependenceDay);
        // Output: NY Independence Day: 2024-07-04T12:00-04:00[America/New_York]

        // 4. Convert between time zones (same instant, different representation)
        ZonedDateTime parisTime = nyIndependenceDay.withZoneSameInstant(ZoneId.of("Europe/Paris"));
        System.out.println("Same instant in Paris: " + parisTime);
        // Output: Same instant in Paris: 2024-07-04T18:00+02:00[Europe/Paris]
        // Note: 12 PM in NY (UTC-4) is 6 PM in Paris (UTC+2)

        // 5. Manipulate ZonedDateTime
        ZonedDateTime nextDayInNY = nowInNewYork.plusDays(1);
        System.out.println("Next day in NY: " + nextDayInNY);

        // 6. Format ZonedDateTime
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("EEEE, MMMM dd, yyyy HH:mm zzz");
        System.out.println("Formatted NY time: " + nyIndependenceDay.format(formatter));
        // Output: Formatted NY time: Thursday, July 04, 2024 12:00 EDT
    }
}
```

#### `Duration`

Represents a quantity of time in terms of seconds and nanoseconds, suitable for machine time.

**Example: `Duration`**

```java
import java.time.Duration;
import java.time.Instant;
import java.time.LocalDateTime;

public class DurationExample {
    public static void main(String[] args) {
        System.out.println("\n--- Duration Example ---");

        // 1. Create Durations
        Duration oneHour = Duration.ofHours(1);
        Duration fiveMinutes = Duration.ofMinutes(5);
        Duration tenSeconds = Duration.ofSeconds(10);
        System.out.println("One Hour: " + oneHour);      // Output: PT1H
        System.out.println("Five Minutes: " + fiveMinutes); // Output: PT5M
        System.out.println("Ten Seconds: " + tenSeconds);  // Output: PT10S

        // 2. Calculate duration between two Instants (machine time)
        Instant start = Instant.now();
        // Simulate some work
        try { Thread.sleep(1500); } catch (InterruptedException e) {}
        Instant end = Instant.now();
        Duration timeElapsed = Duration.between(start, end);
        System.out.println("Time elapsed (Instant): " + timeElapsed.toMillis() + " ms");

        // 3. Calculate duration between two LocalTime/LocalDateTime (no timezone effects)
        LocalDateTime startDT = LocalDateTime.of(2024, 4, 21, 9, 0);
        LocalDateTime endDT = LocalDateTime.of(2024, 4, 21, 10, 30);
        Duration meetingLength = Duration.between(startDT, endDT);
        System.out.println("Meeting Length: " + meetingLength.toMinutes() + " minutes");
        // Output: Meeting Length: 90 minutes

        // 4. Manipulate Durations
        Duration totalDuration = oneHour.plus(fiveMinutes).minus(tenSeconds);
        System.out.println("Total Duration: " + totalDuration); // Output: PT1H4M50S
    }
}
```

#### `Period`

Represents a quantity of time in terms of years, months, and days, suitable for human-scale time.

**Example: `Period`**

```java
import java.time.LocalDate;
import java.time.Period;

public class PeriodExample {
    public static void main(String[] args) {
        System.out.println("\n--- Period Example ---");

        // 1. Create Periods
        Period fiveYearsThreeMonthsTwoDays = Period.of(5, 3, 2);
        System.out.println("Period: " + fiveYearsThreeMonthsTwoDays);
        // Output: P5Y3M2D

        Period tenDays = Period.ofDays(10);
        System.out.println("Ten Days: " + tenDays); // Output: P10D

        // 2. Calculate period between two LocalDates
        LocalDate startDate = LocalDate.of(2020, 1, 15);
        LocalDate endDate = LocalDate.of(2024, 4, 21);
        Period age = Period.between(startDate, endDate);
        System.out.println("Years between: " + age.getYears());   // Output: 4
        System.out.println("Months between: " + age.getMonths()); // Output: 3
        System.out.println("Days between: " + age.getDays());     // Output: 6
        System.out.println("Total period: " + age);               // Output: P4Y3M6D

        // 3. Add a Period to a LocalDate
        LocalDate futureDate = LocalDate.now().plus(Period.ofYears(2).plusMonths(1));
        System.out.println("Date in 2 years and 1 month: " + futureDate);
    }
}
```

#### `ZoneId` and `ZoneOffset`

*   **`ZoneId`**: Represents a time-zone ID, e.g., "America/New_York", "Europe/London". It includes rules for daylight saving time.
*   **`ZoneOffset`**: Represents a fixed offset from UTC, e.g., "+02:00", "-05:00". It does not include daylight saving rules.

**Example: `ZoneId` and `ZoneOffset`**

```java
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.util.Set;

public class TimeZoneExample {
    public static void main(String[] args) {
        System.out.println("\n--- ZoneId and ZoneOffset Example ---");

        // 1. Get system default ZoneId
        ZoneId systemDefaultZone = ZoneId.systemDefault();
        System.out.println("System Default Zone: " + systemDefaultZone);
        // Output: System Default Zone: Europe/Berlin (or your local zone)

        // 2. Create ZoneId by ID
        ZoneId newYork = ZoneId.of("America/New_York");
        System.out.println("New York Zone: " + newYork);

        // 3. Get all available zone IDs (can be a large list)
        // Set<String> availableZoneIds = ZoneId.getAvailableZoneIds();
        // System.out.println("Total available zones: " + availableZoneIds.size());
        // availableZoneIds.stream().limit(5).forEach(System.out::println); // Print first 5

        // 4. Create a ZoneOffset
        ZoneOffset offsetPlusTwo = ZoneOffset.ofHours(2);
        System.out.println("Offset +2 hours: " + offsetPlusTwo); // Output: +02:00

        ZoneOffset offsetMinusFive = ZoneOffset.of("-05:00");
        System.out.println("Offset -5 hours: " + offsetMinusFive); // Output: -05:00
    }
}
```

### Formatting and Parsing with `DateTimeFormatter`

`DateTimeFormatter` is the immutable, thread-safe class for formatting and parsing date-time objects.

**Example: `DateTimeFormatter`**

```java
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.FormatStyle;
import java.util.Locale;

public class DateTimeFormatterExample {
    public static void main(String[] args) {
        System.out.println("\n--- DateTimeFormatter Example ---");

        LocalDateTime now = LocalDateTime.now();

        // 1. Using predefined formatters
        String isoDateTime = now.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
        System.out.println("ISO Local DateTime: " + isoDateTime);
        // Output: ISO Local DateTime: 2024-04-21T15:30:45.123456789

        String isoDate = LocalDate.now().format(DateTimeFormatter.ISO_DATE);
        System.out.println("ISO Date: " + isoDate);
        // Output: ISO Date: 2024-04-21

        // 2. Using pattern strings (custom formatting)
        // Input: Pattern string
        DateTimeFormatter customFormatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss a");
        String formattedCustom = now.format(customFormatter);
        System.out.println("Custom Format: " + formattedCustom);
        // Output: Custom Format: 21/04/2024 15:30:45 PM

        // Different pattern for LocalDate
        DateTimeFormatter dayOfWeekFormatter = DateTimeFormatter.ofPattern("EEEE, MMMM dd, yyyy");
        String formattedDate = LocalDate.now().format(dayOfWeekFormatter);
        System.out.println("Date with Day of Week: " + formattedDate);
        // Output: Date with Day of Week: Sunday, April 21, 2024

        // 3. Using locale-specific format styles
        // Input: FormatStyle and Locale
        DateTimeFormatter germanDateFormatter = DateTimeFormatter.ofLocalizedDate(FormatStyle.FULL)
                                                                 .withLocale(Locale.GERMANY);
        String germanDate = LocalDate.now().format(germanDateFormatter);
        System.out.println("German Full Date: " + germanDate);
        // Output: German Full Date: Sonntag, 21. April 2024

        // 4. Parsing strings into date/time objects
        // Input: String and Formatter
        String dateString = "15/08/2023 10:45:00";
        DateTimeFormatter parser = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss");
        LocalDateTime parsed = LocalDateTime.parse(dateString, parser);
        System.out.println("Parsed LocalDateTime: " + parsed);
        // Output: Parsed LocalDateTime: 2023-08-15T10:45:00

        String dateString2 = "2024-02-29"; // Leap year
        LocalDate parsedDate2 = LocalDate.parse(dateString2, DateTimeFormatter.ISO_DATE);
        System.out.println("Parsed LocalDate (ISO): " + parsedDate2);
        // Output: Parsed LocalDate (ISO): 2024-02-29

        // Handling invalid input during parsing
        String invalidDateString = "2023-02-29"; // Not a leap year
        try {
            LocalDate.parse(invalidDateString, DateTimeFormatter.ISO_DATE);
        } catch (java.time.format.DateTimeParseException e) {
            System.err.println("Error parsing invalid date: " + e.getMessage());
            // Output: Error parsing invalid date: Text '2023-02-29' could not be parsed: Invalid date 'February 29' as '2023' is not a leap year
        }
    }
}
```

**Common Pattern Characters:**

| Character | Meaning                  | Example (for 2024-04-21 15:30:05.123) |
| :-------- | :----------------------- | :------------------------------------ |
| `y`       | Year                     | `yy` -> 24, `yyyy` -> 2024            |
| `M`       | Month of year            | `M` -> 4, `MM` -> 04, `MMM` -> Apr, `MMMM` -> April |
| `d`       | Day of month             | `d` -> 21, `dd` -> 21                 |
| `E`       | Day of week              | `E` -> Sun, `EEEE` -> Sunday          |
| `H`       | Hour of day (0-23)       | `H` -> 15, `HH` -> 15                 |
| `h`       | Hour of day (1-12)       | `h` -> 3, `hh` -> 03                  |
| `m`       | Minute of hour           | `m` -> 30, `mm` -> 30                 |
| `s`       | Second of minute         | `s` -> 5, `ss` -> 05                  |
| `S`       | Fraction of second       | `SSS` -> 123                          |
| `a`       | Am/pm marker             | `a` -> PM                             |
| `z`       | Time zone (short)        | `z` -> CEST                           |
| `Z`       | Zone offset/ID           | `Z` -> +0200, `XX` -> +02             |
| `X`       | Zone offset (ISO 8601)   | `X` -> +02, `XXX` -> +02:00           |
| `'text'`  | Literal text             | `'Date:'` -> Date:                    |
| `''`      | Single quote             | `''` -> '                             |

### Converting Between `java.util` and `java.time`

For interoperability with older code or libraries, you might need to convert between the legacy and modern APIs.

**Example: Conversions**

```java
import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.Date;
import java.util.Calendar;

public class ConversionExample {
    public static void main(String[] args) {
        System.out.println("\n--- Conversions between Legacy and Modern API ---");

        // --- java.util.Date to java.time ---
        Date legacyDate = new Date(); // Current date/time
        System.out.println("Original java.util.Date: " + legacyDate);

        // Date -> Instant (preferred)
        Instant instantFromDate = legacyDate.toInstant();
        System.out.println("java.util.Date to Instant: " + instantFromDate);

        // Instant -> LocalDateTime (needs ZoneId to lose timezone info)
        LocalDateTime ldtFromInstant = instantFromDate.atZone(ZoneId.systemDefault()).toLocalDateTime();
        System.out.println("Instant to LocalDateTime (system default): " + ldtFromInstant);

        // Date -> ZonedDateTime (direct conversion)
        ZonedDateTime zdtFromDate = legacyDate.toInstant().atZone(ZoneId.systemDefault());
        System.out.println("java.util.Date to ZonedDateTime: " + zdtFromDate);

        // --- java.time to java.util.Date ---
        LocalDateTime nowLDT = LocalDateTime.now();
        ZonedDateTime nowZDT = ZonedDateTime.now();
        Instant nowInstant = Instant.now();

        // Instant -> Date (preferred)
        Date dateFromInstant = Date.from(nowInstant);
        System.out.println("Instant to java.util.Date: " + dateFromInstant);

        // LocalDateTime -> Date (needs ZoneId to gain timezone info for Instant conversion)
        Date dateFromLDT = Date.from(nowLDT.atZone(ZoneId.systemDefault()).toInstant());
        System.out.println("LocalDateTime to java.util.Date: " + dateFromLDT);

        // ZonedDateTime -> Date
        Date dateFromZDT = Date.from(nowZDT.toInstant());
        System.out.println("ZonedDateTime to java.util.Date: " + dateFromZDT);


        // --- java.util.Calendar to java.time ---
        Calendar legacyCalendar = Calendar.getInstance();
        System.out.println("\nOriginal java.util.Calendar Date: " + legacyCalendar.getTime());

        // Calendar -> Instant (via Calendar.toInstant())
        Instant instantFromCalendar = legacyCalendar.toInstant();
        System.out.println("Calendar to Instant: " + instantFromCalendar);

        // Calendar -> ZonedDateTime (via Instant)
        ZonedDateTime zdtFromCalendar = instantFromCalendar.atZone(ZoneId.systemDefault());
        System.out.println("Calendar to ZonedDateTime: " + zdtFromCalendar);

        // --- java.time to java.util.Calendar ---
        ZonedDateTime newZDT = ZonedDateTime.of(2025, 7, 1, 10, 0, 0, 0, ZoneId.of("Asia/Tokyo"));
        System.out.println("\nOriginal java.time.ZonedDateTime: " + newZDT);

        // ZonedDateTime -> Calendar (via Instant)
        Calendar calendarFromZDT = Calendar.getInstance();
        calendarFromZDT.setTime(Date.from(newZDT.toInstant())); // Date.from is safest
        System.out.println("ZonedDateTime to Calendar: " + calendarFromZDT.getTime());
    }
}
```

### Working with Databases (`java.sql.*` and `java.time`)

The `java.sql` package provides classes like `java.sql.Date`, `java.sql.Time`, and `java.sql.Timestamp` for database interaction. These have `valueOf` and `to*` methods that facilitate direct conversion with `java.time` types.

*   `java.sql.Date` <-> `java.time.LocalDate`
*   `java.sql.Time` <-> `java.time.LocalTime`
*   `java.sql.Timestamp` <-> `java.time.LocalDateTime` or `java.time.Instant`

**Example: Database Conversions**

```java
import java.sql.Date;
import java.sql.Time;
import java.sql.Timestamp;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.LocalDateTime;
import java.time.Instant;

public class SqlDateConversionExample {
    public static void main(String[] args) {
        System.out.println("\n--- Database Date/Time Conversions ---");

        // LocalDate <-> java.sql.Date
        LocalDate localDate = LocalDate.of(2024, 7, 4);
        Date sqlDate = Date.valueOf(localDate); // LocalDate -> java.sql.Date
        System.out.println("LocalDate: " + localDate + " -> java.sql.Date: " + sqlDate);

        LocalDate convertedLocalDate = sqlDate.toLocalDate(); // java.sql.Date -> LocalDate
        System.out.println("java.sql.Date: " + sqlDate + " -> LocalDate: " + convertedLocalDate);

        // LocalTime <-> java.sql.Time
        LocalTime localTime = LocalTime.of(14, 30, 0);
        Time sqlTime = Time.valueOf(localTime); // LocalTime -> java.sql.Time
        System.out.println("LocalTime: " + localTime + " -> java.sql.Time: " + sqlTime);

        LocalTime convertedLocalTime = sqlTime.toLocalTime(); // java.sql.Time -> LocalTime
        System.out.println("java.sql.Time: " + sqlTime + " -> LocalTime: " + convertedLocalTime);

        // LocalDateTime <-> java.sql.Timestamp
        LocalDateTime localDateTime = LocalDateTime.of(2024, 12, 25, 10, 0, 0);
        Timestamp sqlTimestamp = Timestamp.valueOf(localDateTime); // LocalDateTime -> java.sql.Timestamp
        System.out.println("LocalDateTime: " + localDateTime + " -> java.sql.Timestamp: " + sqlTimestamp);

        LocalDateTime convertedLocalDateTime = sqlTimestamp.toLocalDateTime(); // java.sql.Timestamp -> LocalDateTime
        System.out.println("java.sql.Timestamp: " + sqlTimestamp + " -> LocalDateTime: " + convertedLocalDateTime);

        // Instant <-> java.sql.Timestamp (via toInstant() and from(Instant))
        Instant instant = Instant.now();
        Timestamp sqlTimestampFromInstant = Timestamp.from(instant); // Instant -> java.sql.Timestamp
        System.out.println("Instant: " + instant + " -> java.sql.Timestamp: " + sqlTimestampFromInstant);

        Instant convertedInstant = sqlTimestampFromInstant.toInstant(); // java.sql.Timestamp -> Instant
        System.out.println("java.sql.Timestamp: " + sqlTimestampFromInstant + " -> Instant: " + convertedInstant);
    }
}
```

**Output (approximate):**

```
--- Database Date/Time Conversions ---
LocalDate: 2024-07-04 -> java.sql.Date: 2024-07-04
java.sql.Date: 2024-07-04 -> LocalDate: 2024-07-04
LocalTime: 14:30 -> java.sql.Time: 14:30:00
java.sql.Time: 14:30:00 -> LocalTime: 14:30
LocalDateTime: 2024-12-25T10:00 -> java.sql.Timestamp: 2024-12-25 10:00:00.0
java.sql.Timestamp: 2024-12-25 10:00:00.0 -> LocalDateTime: 2024-12-25T10:00
Instant: 2024-04-21T13:30:45.123456789Z -> java.sql.Timestamp: 2024-04-21 15:30:45.123456789
java.sql.Timestamp: 2024-04-21 15:30:45.123456789 -> Instant: 2024-04-21T13:30:45.123456789Z
```
*Note: The `Timestamp` output might show your local time, but the underlying `Instant` is UTC.*

---

## 4. Best Practices

1.  **Always use `java.time` for new code.** Avoid `java.util.Date` and `java.util.Calendar` unless you absolutely have to interact with a legacy API that still requires them.
2.  **Be explicit about timezone requirements.**
    *   If you only care about date or time without any timezone context (e.g., a birth date, an opening time for a store that's the same in every locale), use `LocalDate`, `LocalTime`, or `LocalDateTime`.
    *   If you need to represent a specific point in time regardless of where it's observed (e.g., event timestamps, logging), use `Instant`. Store `Instant` in your database if possible.
    *   If you need to represent a date and time *in a specific timezone* and handle daylight saving rules correctly (e.g., meeting schedules, flight times), use `ZonedDateTime`.
3.  **Use `DateTimeFormatter` for all parsing and formatting involving strings.** Never manually parse or format date/time strings.
4.  **Store `Instant` or `LocalDateTime` in databases.**
    *   `Instant` (often mapped to `TIMESTAMP WITH TIME ZONE` or similar, or just UTC `TIMESTAMP`): Best for global, unambiguous timestamps.
    *   `LocalDateTime` (often mapped to `TIMESTAMP` or `DATETIME`): Best when the time zone is *not* relevant to the stored value itself, but the date/time components are relevant (e.g., "start of day" in a local context). Be aware that if your application servers are in different time zones, `LocalDateTime` might be ambiguous.
5.  **Prefer `Duration` for time-based amounts (e.g., "30 minutes") and `Period` for date-based amounts (e.g., "3 months, 2 days").**
6.  **Immutable objects are your friends.** The immutability of `java.time` classes prevents many common bugs related to shared mutable state and simplifies concurrency.