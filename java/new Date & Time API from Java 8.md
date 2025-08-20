The `java.time` package, introduced in Java 8, is a comprehensive and well-designed API for handling dates and times. It addresses many of the shortcomings of the old `java.util.Date` and `java.util.Calendar` classes, such as mutability, thread-safety issues, poor API design, and a lack of clear separation between date, time, and timezone concepts.

## New Date & Time API in Java 8 (`java.time`)

### 1. Why the New API? (Problems with Old API)

Before diving into the new API, let's quickly review the major problems with the legacy `java.util.Date` and `java.util.Calendar`:

*   **Mutability:** `Date` objects are mutable, leading to potential bugs in multi-threaded environments or when passed as arguments.
*   **Not Thread-Safe:** `Calendar` is not thread-safe.
*   **Poor API Design:**
    *   Month indexing starts from 0 (January is 0, December is 11).
    *   Year in `Date` represents the year minus 1900.
    *   No clear separation between date, time, and date-time.
    *   Confusing methods (e.g., `Date.setHours()`).
*   **Lack of Readability:** Code using `Calendar` often became verbose and hard to read.
*   **No Concept of Timezones:** Handling timezones was complex and error-prone.

### 2. Core Concepts of `java.time`

The new API is designed with several key principles:

*   **Immutability:** All classes in `java.time` are immutable. Methods that "modify" a date/time object actually return a *new* instance with the changes, leaving the original unchanged. This inherently makes them thread-safe.
*   **Fluent API:** Methods are often chainable, making code more readable and concise.
*   **Clear Separation of Concerns:**
    *   `LocalDate`: Date without time or timezone.
    *   `LocalTime`: Time without date or timezone.
    *   `LocalDateTime`: Date and time without timezone.
    *   `Instant`: A timestamp representing a point on the time-line in UTC.
    *   `ZonedDateTime`: Date, time, and timezone.
    *   `OffsetDateTime`: Date, time, and an offset from UTC.
*   **Type-Safety:** Different types for different date/time concepts prevent accidental mixing.
*   **Extensive Utility Classes:** `Period`, `Duration`, `TemporalAdjusters`, `DateTimeFormatter`, `ZoneId`, `ZoneOffset`.

### 3. Key Classes and Examples

Let's explore the most commonly used classes with detailed examples.

---

#### 3.1. `LocalDate`

Represents a date (year, month, day) without a time or timezone.

**How to Create:**

*   `LocalDate.now()`: Current date.
*   `LocalDate.of(year, month, day)`: Specific date.
*   `LocalDate.parse("YYYY-MM-DD")`: From a string.

**Example: Basic `LocalDate` Operations**

```java
// Input (Java Code)
import java.time.LocalDate;
import java.time.Month;

public class LocalDateExample {
    public static void main(String[] args) {
        // 1. Get current date
        LocalDate today = LocalDate.now();
        System.out.println("1. Today's date: " + today);

        // 2. Create a specific date
        LocalDate independenceDay = LocalDate.of(1947, Month.AUGUST, 15);
        System.out.println("2. Indian Independence Day: " + independenceDay);

        // 3. Parse a date string
        LocalDate christmas2024 = LocalDate.parse("2024-12-25");
        System.out.println("3. Christmas 2024: " + christmas2024);

        // 4. Get components of a date
        System.out.println("4. Year of Christmas 2024: " + christmas2024.getYear());
        System.out.println("   Month of Christmas 2024: " + christmas2024.getMonth()); // Returns Month enum
        System.out.println("   Day of Christmas 2024: " + christmas2024.getDayOfMonth());
        System.out.println("   Day of week for Christmas 2024: " + christmas2024.getDayOfWeek());

        // 5. Manipulate dates (returns new instances)
        LocalDate nextWeek = today.plusWeeks(1);
        System.out.println("5. Date next week: " + nextWeek);

        LocalDate lastMonth = today.minusMonths(1);
        System.out.println("   Date last month: " + lastMonth);

        LocalDate newYear = today.withMonth(1).withDayOfMonth(1); // Set month and day
        System.out.println("   Start of current year: " + newYear);

        // 6. Compare dates
        System.out.println("6. Is Christmas 2024 before today? " + christmas2024.isBefore(today));
        System.out.println("   Is today after Independence Day? " + today.isAfter(independenceDay));
        System.out.println("   Is today equal to itself? " + today.isEqual(LocalDate.now())); // Will be true unless execution time difference

        // 7. Check for leap year
        System.out.println("7. Is 2024 a leap year? " + christmas2024.isLeapYear());
    }
}
```

