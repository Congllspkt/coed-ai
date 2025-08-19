Java's date and time handling has evolved significantly. Before Java 8, it was notoriously clunky and error-prone with `java.util.Date` and `java.util.Calendar`. Java 8 introduced the new `java.time` package (JSR-310), which provides a much more robust, immutable, and intuitive API for working with dates and times.

This guide will cover both the old and new APIs, focusing heavily on the `java.time` package as it's the recommended approach for modern Java development.

---

# Java Date and Time APIs

## 1. Introduction

Working with dates and times in programming often involves challenges like:
*   **Time Zones:** Converting between different time zones, handling daylight saving.
*   **Mutability:** Old date objects could be modified after creation, leading to unexpected behavior.
*   **Thread Safety:** Mutable objects are not inherently thread-safe.
*   **Clarity:** Ambiguous APIs (e.g., month starting from 0, or `Date` representing an instant, not a date).
*   **Calculations:** Performing arithmetic operations (add days, find difference) correctly.

The `java.time` package in Java 8+ addresses these issues with a well-designed, immutable, and thread-safe set of classes.

## 2. The Old Date and Time API (Pre-Java 8)

The classes `java.util.Date` and `java.util.Calendar` were the primary way to handle dates and times before Java 8. They are largely deprecated for new code due to their significant shortcomings.

### 2.1 `java.util.Date`

*   Represents a specific instant in time (milliseconds since the Unix epoch - January 1, 1970, 00:00:00 GMT).
*   Mutable, meaning its value can be changed after creation. This leads to thread-safety issues and unpredictable behavior.
*   Methods like `getYear()`, `getMonth()`, `getDay()` are deprecated because they don't account for time zones properly and are confusing (e.g., months are 0-indexed).

#### Example: `java.util.Date`

```java
import java.util.Date;

public class OldDateExample {
    public static void main(String[] args) {
        System.out.println("--- java.util.Date Example ---");

        // 1. Creating a Date object for the current instant
        Date currentDate = new Date();
        System.out.println("Current Date: " + currentDate);

        // 2. Creating a Date from milliseconds (since epoch)
        long milliseconds = 1678886400000L; // March 15, 2023 12:00:00 PM GMT
        Date specificDate = new Date(milliseconds);
        System.out.println("Specific Date from millis: " + specificDate);

        // 3. Mutability demonstration (DO NOT DO THIS IN PRODUCTION CODE)
        Date anotherDate = new Date();
        System.out.println("Before modification: " + anotherDate);
        anotherDate.setTime(0); // Sets it to Jan 1, 1970, 00:00:00 GMT
        System.out.println("After modification:  " + anotherDate);

        // Note: Many useful methods like getYear(), getMonth() are deprecated
        // due to issues with time zones and their confusing nature.
    }
}
```

**Output:**

```
--- java.util.Date Example ---
Current Date: Wed May 15 10:30:45 EDT 2024 // (Actual date/time will vary)
Specific Date from millis: Wed Mar 15 08:00:00 EDT 2023 // (Actual timezone may vary)
Before modification: Wed May 15 10:30:45 EDT 2024 // (Actual date/time will vary)
After modification:  Wed Dec 31 19:00:00 EST 1969 // (Actual timezone may vary, 0 GMT is previous day in EST)
```

### 2.2 `java.util.Calendar`

*   An abstract class providing methods for converting between a `Date` object and a set of integer fields such as year, month, day, hour, and minute.
*   More powerful than `Date` for date/time arithmetic and field manipulation.
*   Still mutable and cumbersome to use (e.g., month is 0-indexed, but day of month starts at 1; constants for fields are often hard to remember).
*   Inherently complex due to dealing with locales, time zones, and different calendar systems.

#### Example: `java.util.Calendar`

```java
import java.util.Calendar;
import java.util.Date;

public class OldCalendarExample {
    public static void main(String[] args) {
        System.out.println("--- java.util.Calendar Example ---");

        // 1. Get a Calendar instance (usually GregorianCalendar)
        Calendar calendar = Calendar.getInstance();
        System.out.println("Current Calendar: " + calendar.getTime());

        // 2. Set specific date/time fields
        calendar.set(2023, Calendar.MARCH, 15, 10, 30, 0); // Year, Month (0-indexed), Day, Hour, Minute, Second
        System.out.println("Set Calendar Date: " + calendar.getTime());

        // 3. Add or subtract time
        calendar.add(Calendar.DAY_OF_MONTH, 5); // Add 5 days
        System.out.println("After adding 5 days: " + calendar.getTime());

        calendar.add(Calendar.HOUR, -2); // Subtract 2 hours
        System.out.println("After subtracting 2 hours: " + calendar.getTime());

        // 4. Get specific fields
        int year = calendar.get(Calendar.YEAR);
        int month = calendar.get(Calendar.MONTH); // 0-indexed month
        int dayOfMonth = calendar.get(Calendar.DAY_OF_MONTH);
        int dayOfWeek = calendar.get(Calendar.DAY_OF_WEEK); // Sunday is 1, Monday is 2, etc.

        System.out.println("Year: " + year);
        System.out.println("Month (0-indexed): " + month);
        System.out.println("Day of Month: " + dayOfMonth);
        System.out.println("Day of Week (1=Sunday): " + dayOfWeek);

        // 5. Convert Calendar to Date
        Date calendarToDate = calendar.getTime();
        System.out.println("Calendar to Date: " + calendarToDate);
    }
}
```