```
// Output (Example - actual output for dates will vary based on execution time)
1. Today's date: 2023-10-27
2. Indian Independence Day: 1947-08-15
3. Christmas 2024: 2024-12-25
4. Year of Christmas 2024: 2024
   Month of Christmas 2024: DECEMBER
   Day of Christmas 2024: 25
   Day of week for Christmas 2024: WEDNESDAY
5. Date next week: 2023-11-03
   Date last month: 2023-09-27
   Start of current year: 2023-01-01
6. Is Christmas 2024 before today? false
   Is today after Independence Day? true
   Is today equal to itself? true
7. Is 2024 a leap year? true
```

---

#### 3.2. `LocalTime`

Represents a time (hour, minute, second, nanosecond) without a date or timezone.

**How to Create:**

*   `LocalTime.now()`: Current time.
*   `LocalTime.of(hour, minute, second, nanoOfSecond)`: Specific time.
*   `LocalTime.parse("HH:mm:ss.SSS")`: From a string.

**Example: Basic `LocalTime` Operations**

```java
// Input (Java Code)
import java.time.LocalTime;

public class LocalTimeExample {
    public static void main(String[] args) {
        // 1. Get current time
        LocalTime now = LocalTime.now();
        System.out.println("1. Current time: " + now);

        // 2. Create a specific time
        LocalTime lunchTime = LocalTime.of(12, 30, 0);
        System.out.println("2. Lunch time: " + lunchTime);

        // 3. Parse a time string
        LocalTime meetingTime = LocalTime.parse("09:15:30.123");
        System.out.println("3. Meeting time: " + meetingTime);

        // 4. Get components of a time
        System.out.println("4. Hour of meeting time: " + meetingTime.getHour());
        System.out.println("   Minute of meeting time: " + meetingTime.getMinute());
        System.out.println("   Second of meeting time: " + meetingTime.getSecond());
        System.out.println("   Nano of meeting time: " + meetingTime.getNano());

        // 5. Manipulate times (returns new instances)
        LocalTime inTwoHours = now.plusHours(2);
        System.out.println("5. Time in 2 hours: " + inTwoHours);

        LocalTime tenMinutesAgo = now.minusMinutes(10);
        System.out.println("   Time 10 minutes ago: " + tenMinutesAgo);

        LocalTime specificSecond = now.withSecond(0).withNano(0); // Set specific second and nano
        System.out.println("   Current time without seconds/nanos: " + specificSecond);

        // 6. Compare times
        System.out.println("6. Is lunch time before meeting time? " + lunchTime.isBefore(meetingTime));
        System.out.println("   Is current time after lunch time? " + now.isAfter(lunchTime));
    }
}
```

```
// Output (Example - actual output for times will vary based on execution time)
1. Current time: 10:35:45.123456789
2. Lunch time: 12:30:00
3. Meeting time: 09:15:30.123
4. Hour of meeting time: 9
   Minute of meeting time: 15
   Second of meeting time: 30
   Nano of meeting time: 123000000
5. Time in 2 hours: 12:35:45.123456789
   Time 10 minutes ago: 10:25:45.123456789
   Current time without seconds/nanos: 10:35:00
6. Is lunch time before meeting time? false
   Is current time after lunch time? true
```

---

#### 3.3. `LocalDateTime`

Represents a date and time without a timezone. It's a combination of `LocalDate` and `LocalTime`.

**How to Create:**

*   `LocalDateTime.now()`: Current date and time.
*   `LocalDateTime.of(LocalDate date, LocalTime time)`: From existing `LocalDate` and `LocalTime`.
*   `LocalDateTime.of(year, month, day, hour, minute, second)`: Specific date and time.
*   `LocalDateTime.parse("YYYY-MM-DDTHH:mm:ss")`: From a string (note the 'T' separator).

**Example: Basic `LocalDateTime` Operations**

```java
// Input (Java Code)
import java.time.LocalDateTime;
import java.time.Month;

public class LocalDateTimeExample {
    public static void main(String[] args) {
        // 1. Get current date and time
        LocalDateTime currentDateTime = LocalDateTime.now();
        System.out.println("1. Current date and time: " + currentDateTime);

        // 2. Create a specific date and time
        LocalDateTime meetingStart = LocalDateTime.of(2023, Month.NOVEMBER, 10, 14, 0, 0);
        System.out.println("2. Meeting start: " + meetingStart);

        // 3. Parse a date-time string
        LocalDateTime flightDeparture = LocalDateTime.parse("2023-11-20T18:45:00");
        System.out.println("3. Flight departure: " + flightDeparture);

        // 4. Get components (combines LocalDate and LocalTime methods)
        System.out.println("4. Year: " + flightDeparture.getYear());
        System.out.println("   Hour: " + flightDeparture.getHour());

        // 5. Manipulate date-time (returns new instances)
        LocalDateTime nextDay = currentDateTime.plusDays(1);
        System.out.println("5. Date and time tomorrow: " + nextDay);

        LocalDateTime tenMinutesLater = currentDateTime.plusMinutes(10);
        System.out.println("   Date and time 10 minutes later: " + tenMinutesLater);

        // 6. Convert to LocalDate or LocalTime
        System.out.println("6. Date part: " + currentDateTime.toLocalDate());
        System.out.println("   Time part: " + currentDateTime.toLocalTime());
    }
}
```

```
// Output (Example - actual output will vary)
1. Current date and time: 2023-10-27T10:35:45.123456789
2. Meeting start: 2023-11-10T14:00:00
3. Flight departure: 2023-11-20T18:45:00
4. Year: 2023
   Hour: 18
5. Date and time tomorrow: 2023-10-28T10:35:45.123456789
   Date and time 10 minutes later: 2023-10-27T10:45:45.123456789
6. Date part: 2023-10-27
   Time part: 10:35:45.123456789
```

---

#### 3.4. `Instant`

Represents an instantaneous point on the time-line in UTC (Coordinated Universal Time). It's essentially a timestamp, often used for machine-level time recording.

**How to Create:**

*   `Instant.now()`: Current UTC instant.
*   `Instant.ofEpochMilli(long epochMilli)`: From milliseconds since the epoch (January 1, 1970, 00:00:00 UTC).
*   `Instant.parse("YYYY-MM-DDTHH:mm:ss.SSSZ")`: From a string (ISO 8601 format with 'Z' for UTC).

**Example: `Instant` Operations**

```java
// Input (Java Code)
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;

public class InstantExample {
    public static void main(String[] args) {
        // 1. Get current Instant (UTC)
        Instant currentInstant = Instant.now();
        System.out.println("1. Current Instant (UTC): " + currentInstant);

        // 2. Create Instant from epoch milliseconds
        long epochMilli = 1678886400000L; // March 15, 2023 00:00:00 UTC
        Instant specificInstant = Instant.ofEpochMilli(epochMilli);
        System.out.println("2. Instant from epoch milliseconds: " + specificInstant);

        // 3. Convert Instant to epoch milliseconds
        long toEpochMilli = currentInstant.toEpochMilli();
        System.out.println("3. Current Instant in epoch milliseconds: " + toEpochMilli);

        // 4. Parse an Instant string
        Instant parsedInstant = Instant.parse("2023-01-01T12:00:00Z"); // Z indicates UTC
        System.out.println("4. Parsed Instant: " + parsedInstant);

        // 5. Add/subtract duration
        Instant tenMinutesLater = currentInstant.plusSeconds(60 * 10);
        System.out.println("5. Instant 10 minutes later: " + tenMinutesLater);

        // 6. Convert Instant to LocalDateTime (requires an offset/zone)
        // For UTC, use ZoneOffset.UTC or ZoneOffset.ofHours(0)
        LocalDateTime localDateTimeFromInstant = LocalDateTime.ofInstant(currentInstant, ZoneOffset.UTC);
        System.out.println("6. Current Instant as LocalDateTime (UTC): " + localDateTimeFromInstant);

        // Convert LocalDateTime to Instant (requires an offset/zone)
        LocalDateTime localDt = LocalDateTime.of(2023, 10, 27, 10, 0);
        Instant instantFromLocalDt = localDt.toInstant(ZoneOffset.ofHours(5, 30)); // Assuming IST offset
        System.out.println("   Local 2023-10-27 10:00 IST as Instant: " + instantFromLocalDt);
    }
}
```