**Output:**

```
--- java.util.Calendar Example ---
Current Calendar: Wed May 15 10:30:45 EDT 2024 // (Actual date/time will vary)
Set Calendar Date: Wed Mar 15 10:30:00 EDT 2023 // (Actual timezone may vary)
After adding 5 days: Mon Mar 20 10:30:00 EDT 2023
After subtracting 2 hours: Mon Mar 20 08:30:00 EDT 2023
Year: 2023
Month (0-indexed): 2
Day of Month: 20
Day of Week (1=Sunday): 2
Calendar to Date: Mon Mar 20 08:30:00 EDT 2023
```

### 2.3 Problems with the Old API Summary

*   **Mutability:** Objects can be changed after creation, leading to side effects.
*   **Not Thread-Safe:** Not suitable for concurrent environments.
*   **Poor Design:**
    *   Months start from 0 (`JANUARY = 0`).
    *   Days of the week start from 1 (`SUNDAY = 1`).
    *   No clear separation between date, time, and date-time.
    *   Poor handling of time zones (e.g., `Date`'s `toString()` uses default time zone).
*   **Error-Prone:** Easy to introduce subtle bugs.

## 3. The New Date and Time API (Java 8+) - `java.time`

The `java.time` package, inspired by Joda-Time, provides a comprehensive and well-designed API.

**Key Features:**

*   **Immutability:** All core classes are immutable and thread-safe. Operations return new instances.
*   **Clear Definitions:** Specific classes for date-only, time-only, date-time (with/without time zone), and instants.
*   **Fluent API:** Method chaining for easier manipulation.
*   **Time Zone Support:** Explicit and robust handling of time zones.
*   **Clarity:** Months are `Month.JANUARY` or `1`, not `0`. Days of week are `DayOfWeek.MONDAY`.
*   **Calculations:** Easy and intuitive methods for adding, subtracting, and comparing time.

### 3.1 Core Classes

#### 3.1.1 `LocalDate`

*   Represents a date without time or time zone information.
*   Example: `2024-05-15`

```java
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.Month;

public class LocalDateExample {
    public static void main(String[] args) {
        System.out.println("--- LocalDate Example ---");

        // 1. Get current date
        LocalDate today = LocalDate.now();
        System.out.println("Today's Date: " + today);

        // 2. Create a specific date
        LocalDate specificDate = LocalDate.of(2023, Month.MARCH, 15);
        // or LocalDate specificDate = LocalDate.of(2023, 3, 15);
        System.out.println("Specific Date: " + specificDate);

        // 3. Parse a date string
        String dateString = "2024-10-26";
        LocalDate parsedDate = LocalDate.parse(dateString);
        System.out.println("Parsed Date: " + parsedDate);

        // 4. Manipulate dates (immutable operations)
        LocalDate tomorrow = today.plusDays(1);
        System.out.println("Tomorrow: " + tomorrow);

        LocalDate lastMonth = today.minusMonths(1);
        System.out.println("Last Month: " + lastMonth);

        LocalDate nextYearSameDay = today.plusYears(1);
        System.out.println("Next Year Same Day: " + nextYearSameDay);

        LocalDate firstDayOfNextMonth = today.plusMonths(1).withDayOfMonth(1);
        System.out.println("First Day of Next Month: " + firstDayOfNextMonth);

        // 5. Get date components
        int year = today.getYear();
        Month month = today.getMonth();
        int dayOfMonth = today.getDayOfMonth();
        DayOfWeek dayOfWeek = today.getDayOfWeek();
        int dayOfYear = today.getDayOfYear();

        System.out.println("Year: " + year);
        System.out.println("Month: " + month);
        System.out.println("Day of Month: " + dayOfMonth);
        System.out.println("Day of Week: " + dayOfWeek);
        System.out.println("Day of Year: " + dayOfYear);

        // 6. Compare dates
        System.out.println("Is today before specificDate? " + today.isBefore(specificDate));
        System.out.println("Is today after parsedDate? " + today.isAfter(parsedDate));
        System.out.println("Is today equal to itself? " + today.isEqual(LocalDate.now())); // Check for exact equality
    }
}
```

**Output:**

```
--- LocalDate Example ---
Today's Date: 2024-05-15 // (Actual date will vary)
Specific Date: 2023-03-15
Parsed Date: 2024-10-26
Tomorrow: 2024-05-16
Last Month: 2024-04-15
Next Year Same Day: 2025-05-15
First Day of Next Month: 2024-06-01
Year: 2024
Month: MAY
Day of Month: 15
Day of Week: WEDNESDAY
Day of Year: 136
Is today before specificDate? false
Is today after parsedDate? false
Is today equal to itself? true
```

#### 3.1.2 `LocalTime`

*   Represents a time without date or time zone information.
*   Example: `14:30:15.123`

```java
import java.time.LocalTime;
import java.time.temporal.ChronoUnit;

public class LocalTimeExample {
    public static void main(String[] args) {
        System.out.println("--- LocalTime Example ---");

        // 1. Get current time
        LocalTime now = LocalTime.now();
        System.out.println("Current Time: " + now);

        // 2. Create a specific time
        LocalTime specificTime = LocalTime.of(14, 30, 15); // Hour, Minute, Second
        System.out.println("Specific Time: " + specificTime);

        // 3. Create a specific time with nanoseconds
        LocalTime specificTimeNano = LocalTime.of(10, 20, 30, 123456789); // Hour, Minute, Second, Nanosecond
        System.out.println("Specific Time with Nanos: " + specificTimeNano);

        // 4. Parse a time string
        String timeString = "09:45:00";
        LocalTime parsedTime = LocalTime.parse(timeString);
        System.out.println("Parsed Time: " + parsedTime);

        // 5. Manipulate times (immutable operations)
        LocalTime futureTime = now.plusHours(2).minusMinutes(15);
        System.out.println("Future Time: " + futureTime);

        LocalTime truncatedToHour = now.truncatedTo(ChronoUnit.HOURS);
        System.out.println("Truncated to Hour: " + truncatedToHour);

        // 6. Get time components
        int hour = now.getHour();
        int minute = now.getMinute();
        int second = now.getSecond();
        int nano = now.getNano();

        System.out.println("Hour: " + hour);
        System.out.println("Minute: " + minute);
        System.out.println("Second: " + second);
        System.out.println("Nanosecond: " + nano);

        // 7. Compare times
        System.out.println("Is now before specificTime? " + now.isBefore(specificTime));
        System.out.println("Is now after parsedTime? " + now.isAfter(parsedTime));
    }
}
```

**Output:**

```
--- LocalTime Example ---
Current Time: 10:30:45.123456789 // (Actual time will vary)
Specific Time: 14:30:15
Specific Time with Nanos: 10:20:30.123456789
Parsed Time: 09:45
Future Time: 12:15:45.123456789
Truncated to Hour: 10:00
Hour: 10
Minute: 30
Second: 45
Nanosecond: 123456789
Is now before specificTime? true
Is now after parsedTime? true
```

#### 3.1.3 `LocalDateTime`

*   Represents a date and time without any time zone information.
*   Useful when dealing with dates and times in a single, consistent time zone (e.g., UTC) or when the time zone context is handled separately.
*   Example: `2024-05-15T10:30:45`

```java
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

public class LocalDateTimeExample {
    public static void main(String[] args) {
        System.out.println("--- LocalDateTime Example ---");

        // 1. Get current date and time
        LocalDateTime now = LocalDateTime.now();
        System.out.println("Current LocalDateTime: " + now);

        // 2. Create a specific date and time
        LocalDateTime specificDateTime = LocalDateTime.of(2023, 3, 15, 14, 30, 0);
        System.out.println("Specific LocalDateTime: " + specificDateTime);

        // 3. Combine LocalDate and LocalTime
        LocalDate date = LocalDate.of(2025, 1, 1);
        LocalTime time = LocalTime.of(23, 59, 59);
        LocalDateTime combinedDateTime = LocalDateTime.of(date, time);
        System.out.println("Combined LocalDateTime: " + combinedDateTime);

        // 4. Parse a date-time string
        String dateTimeString = "2024-07-20T18:00:00";
        LocalDateTime parsedDateTime = LocalDateTime.parse(dateTimeString);
        System.out.println("Parsed LocalDateTime: " + parsedDateTime);

        // 5. Manipulate date-time
        LocalDateTime nextWeekSameTime = now.plusWeeks(1);
        System.out.println("Next Week Same Time: " + nextWeekSameTime);

        LocalDateTime previousMonthHourLater = now.minusMonths(1).plusHours(1);
        System.out.println("Previous Month Hour Later: " + previousMonthHourLater);

        // 6. Extract LocalDate and LocalTime
        LocalDate extractedDate = now.toLocalDate();
        LocalTime extractedTime = now.toLocalTime();
        System.out.println("Extracted Date: " + extractedDate);
        System.out.println("Extracted Time: " + extractedTime);

        // 7. Compare
        System.out.println("Is now before specificDateTime? " + now.isBefore(specificDateTime));
        System.out.println("Is now after parsedDateTime? " + now.isAfter(parsedDateTime));
    }
}
```

**Output:**

```
--- LocalDateTime Example ---
Current LocalDateTime: 2024-05-15T10:30:45.123456789 // (Actual date/time will vary)
Specific LocalDateTime: 2023-03-15T14:30
Combined LocalDateTime: 2025-01-01T23:59:59
Parsed LocalDateTime: 2024-07-20T18:00
Next Week Same Time: 2024-05-22T10:30:45.123456789
Previous Month Hour Later: 2024-04-15T11:30:45.123456789
Extracted Date: 2024-05-15
Extracted Time: 10:30:45.123456789
Is now before specificDateTime? false
Is now after parsedDateTime? false
```

#### 3.1.4 `Instant`

*   Represents a point in time on the timeline, often used to record event timestamps.
*   Always stored as milliseconds/nanoseconds from the epoch (January 1, 1970, 00:00:00 GMT/UTC).
*   Does not contain any timezone information itself, it's just a raw timestamp.

```java
import java.time.Instant;
import java.time.ZoneId;
import java.time.ZonedDateTime;

public class InstantExample {
    public static void main(String[] args) {
        System.out.println("--- Instant Example ---");

        // 1. Get current instant (UTC)
        Instant now = Instant.now();
        System.out.println("Current Instant (UTC): " + now);

        // 2. Create an instant from epoch milliseconds
        long epochMilli = 1678886400000L; // March 15, 2023 12:00:00 PM GMT
        Instant specificInstant = Instant.ofEpochMilli(epochMilli);
        System.out.println("Specific Instant from millis: " + specificInstant);

        // 3. Convert Instant to epoch milliseconds
        long milliFromInstant = now.toEpochMilli();
        System.out.println("Current Instant in milliseconds: " + milliFromInstant);

        // 4. Manipulate Instant
        Instant fiveHoursLater = now.plusSeconds(5 * 3600); // Add 5 hours
        System.out.println("Five hours later: " + fiveHoursLater);

        // 5. Convert Instant to ZonedDateTime (needs a ZoneId)
        ZonedDateTime zonedDateTimeUTC = now.atZone(ZoneId.of("UTC"));
        System.out.println("Instant in UTC Zone: " + zonedDateTimeUTC);

        ZonedDateTime zonedDateTimeNY = now.atZone(ZoneId.of("America/New_York"));
        System.out.println("Instant in New York Zone: " + zonedDateTimeNY);

        // Important: Instant is purely UTC. When printed, it might implicitly convert to default system timezone,
        // but its internal value is always based on epoch milliseconds in UTC.
    }
}
```

**Output:**

```
--- Instant Example ---
Current Instant (UTC): 2024-05-15T14:30:45.123456789Z // (Actual instant will vary)
Specific Instant from millis: 2023-03-15T12:00:00Z
Current Instant in milliseconds: 1715783445123
Five hours later: 2024-05-15T19:30:45.123456789Z
Instant in UTC Zone: 2024-05-15T14:30:45.123456789Z[UTC]
Instant in New York Zone: 2024-05-15T10:30:45.123456789-04:00[America/New_York]
```
*(Note: 'Z' in Instant output denotes UTC/Zulu time)*

#### 3.1.5 `ZonedDateTime`

*   Represents a date and time with a specific time zone.
*   Crucial for applications that need to handle different geographical locations or complex time zone rules (like daylight saving).
*   Example: `2024-05-15T10:30:45-04:00[America/New_York]`

```java
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Set;

public class ZonedDateTimeExample {
    public static void main(String[] args) {
        System.out.println("--- ZonedDateTime Example ---");

        // 1. Get current date and time in default system zone
        ZonedDateTime now = ZonedDateTime.now();
        System.out.println("Current ZonedDateTime (Default Zone): " + now);

        // 2. Get current date and time in a specific zone
        ZoneId newYorkZone = ZoneId.of("America/New_York");
        ZonedDateTime nowInNewYork = ZonedDateTime.now(newYorkZone);
        System.out.println("Current ZonedDateTime (New York): " + nowInNewYork);

        ZoneId londonZone = ZoneId.of("Europe/London");
        ZonedDateTime nowInLondon = ZonedDateTime.now(londonZone);
        System.out.println("Current ZonedDateTime (London): " + nowInLondon);

        // 3. Create a specific ZonedDateTime
        ZonedDateTime specificZDT = ZonedDateTime.of(2023, 10, 29, 2, 30, 0, 0, londonZone);
        System.out.println("Specific ZonedDateTime (London, DST change): " + specificZDT);
        // Note: If 2:30 AM on Oct 29, 2023 doesn't exist due to DST, it will adjust.
        // For London 2023, DST ends on Oct 29 at 2AM, so 2:30AM is in the new offset.

        // 4. Convert LocalDateTime to ZonedDateTime
        LocalDateTime localDateTime = LocalDateTime.of(2024, 6, 1, 10, 0); // No zone info
        ZonedDateTime zdtFromLocal = localDateTime.atZone(newYorkZone);
        System.out.println("LocalDateTime to ZonedDateTime (New York): " + zdtFromLocal);

        // 5. Convert Instant to ZonedDateTime
        Instant instant = Instant.now();
        ZonedDateTime zdtFromInstant = instant.atZone(londonZone);
        System.out.println("Instant to ZonedDateTime (London): " + zdtFromInstant);

        // 6. Change time zone (converts the instant in time to the new zone's local time)
        ZonedDateTime convertedToTokyo = nowInNewYork.withZoneSameInstant(ZoneId.of("Asia/Tokyo"));
        System.out.println("New York time converted to Tokyo: " + convertedToTokyo);

        // 7. Manipulate ZonedDateTime
        ZonedDateTime tomorrowInNewYork = nowInNewYork.plusDays(1);
        System.out.println("Tomorrow in New York: " + tomorrowInNewYork);

        // 8. Get time zone information
        System.out.println("Zone ID: " + now.getZone());
        System.out.println("Offset: " + now.getOffset());

        // 9. List available time zone IDs
        System.out.println("\n--- Sample Available Zone IDs ---");
        Set<String> zoneIds = ZoneId.getAvailableZoneIds();
        zoneIds.stream().limit(5).forEach(System.out::println);
        System.out.println("...");
    }
}
```

**Output:**

```
--- ZonedDateTime Example ---
Current ZonedDateTime (Default Zone): 2024-05-15T10:30:45.123456789-04:00[America/New_York] // (Actual date/time will vary)
Current ZonedDateTime (New York): 2024-05-15T10:30:45.123456789-04:00[America/New_York]
Current ZonedDateTime (London): 2024-05-15T15:30:45.123456789+01:00[Europe/London]
Specific ZonedDateTime (London, DST change): 2023-10-29T02:30+00:00[Europe/London] // 2:30 AM *after* DST ends
LocalDateTime to ZonedDateTime (New York): 2024-06-01T10:00-04:00[America/New_York]
Instant to ZonedDateTime (London): 2024-05-15T15:30:45.123456789+01:00[Europe/London]
New York time converted to Tokyo: 2024-05-16T00:30:45.123456789+09:00[Asia/Tokyo]
Tomorrow in New York: 2024-05-16T10:30:45.123456789-04:00[America/New_York]
Zone ID: America/New_York
Offset: -04:00

--- Sample Available Zone IDs ---
Asia/Aden
America/Cuiaba
Etc/GMT+9
Etc/GMT+8
Africa/Nairobi
...
```

### 3.2 Key Concepts and Utility Classes

#### 3.2.1 `Duration`

*   Measures a quantity of time in terms of seconds and nanoseconds.
*   Used for time-based amounts (e.g., "3 hours, 20 minutes, 15 seconds").
*   Best suited for `LocalTime` or `Instant` differences.

```java
import java.time.Duration;
import java.time.Instant;
import java.time.LocalTime;

public class DurationExample {
    public static void main(String[] args) {
        System.out.println("--- Duration Example ---");

        // 1. Create a Duration
        Duration duration = Duration.ofHours(2).plusMinutes(30);
        System.out.println("Duration: " + duration); // PT2H30M (Parse Time 2 Hours 30 Minutes)

        // 2. Calculate duration between two LocalTime
        LocalTime startTime = LocalTime.of(9, 0);
        LocalTime endTime = LocalTime.of(17, 30);
        Duration timeTaken = Duration.between(startTime, endTime);
        System.out.println("Time taken (LocalTime): " + timeTaken);
        System.out.println("Time taken in minutes: " + timeTaken.toMinutes());

        // 3. Calculate duration between two Instants
        Instant startInstant = Instant.now();
        // Simulate some work
        try { Thread.sleep(2000); } catch (InterruptedException e) {}
        Instant endInstant = Instant.now();
        Duration elapsedInstant = Duration.between(startInstant, endInstant);
        System.out.println("Elapsed time (Instant): " + elapsedInstant);
        System.out.println("Elapsed time in milliseconds: " + elapsedInstant.toMillis());

        // 4. Add duration to a time
        LocalTime updatedTime = startTime.plus(duration);
        System.out.println("Start time + Duration: " + updatedTime);
    }
}
```

**Output:**

```
--- Duration Example ---
Duration: PT2H30M
Time taken (LocalTime): PT8H30M
Time taken in minutes: 510
Elapsed time (Instant): PT2.000000XXXS // (Approx. 2 seconds)
Elapsed time in milliseconds: 2000
Start time + Duration: 11:30
```

#### 3.2.2 `Period`

*   Measures a quantity of time in terms of years, months, and days.
*   Used for date-based amounts (e.g., "2 years, 3 months, 5 days").
*   Best suited for `LocalDate` differences.

```java
import java.time.LocalDate;
import java.time.Period;

public class PeriodExample {
    public static void main(String[] args) {
        System.out.println("--- Period Example ---");

        // 1. Create a Period
        Period period = Period.ofYears(1).plusMonths(6).plusDays(10);
        System.out.println("Period: " + period); // P1Y6M10D (Period 1 Year 6 Months 10 Days)

        // 2. Calculate period between two LocalDates
        LocalDate startDate = LocalDate.of(2020, 1, 15);
        LocalDate endDate = LocalDate.of(2023, 5, 20);
        Period dateDifference = Period.between(startDate, endDate);
        System.out.println("Difference in Period: " + dateDifference);
        System.out.println("Years: " + dateDifference.getYears());
        System.out.println("Months: " + dateDifference.getMonths());
        System.out.println("Days: " + dateDifference.getDays());

        // 3. Normalize a Period
        Period normalizedPeriod = Period.ofMonths(15);
        System.out.println("Period 15 months: " + normalizedPeriod);
        System.out.println("Normalized: " + normalizedPeriod.normalized()); // P1Y3M

        // 4. Add period to a date
        LocalDate updatedDate = startDate.plus(period);
        System.out.println("Start date + Period: " + updatedDate);
    }
}
```

**Output:**

```
--- Period Example ---
Period: P1Y6M10D
Difference in Period: P3Y4M5D
Years: 3
Months: 4
Days: 5
Period 15 months: P15M
Normalized: P1Y3M
Start date + Period: 2021-07-25
```

#### 3.2.3 `ChronoUnit`

*   An enum representing standard units of time (e.g., `DAYS`, `HOURS`, `MONTHS`, `YEARS`, `MILLENNIA`).
*   Useful for adding/subtracting specific units and calculating differences between temporal objects.

```java
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.temporal.ChronoUnit;

public class ChronoUnitExample {
    public static void main(String[] args) {
        System.out.println("--- ChronoUnit Example ---");

        LocalDate date1 = LocalDate.of(2023, 1, 1);
        LocalDate date2 = LocalDate.of(2024, 5, 15);

        // 1. Calculate difference in units
        long daysBetween = ChronoUnit.DAYS.between(date1, date2);
        System.out.println("Days between " + date1 + " and " + date2 + ": " + daysBetween);

        long monthsBetween = ChronoUnit.MONTHS.between(date1, date2);
        System.out.println("Months between: " + monthsBetween);

        long yearsBetween = ChronoUnit.YEARS.between(date1, date2);
        System.out.println("Years between: " + yearsBetween);

        // 2. Add/Subtract units using plus()/minus() with ChronoUnit
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime fiveHoursLater = now.plus(5, ChronoUnit.HOURS);
        System.out.println("Five hours later: " + fiveHoursLater);

        LocalTime time = LocalTime.of(10, 30);
        LocalTime nextMinute = time.plus(1, ChronoUnit.MINUTES);
        System.out.println("Next minute: " + nextMinute);
    }
}
```

**Output:**

```
--- ChronoUnit Example ---
Days between 2023-01-01 and 2024-05-15: 500
Months between: 16
Years between: 1
Five hours later: 2024-05-15T15:30:45.123456789
Next minute: 10:31
```

### 3.3 Formatting and Parsing

The `java.time.format.DateTimeFormatter` class is used for converting between date/time objects and their string representations.

*   It's immutable and thread-safe.
*   Provides predefined formatters (`ISO_LOCAL_DATE`, `ISO_DATE_TIME`, etc.).
*   Allows custom pattern-based formatting.

#### Example: `DateTimeFormatter`

```java
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.FormatStyle;
import java.util.Locale;

public class DateTimeFormatterExample {
    public static void main(String[] args) {
        System.out.println("--- DateTimeFormatter Example ---");

        LocalDateTime now = LocalDateTime.now();
        LocalDate today = LocalDate.now();
        LocalTime currentTime = LocalTime.now();
        ZonedDateTime zdt = ZonedDateTime.now();

        // --- 1. Predefined Formatters ---
        System.out.println("\n--- Predefined Formatters ---");
        System.out.println("ISO Local Date: " + today.format(DateTimeFormatter.ISO_LOCAL_DATE)); // 2024-05-15
        System.out.println("ISO Local Time: " + currentTime.format(DateTimeFormatter.ISO_LOCAL_TIME)); // 10:30:45.123456789
        System.out.println("ISO Local Date Time: " + now.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME)); // 2024-05-15T10:30:45.123456789
        System.out.println("ISO Zoned Date Time: " + zdt.format(DateTimeFormatter.ISO_ZONED_DATE_TIME)); // 2024-05-15T10:30:45.123456789-04:00[America/New_York]

        // --- 2. FormatStyle (Locale-sensitive) ---
        System.out.println("\n--- FormatStyle (Locale-sensitive) ---");
        DateTimeFormatter shortDate = DateTimeFormatter.ofLocalizedDate(FormatStyle.SHORT);
        System.out.println("Short Date (Default Locale): " + today.format(shortDate)); // 5/15/24 (for US)

        DateTimeFormatter mediumDateTime = DateTimeFormatter.ofLocalizedDateTime(FormatStyle.MEDIUM)
                                                    .withLocale(Locale.UK); // Specify locale
        System.out.println("Medium DateTime (UK Locale): " + now.format(mediumDateTime)); // 15 May 2024, 10:30:45

        // --- 3. Custom Patterns ---
        System.out.println("\n--- Custom Patterns ---");
        // yyyy: year (e.g., 2024)
        // MM: month (01-12)
        // dd: day of month (01-31)
        // HH: hour (00-23)
        // mm: minute (00-59)
        // ss: second (00-59)
        // SSS: milliseconds
        // EEE: day of week short (Mon)
        // EEEE: day of week full (Monday)
        // a: AM/PM
        // zzz: time zone abbreviation (EST)
        // Z: time zone offset (+0000)
        // X: ISO 8601 offset (+04, +0400, +04:00)
        // For full list: https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html

        DateTimeFormatter customFormatter = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss EEEE");
        System.out.println("Custom Formatted: " + now.format(customFormatter)); // 2024/05/15 10:30:45 Wednesday

        DateTimeFormatter timeWithAmPm = DateTimeFormatter.ofPattern("hh:mm:ss a");
        System.out.println("Time with AM/PM: " + currentTime.format(timeWithAmPm)); // 10:30:45 AM

        DateTimeFormatter zdtCustomFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss zzzz");
        System.out.println("ZonedDateTime Custom: " + zdt.format(zdtCustomFormatter)); // 2024-05-15 10:30:45 Eastern Daylight Time

        // --- 4. Parsing Strings into Date-Time Objects ---
        System.out.println("\n--- Parsing Strings ---");
        String dateToParse = "2023-01-25";
        LocalDate parsedLocalDate = LocalDate.parse(dateToParse);
        System.out.println("Parsed LocalDate: " + parsedLocalDate);

        String dateTimeToParse = "2022-12-31 23:59:59";
        // Need to use a formatter that matches the string format
        DateTimeFormatter parser = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        LocalDateTime parsedLocalDateTime = LocalDateTime.parse(dateTimeToParse, parser);
        System.out.println("Parsed LocalDateTime: " + parsedLocalDateTime);

        String zonedDateTimeToParse = "2021-07-04 14:00:00 America/Los_Angeles";
        DateTimeFormatter zdtParser = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss VV"); // VV for Zone ID
        ZonedDateTime parsedZonedDateTime = ZonedDateTime.parse(zonedDateTimeToParse, zdtParser);
        System.out.println("Parsed ZonedDateTime: " + parsedZonedDateTime);
    }
}
```

**Output:**

```
--- DateTimeFormatter Example ---

--- Predefined Formatters ---
ISO Local Date: 2024-05-15
ISO Local Time: 10:30:45.123456789
ISO Local Date Time: 2024-05-15T10:30:45.123456789
ISO Zoned Date Time: 2024-05-15T10:30:45.123456789-04:00[America/New_York]

--- FormatStyle (Locale-sensitive) ---
Short Date (Default Locale): 5/15/24
Medium DateTime (UK Locale): 15 May 2024, 10:30:45

--- Custom Patterns ---
Custom Formatted: 2024/05/15 10:30:45 Wednesday
Time with AM/PM: 10:30:45 AM
ZonedDateTime Custom: 2024-05-15 10:30:45 Eastern Daylight Time

--- Parsing Strings ---
Parsed LocalDate: 2023-01-25
Parsed LocalDateTime: 2022-12-31T23:59:59
Parsed ZonedDateTime: 2021-07-04T14:00-07:00[America/Los_Angeles]
```

### 3.4 Converting Between Old and New API

Sometimes you'll need to interoperate with legacy code or APIs that still use `java.util.Date` or `java.util.Calendar`.

#### Example: Conversions

```java
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Calendar;
import java.util.Date;

public class ConversionExample {
    public static void main(String[] args) {
        System.out.println("--- Conversion Example ---");

        // --- Old to New API ---

        // 1. java.util.Date to java.time.Instant
        Date oldDate = new Date(); // Current date and time
        Instant instantFromDate = oldDate.toInstant();
        System.out.println("Date to Instant: " + oldDate + " -> " + instantFromDate);

        // 2. java.util.Date to java.time.LocalDateTime (requires a ZoneId)
        // If you don't specify a zone, Instant.atZone(ZoneId.systemDefault()) is commonly used
        ZoneId defaultZone = ZoneId.systemDefault();
        LocalDateTime localDateTimeFromDate = instantFromDate.atZone(defaultZone).toLocalDateTime();
        System.out.println("Date to LocalDateTime (via Instant): " + oldDate + " -> " + localDateTimeFromDate);

        // 3. java.util.Calendar to java.time.ZonedDateTime
        Calendar oldCalendar = Calendar.getInstance(); // Current date and time in default zone
        ZonedDateTime zonedDateTimeFromCalendar = oldCalendar.toInstant().atZone(oldCalendar.getTimeZone().toZoneId());
        System.out.println("Calendar to ZonedDateTime: " + oldCalendar.getTime() + " -> " + zonedDateTimeFromCalendar);


        // --- New to Old API ---

        // 1. java.time.Instant to java.util.Date
        Instant newInstant = Instant.now();
        Date dateFromInstant = Date.from(newInstant);
        System.out.println("Instant to Date: " + newInstant + " -> " + dateFromInstant);

        // 2. java.time.ZonedDateTime to java.util.Date
        ZonedDateTime newZonedDateTime = ZonedDateTime.now();
        Date dateFromZonedDateTime = Date.from(newZonedDateTime.toInstant());
        System.out.println("ZonedDateTime to Date: " + newZonedDateTime + " -> " + dateFromZonedDateTime);

        // 3. java.time.LocalDateTime to java.util.Date (requires a ZoneId)
        LocalDateTime newLocalDateTime = LocalDateTime.now();
        Date dateFromLocalDateTime = Date.from(newLocalDateTime.atZone(defaultZone).toInstant());
        System.out.println("LocalDateTime to Date (via default Zone): " + newLocalDateTime + " -> " + dateFromLocalDateTime);

        // 4. java.time.ZonedDateTime to java.util.Calendar
        ZonedDateTime newZdtForCalendar = ZonedDateTime.now(ZoneId.of("America/Los_Angeles"));
        Calendar calendarFromZdt = Calendar.getInstance(java.util.TimeZone.getTimeZone(newZdtForCalendar.getZone()));
        calendarFromZdt.setTimeInMillis(newZdtForCalendar.toInstant().toEpochMilli());
        System.out.println("ZonedDateTime to Calendar: " + newZdtForCalendar + " -> " + calendarFromZdt.getTime());
    }
}
```

**Output:**

```
--- Conversion Example ---
Date to Instant: Wed May 15 10:30:45 EDT 2024 -> 2024-05-15T14:30:45.123456789Z
Date to LocalDateTime (via Instant): Wed May 15 10:30:45 EDT 2024 -> 2024-05-15T10:30:45.123456789
Calendar to ZonedDateTime: Wed May 15 10:30:45 EDT 2024 -> 2024-05-15T10:30:45.123456789-04:00[America/New_York]
Instant to Date: 2024-05-15T14:30:45.123456789Z -> Wed May 15 10:30:45 EDT 2024
ZonedDateTime to Date: 2024-05-15T10:30:45.123456789-04:00[America/New_York] -> Wed May 15 10:30:45 EDT 2024
LocalDateTime to Date (via default Zone): 2024-05-15T10:30:45.123456789 -> Wed May 15 10:30:45 EDT 2024
ZonedDateTime to Calendar: 2024-05-15T07:30:45.123456789-07:00[America/Los_Angeles] -> Wed May 15 07:30:45 PDT 2024
```

## 4. Best Practices

*   **Always use `java.time` for new code.** Avoid `java.util.Date` and `java.util.Calendar` unless you are dealing with legacy APIs.
*   **Be explicit about time zones.** If your application deals with users in different locations, `ZonedDateTime` is your friend.
*   **Store `Instant` or UTC `LocalDateTime` in databases.** When saving timestamps, it's generally best to store them in UTC to avoid time zone conversion issues. Use `Instant` for precise point-in-time stamps. If a database only supports `DATETIME` without time zone, store `LocalDateTime` that has been converted from a `ZonedDateTime` to UTC.
*   **Use `LocalDate` and `LocalTime` when no time zone is relevant.** For birthdays, anniversaries, or daily recurring events (like store opening hours that are the "same local time" everywhere), these are perfect.
*   **Use `LocalDateTime` when a specific date and time are needed, but the time zone context is handled implicitly or externally.** E.g., a "meeting start time" for an event that will always be interpreted in the user's local time, or when all times are already assumed to be in UTC.
*   **Use `DateTimeFormatter` for all parsing and formatting.** Never rely on `toString()` for display or `Date` constructors for parsing. Always specify a `Locale` if the format is locale-sensitive (e.g., month names, date order).
*   **Understand `Duration` vs. `Period`.** `Duration` for time-based amounts (hours, minutes), `Period` for date-based amounts (years, months, days).

## 5. Conclusion

The `java.time` package has significantly improved date and time handling in Java, making it more intuitive, robust, and less prone to errors. By embracing its immutable classes and clear separation of concerns (date, time, instant, time-zone-aware), developers can write more reliable and maintainable code when dealing with temporal data.