```
// Output (Example - actual output will vary)
1. Current Instant (UTC): 2023-10-27T04:35:45.123456789Z
2. Instant from epoch milliseconds: 2023-03-15T00:00:00Z
3. Current Instant in epoch milliseconds: 1698371745123
4. Parsed Instant: 2023-01-01T12:00:00Z
5. Instant 10 minutes later: 2023-10-27T04:45:45.123456789Z
6. Current Instant as LocalDateTime (UTC): 2023-10-27T04:35:45.123456789
   Local 2023-10-27 10:00 IST as Instant: 2023-10-27T04:30:00Z
```

---

#### 3.5. `ZonedDateTime`

Represents a date, time, and timezone. It's the most complete date/time object, useful for applications that need to be aware of different geographic locations and daylight saving rules.

**How to Create:**

*   `ZonedDateTime.now()`: Current date, time, and system default timezone.
*   `ZonedDateTime.now(ZoneId zone)`: Current date, time, and a specific timezone.
*   `ZonedDateTime.of(LocalDateTime dateTime, ZoneId zone)`: From `LocalDateTime` and `ZoneId`.
*   `ZonedDateTime.parse("YYYY-MM-DDTHH:mm:ss.SSS[ZoneId]")`: From a string.

**Example: `ZonedDateTime` Operations**

```java
// Input (Java Code)
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;

public class ZonedDateTimeExample {
    public static void main(String[] args) {
        // 1. Get system default timezone
        ZoneId defaultZone = ZoneId.systemDefault();
        System.out.println("1. System Default Zone: " + defaultZone);

        // 2. Get a specific timezone
        ZoneId newYorkZone = ZoneId.of("America/New_York");
        ZoneId londonZone = ZoneId.of("Europe/London");
        ZoneId tokyoZone = ZoneId.of("Asia/Tokyo");
        System.out.println("   New York Zone: " + newYorkZone);

        // 3. Get current ZonedDateTime in default zone
        ZonedDateTime nowInDefaultZone = ZonedDateTime.now();
        System.out.println("3. Current ZonedDateTime (Default Zone): " + nowInDefaultZone);

        // 4. Get current ZonedDateTime in a specific zone
        ZonedDateTime nowInNewYork = ZonedDateTime.now(newYorkZone);
        System.out.println("4. Current ZonedDateTime (New York): " + nowInNewYork);

        // 5. Create ZonedDateTime from LocalDateTime and ZoneId
        LocalDateTime localDt = LocalDateTime.of(2024, 1, 1, 9, 0); // Jan 1, 2024, 9 AM
        ZonedDateTime newYorkDateTime = ZonedDateTime.of(localDt, newYorkZone);
        System.out.println("5. Specific DateTime in New York: " + newYorkDateTime);

        // 6. Convert ZonedDateTime between timezones
        ZonedDateTime londonDateTime = newYorkDateTime.withZoneSameInstant(londonZone);
        System.out.println("6. Same Instant in London: " + londonDateTime);

        ZonedDateTime tokyoDateTime = newYorkDateTime.withZoneSameInstant(tokyoZone);
        System.out.println("   Same Instant in Tokyo: " + tokyoDateTime);

        // Note: withZoneSameLocal() changes the instant while keeping local date/time
        ZonedDateTime localTimeInLondon = newYorkDateTime.withZoneSameLocal(londonZone);
        System.out.println("   Same Local Time (9 AM) in London (Different Instant): " + localTimeInLondon);

        // 7. Parse ZonedDateTime string
        ZonedDateTime parsedZdt = ZonedDateTime.parse("2023-11-01T10:30:00+01:00[Europe/Paris]");
        System.out.println("7. Parsed ZonedDateTime: " + parsedZdt);
    }
}
```

```
// Output (Example - actual output will vary)
1. System Default Zone: Asia/Kolkata
   New York Zone: America/New_York
3. Current ZonedDateTime (Default Zone): 2023-10-27T10:35:45.123456789+05:30[Asia/Kolkata]
4. Current ZonedDateTime (New York): 2023-10-27T01:05:45.123456789-04:00[America/New_York]
5. Specific DateTime in New York: 2024-01-01T09:00-05:00[America/New_York]
6. Same Instant in London: 2024-01-01T14:00+00:00[Europe/London]
   Same Instant in Tokyo: 2024-01-01T23:00+09:00[Asia/Tokyo]
   Same Local Time (9 AM) in London (Different Instant): 2024-01-01T09:00+00:00[Europe/London]
7. Parsed ZonedDateTime: 2023-11-01T10:30+01:00[Europe/Paris]
```

---

#### 3.6. `Duration`

Represents a time-based amount of time, such as "3 hours, 20 minutes". It's often used to measure the difference between two `Instant`s or `LocalTime`s.

**How to Create:**

*   `Duration.between(startTemporal, endTemporal)`: Measures duration between two temporal objects.
*   `Duration.ofDays()`, `ofHours()`, `ofMinutes()`, `ofSeconds()`, `ofNanos()`: Specific durations.

**Example: `Duration` Operations**

```java
// Input (Java Code)
import java.time.Duration;
import java.time.Instant;
import java.time.LocalTime;
import java.time.temporal.ChronoUnit;

public class DurationExample {
    public static void main(String[] args) {
        // 1. Measure duration between two Instants
        Instant start = Instant.parse("2023-10-27T09:00:00Z");
        Instant end = Instant.parse("2023-10-27T12:30:00Z");
        Duration duration1 = Duration.between(start, end);
        System.out.println("1. Duration between Instants: " + duration1); // PThHMMSS.NNNS

        // 2. Measure duration between two LocalTimes
        LocalTime startTime = LocalTime.of(9, 0);
        LocalTime endTime = LocalTime.of(12, 30);
        Duration duration2 = Duration.between(startTime, endTime);
        System.out.println("2. Duration between LocalTimes: " + duration2);

        // 3. Create specific durations
        Duration oneHour = Duration.ofHours(1);
        System.out.println("3. One hour duration: " + oneHour);

        Duration fiveMinutes = Duration.of(5, ChronoUnit.MINUTES);
        System.out.println("   Five minutes duration: " + fiveMinutes);

        // 4. Get components of a duration
        System.out.println("4. Duration in hours: " + duration1.toHours());
        System.out.println("   Duration in minutes: " + duration1.toMinutes());
        System.out.println("   Duration in seconds: " + duration1.getSeconds());

        // 5. Add/subtract durations
        Duration sumDuration = oneHour.plus(fiveMinutes);
        System.out.println("5. One hour + five minutes: " + sumDuration);

        Duration diffDuration = duration1.minusSeconds(30);
        System.out.println("   Duration minus 30 seconds: " + diffDuration);
    }
}
```

```
// Output
1. Duration between Instants: PT3H30M
2. Duration between LocalTimes: PT3H30M
3. One hour duration: PT1H
   Five minutes duration: PT5M
4. Duration in hours: 3
   Duration in minutes: 210
   Duration in seconds: 12600
5. One hour + five minutes: PT1H5M
   Duration minus 30 seconds: PT3H29M30S
```

---

#### 3.7. `Period`

Represents a date-based amount of time, such as "2 years, 3 months, and 5 days". It's used with `LocalDate` objects.

**How to Create:**

*   `Period.between(startDate, endDate)`: Measures period between two `LocalDate` objects.
*   `Period.ofYears()`, `ofMonths()`, `ofDays()`: Specific periods.

**Example: `Period` Operations**

```java
// Input (Java Code)
import java.time.LocalDate;
import java.time.Period;

public class PeriodExample {
    public static void main(String[] args) {
        // 1. Measure period between two LocalDates
        LocalDate startDate = LocalDate.of(2020, 1, 15);
        LocalDate endDate = LocalDate.of(2023, 10, 27);
        Period period = Period.between(startDate, endDate);
        System.out.println("1. Period between dates: " + period); // PYYyMMmDDd

        // 2. Create specific periods
        Period twoYearsThreeMonths = Period.ofYears(2).plusMonths(3);
        System.out.println("2. Two years, three months: " + twoYearsThreeMonths);

        Period aWeek = Period.ofWeeks(1); // Converts to days
        System.out.println("   One week period: " + aWeek);

        // 3. Get components of a period
        System.out.println("3. Years in period: " + period.getYears());
        System.out.println("   Months in period: " + period.getMonths());
        System.out.println("   Days in period: " + period.getDays());

        // 4. Add/subtract periods
        LocalDate futureDate = endDate.plus(twoYearsThreeMonths);
        System.out.println("4. End date plus 2y 3m: " + futureDate);

        Period adjustedPeriod = period.minusMonths(5);
        System.out.println("   Period minus 5 months: " + adjustedPeriod);
    }
}
```

```
// Output
1. Period between dates: P3Y9M12D
2. Two years, three months: P2Y3M
   One week period: P7D
3. Years in period: 3
   Months in period: 9
   Days in period: 12
4. End date plus 2y 3m: 2026-01-27
   Period minus 5 months: P3Y4M12D
```

---

#### 3.8. `DateTimeFormatter`

Used for formatting `java.time` objects into strings and parsing strings into `java.time` objects.

**How to Create:**

*   `DateTimeFormatter.ofPattern("custom_pattern")`: Custom pattern (e.g., "dd/MM/yyyy").
*   `DateTimeFormatter.ISO_DATE`, `ISO_LOCAL_DATE_TIME`, etc.: Predefined formatters.

**Example: `DateTimeFormatter` Operations**

```java
// Input (Java Code)
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class DateTimeFormatterExample {
    public static void main(String[] args) {
        LocalDateTime now = LocalDateTime.now();
        LocalDate today = LocalDate.now();

        // 1. Formatting with predefined formatters
        String isoDate = today.format(DateTimeFormatter.ISO_LOCAL_DATE);
        System.out.println("1. ISO Date: " + isoDate);

        String isoDateTime = now.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
        System.out.println("   ISO Date-Time: " + isoDateTime);

        // 2. Formatting with custom patterns
        DateTimeFormatter customFormatter1 = DateTimeFormatter.ofPattern("dd-MM-yyyy HH:mm:ss");
        String formattedDateTime1 = now.format(customFormatter1);
        System.out.println("2. Custom Format 1: " + formattedDateTime1);

        DateTimeFormatter customFormatter2 = DateTimeFormatter.ofPattern("EEEE, MMMM dd, yyyy 'at' hh:mm a");
        String formattedDateTime2 = now.format(customFormatter2);
        System.out.println("   Custom Format 2: " + formattedDateTime2);

        // 3. Parsing strings into date/time objects
        String dateString = "15/08/1947";
        DateTimeFormatter parseFormatter1 = DateTimeFormatter.ofPattern("dd/MM/yyyy");
        LocalDate parsedDate = LocalDate.parse(dateString, parseFormatter1);
        System.out.println("3. Parsed Date: " + parsedDate);

        String dateTimeString = "2023-11-01 14:30:00";
        DateTimeFormatter parseFormatter2 = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        LocalDateTime parsedDateTime = LocalDateTime.parse(dateTimeString, parseFormatter2);
        System.out.println("   Parsed Date-Time: " + parsedDateTime);

        // Parsing using default ISO format (no formatter needed if string matches)
        String isoDateString = "2023-10-27";
        LocalDate defaultParsedDate = LocalDate.parse(isoDateString);
        System.out.println("   Default Parsed Date: " + defaultParsedDate);
    }
}
```

```
// Output (Example - actual output will vary)
1. ISO Date: 2023-10-27
   ISO Date-Time: 2023-10-27T10:35:45.123456789
2. Custom Format 1: 27-10-2023 10:35:45
   Custom Format 2: Friday, October 27, 2023 at 10:35 AM
3. Parsed Date: 1947-08-15
   Parsed Date-Time: 2023-11-01T14:30:00
   Default Parsed Date: 2023-10-27
```

---

#### 3.9. `TemporalAdjusters`

A utility class that provides a set of pre-defined `TemporalAdjuster` implementations. These are useful for performing common date adjustments, such as "next working day", "last day of the month", "first day of next year", etc.

**How to Use:**

*   Used with the `with()` method of `LocalDate`, `LocalDateTime`, `ZonedDateTime`.
*   `TemporalAdjusters.nextOrSame(DayOfWeek)`
*   `TemporalAdjusters.lastDayOfMonth()`
*   `TemporalAdjusters.firstDayOfNextYear()`

**Example: `TemporalAdjusters` Operations**

```java
// Input (Java Code)
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.temporal.TemporalAdjusters;

public class TemporalAdjustersExample {
    public static void main(String[] args) {
        LocalDate today = LocalDate.of(2023, 10, 27); // Friday

        // 1. Next Tuesday
        LocalDate nextTuesday = today.with(TemporalAdjusters.next(DayOfWeek.TUESDAY));
        System.out.println("1. Next Tuesday from " + today + ": " + nextTuesday);

        // 2. Next or same Friday
        LocalDate nextOrSameFriday = today.with(TemporalAdjusters.nextOrSame(DayOfWeek.FRIDAY));
        System.out.println("2. Next or Same Friday from " + today + ": " + nextOrSameFriday);

        // 3. Last day of the month
        LocalDate lastDay = today.with(TemporalAdjusters.lastDayOfMonth());
        System.out.println("3. Last day of October 2023: " + lastDay);

        // 4. First day of next month
        LocalDate firstDayOfNextMonth = today.with(TemporalAdjusters.firstDayOfNextMonth());
        System.out.println("4. First day of next month from " + today + ": " + firstDayOfNextMonth);

        // 5. First day of next year
        LocalDate firstDayOfNextYear = today.with(TemporalAdjusters.firstDayOfNextYear());
        System.out.println("5. First day of next year from " + today + ": " + firstDayOfNextYear);

        // 6. Custom adjuster: Next working day (Mon-Fri)
        // This is a more complex example where you might combine adjusters
        // or create your own custom TemporalAdjuster.
        // For simplicity, let's just illustrate a common pattern.
        LocalDate weekendDate = LocalDate.of(2023, 10, 28); // Saturday
        LocalDate nextWorkingDay = weekendDate.with(TemporalAdjusters.nextOrSame(DayOfWeek.MONDAY));
        System.out.println("6. Next working day from " + weekendDate + ": " + nextWorkingDay);
    }
}
```

```
// Output
1. Next Tuesday from 2023-10-27: 2023-10-31
2. Next or Same Friday from 2023-10-27: 2023-10-27
3. Last day of October 2023: 2023-10-31
4. First day of next month from 2023-10-27: 2023-11-01
5. First day of next year from 2023-10-27: 2024-01-01
6. Next working day from 2023-10-28: 2023-10-30
```

---

### 4. Backward Compatibility (Converting Old to New and Vice Versa)

The `java.time` API provides methods to convert between the old `java.util.Date`/`java.util.Calendar` and the new types.

```java
// Input (Java Code)
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

public class BackwardCompatibilityExample {
    public static void main(String[] args) {
        // --- Old to New ---

        // 1. From java.util.Date to Instant
        Date oldDate = new Date(); // Current date/time
        Instant instantFromDate = oldDate.toInstant();
        System.out.println("1. Old Date: " + oldDate + " -> Instant: " + instantFromDate);

        // 2. From java.util.Date to LocalDateTime (requires ZoneId)
        LocalDateTime localDateTimeFromDate = oldDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDateTime();
        System.out.println("2. Old Date: " + oldDate + " -> LocalDateTime: " + localDateTimeFromDate);

        // 3. From java.util.Calendar to ZonedDateTime
        Calendar oldCalendar = Calendar.getInstance(); // Current date/time
        ZonedDateTime zonedDateTimeFromCalendar = oldCalendar.toInstant().atZone(oldCalendar.getTimeZone().toZoneId());
        System.out.println("3. Old Calendar: " + oldCalendar.getTime() + " -> ZonedDateTime: " + zonedDateTimeFromCalendar);

        // Or, more directly from GregorianCalendar
        GregorianCalendar gc = new GregorianCalendar();
        ZonedDateTime zdtFromGc = gc.toZonedDateTime();
        System.out.println("   GregorianCalendar: " + gc.getTime() + " -> ZonedDateTime: " + zdtFromGc);


        // --- New to Old ---

        // 4. From Instant to java.util.Date
        Instant newInstant = Instant.now();
        Date newDateFromInstant = Date.from(newInstant);
        System.out.println("4. New Instant: " + newInstant + " -> Old Date: " + newDateFromInstant);

        // 5. From ZonedDateTime to java.util.Date
        ZonedDateTime newZonedDateTime = ZonedDateTime.now();
        Date newDateFromZonedDateTime = Date.from(newZonedDateTime.toInstant());
        System.out.println("5. New ZonedDateTime: " + newZonedDateTime + " -> Old Date: " + newDateFromZonedDateTime);

        // 6. From ZonedDateTime to java.util.Calendar
        ZonedDateTime anotherNewZonedDateTime = ZonedDateTime.now();
        Calendar newCalendarFromZonedDateTime = GregorianCalendar.from(anotherNewZonedDateTime);
        System.out.println("6. New ZonedDateTime: " + anotherNewZonedDateTime + " -> Old Calendar: " + newCalendarFromZonedDateTime.getTime());
    }
}
```

```
// Output (Example - actual output will vary based on execution time and system timezone)
1. Old Date: Fri Oct 27 10:35:45 IST 2023 -> Instant: 2023-10-27T05:05:45.123Z
2. Old Date: Fri Oct 27 10:35:45 IST 2023 -> LocalDateTime: 2023-10-27T10:35:45.123
3. Old Calendar: Fri Oct 27 10:35:45 IST 2023 -> ZonedDateTime: 2023-10-27T10:35:45.123+05:30[Asia/Kolkata]
   GregorianCalendar: Fri Oct 27 10:35:45 IST 2023 -> ZonedDateTime: 2023-10-27T10:35:45.123+05:30[Asia/Kolkata]
4. New Instant: 2023-10-27T05:05:45.123Z -> Old Date: Fri Oct 27 10:35:45 IST 2023
5. New ZonedDateTime: 2023-10-27T10:35:45.123+05:30[Asia/Kolkata] -> Old Date: Fri Oct 27 10:35:45 IST 2023
6. New ZonedDateTime: 2023-10-27T10:35:45.123+05:30[Asia/Kolkata] -> Old Calendar: Fri Oct 27 10:35:45 IST 2023
```

---

### Conclusion

The `java.time` API is a significant improvement over the legacy `Date` and `Calendar` classes. Its design principles (immutability, clear separation of concerns, fluent API) lead to more robust, readable, and maintainable date and time handling code. By embracing this new API, developers can avoid many common pitfalls and write more expressive date and time logic in their Java applications.