The concept of `datetime` in Java has evolved significantly over the years. Before Java 8, handling dates and times was notoriously cumbersome and error-prone. With Java 8, a new, much-improved Date and Time API (JSR 310, inspired by Joda-Time) was introduced in the `java.time` package, fundamentally changing how we work with dates and times.

This guide will cover both:
1.  **The Legacy Date/Time API (Pre-Java 8):** `java.util.Date`, `java.util.Calendar`, `java.text.SimpleDateFormat`.
2.  **The Modern Date/Time API (Java 8+):** Classes in the `java.time` package.

---

# Date and Time in Java

## 1. The Legacy Date/Time API (Pre-Java 8)

Before Java 8, working with dates and times was often a source of frustration for developers due to its mutable nature, lack of thread-safety, and confusing API design (e.g., months starting from 0).

### 1.1 `java.util.Date`

Represents a specific instant in time, with millisecond precision. It's essentially a wrapper around a `long` value representing milliseconds since the [Unix epoch](https://en.wikipedia.org/wiki/Unix_time) (January 1, 1970, 00:00:00 GMT).

**Problems:**
*   **Mutable:** Its state can be changed after creation, leading to unexpected side effects, especially in multi-threaded environments.
*   **Poor API:** Many methods are deprecated (e.g., `getYear()`, `getMonth()`, `getDate()`) because they don't follow modern API design principles and were confusing.
*   **No Timezone Information:** It doesn't inherently store timezone information, leading to ambiguity. `toString()` uses the default timezone of the JVM.

**Examples:**

```java
import java.util.Date;

public class LegacyDateExample {
    public static void main(String[] args) {
        // 1. Creating a Date object
        Date now = new Date(); // Current date and time
        System.out.println("Current Date (now): " + now);

        // 2. Creating a Date from milliseconds
        long milliseconds = 1678886400000L; // March 15, 2023 00:00:00 GMT
        Date specificDate = new Date(milliseconds);
        System.out.println("Specific Date (from millis): " + specificDate);

        // 3. Comparison
        Date futureDate = new Date(now.getTime() + 3600 * 1000); // 1 hour from now
        System.out.println("Is now before futureDate? " + now.before(futureDate)); // true
        System.out.println("Is futureDate after now? " + futureDate.after(now));   // true

        // 4. Getting time in milliseconds
        System.out.println("Milliseconds since epoch for now: " + now.getTime());

        // Note: Methods like getYear(), getMonth() are deprecated and should be avoided.
        // They return values relative to 1900 and 0-indexed months, respectively.
    }
}
```

### 1.2 `java.util.Calendar`

An abstract base class for converting between a `Date` object and a set of integer fields such as `YEAR`, `MONTH`, `DAY_OF_MONTH`, `HOUR`, etc. It was designed to address some of the shortcomings of `Date`, especially for date manipulation and component extraction.

**Problems:**
*   **Mutable:** Like `Date`, it's mutable.
*   **Complex API:** Using integer constants (`Calendar.MONTH`, `Calendar.DAY_OF_WEEK`) makes the code less readable.
*   **0-indexed Months:** `Calendar.JANUARY` is 0, `Calendar.FEBRUARY` is 1, etc., a common source of bugs.
*   **Not Thread-Safe:** Concurrent modification issues can arise.

**Examples:**

```java
import java.util.Calendar;
import java.util.Date;

public class LegacyCalendarExample {
    public static void main(String[] args) {
        // 1. Getting a Calendar instance (usually GregorianCalendar)
        Calendar calendar = Calendar.getInstance(); // Current date and time
        System.out.println("Current Calendar: " + calendar.getTime());

        // 2. Setting specific date and time components
        calendar.set(2023, Calendar.OCTOBER, 26, 10, 30, 0); // Month is 0-indexed (OCTOBER is 9)
        System.out.println("Set Date: " + calendar.getTime());

        // 3. Getting specific components
        System.out.println("Year: " + calendar.get(Calendar.YEAR));
        System.out.println("Month (0-indexed): " + calendar.get(Calendar.MONTH)); // 9 for October
        System.out.println("Day of Month: " + calendar.get(Calendar.DAY_OF_MONTH));
        System.out.println("Hour of Day (24-hour): " + calendar.get(Calendar.HOUR_OF_DAY));

        // 4. Adding/Subtracting time
        calendar.add(Calendar.DAY_OF_MONTH, 5); // Add 5 days
        System.out.println("Date after adding 5 days: " + calendar.getTime());

        calendar.add(Calendar.HOUR, -2); // Subtract 2 hours
        System.out.println("Date after subtracting 2 hours: " + calendar.getTime());

        // 5. Converting Calendar to Date
        Date dateFromCalendar = calendar.getTime();
        System.out.println("Date from Calendar: " + dateFromCalendar);
    }
}
```

### 1.3 `java.text.SimpleDateFormat`

Used for formatting dates into strings and parsing strings into `Date` objects. It allows you to define custom date and time patterns.

**Problems:**
*   **Not Thread-Safe:** Multiple threads using the same `SimpleDateFormat` instance concurrently can lead to incorrect results. It's often advised to create a new instance for each thread or use `ThreadLocal`.
*   **Verbose:** Requires creating an instance and handling `ParseException`.
*   **Pattern Letters:** The pattern letters (e.g., `yyyy`, `MM`, `dd`, `HH`, `mm`, `ss`) can be tricky to remember.

**Examples:**

```java
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class LegacyDateFormatExample {
    public static void main(String[] args) {
        Date now = new Date();

        // 1. Formatting Date to String
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss EEEE"); // EEEE for full day name
        String formattedDate = formatter.format(now);
        System.out.println("Formatted Date: " + formattedDate);

        // Custom format
        SimpleDateFormat customFormatter = new SimpleDateFormat("dd/MM/yyyy 'at' hh:mm a"); // 'a' for AM/PM
        String customFormattedDate = customFormatter.format(now);
        System.out.println("Custom Formatted Date: " + customFormattedDate);

        // 2. Parsing String to Date
        String dateString = "2023-01-15 14:30:00";
        SimpleDateFormat parser = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        try {
            Date parsedDate = parser.parse(dateString);
            System.out.println("Parsed Date: " + parsedDate);
        } catch (ParseException e) {
            System.err.println("Error parsing date: " + e.getMessage());
        }

        // 3. Thread-safety warning (demonstration, not actual multi-threading)
        // In a real multi-threaded scenario, this single instance would be problematic.
        // It's generally better to create a new instance per use or use ThreadLocal.
        SimpleDateFormat threadUnsafeFormatter = new SimpleDateFormat("yyyy-MM-dd");
        String date1 = threadUnsafeFormatter.format(new Date(1672531200000L)); // Jan 1, 2023
        String date2 = threadUnsafeFormatter.format(new Date(1675209600000L)); // Feb 1, 2023
        System.out.println("Thread-unsafe dates: " + date1 + ", " + date2);
    }
}
```

---

## 2. The Modern Date/Time API (Java 8+) - `java.time` Package

The `java.time` package was introduced to address all the issues of the legacy API. It offers a comprehensive set of classes for handling dates, times, instants, and durations with better design principles.

**Key Design Principles:**
*   **Immutability:** All core classes in `java.time` are immutable, making them inherently thread-safe and easier to reason about. Operations like `plusDays()` return a *new* object.
*   **Clarity:** Clear separation between date-only (`LocalDate`), time-only (`LocalTime`), date-time (`LocalDateTime`), and date-time with timezone (`ZonedDateTime`).
*   **Fluency:** Method chaining (e.g., `now().plusDays(1).plusHours(2)`) makes code more readable.
*   **Domain-driven:** Classes are named clearly according to their purpose.
*   **ISO 8601 Compliance:** Most classes adhere to the ISO 8601 standard for date and time representation (e.g., `2023-10-26T14:30:00`).

### Core Classes:

*   **`LocalDate`**: A date without a time or timezone (e.g., `2023-10-26`).
*   **`LocalTime`**: A time without a date or timezone (e.g., `14:30:00`).
*   **`LocalDateTime`**: A date-time without a timezone (e.g., `2023-10-26T14:30:00`).
*   **`Instant`**: A point in time on the timeline (e.g., `2023-10-26T12:00:00Z`). Primarily for machine-readable time, often used for timestamps.
*   **`ZonedDateTime`**: A date-time with a timezone (e.g., `2023-10-26T14:30:00-04:00[America/New_York]`).
*   **`OffsetDateTime`**: A date-time with a timezone offset from UTC/Greenwich (e.g., `2023-10-26T14:30:00-04:00`). Useful for database storage where the specific timezone isn't needed, but the offset is.
*   **`Duration`**: A time-based amount of time, like '3 hours, 30 minutes'.
*   **`Period`**: A date-based amount of time, like '2 years, 3 months, 5 days'.
*   **`DateTimeFormatter`**: For formatting and parsing date-time objects (thread-safe!).
*   **`TemporalAdjusters`**: For complex date adjustments (e.g., "next Sunday", "last day of the month").
*   **`ZoneId`**: Represents a timezone (e.g., `America/New_York`).
*   **`ZoneOffset`**: Represents a fixed offset from Greenwich (e.g., `-04:00`).

---

### 2.1 `LocalDate` - Date Without Time or Timezone

**Purpose:** Represents a date (year, month, day) without a time of day or a time-zone.

**Examples:**

```java
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.Month;

public class LocalDateExample {
    public static void main(String[] args) {
        // 1. Current Date
        LocalDate today = LocalDate.now();
        System.out.println("Today: " + today); // e.g., 2023-10-26

        // 2. Specific Date
        LocalDate specificDate = LocalDate.of(2023, 1, 15); // Year, Month (enum), Day
        LocalDate anotherSpecificDate = LocalDate.of(2024, Month.FEBRUARY, 29); // Using Month enum
        System.out.println("Specific Date: " + specificDate);
        System.out.println("Another Specific Date (Leap Year): " + anotherSpecificDate);

        // 3. Parsing a String to LocalDate (ISO 8601 format by default)
        LocalDate parsedDate = LocalDate.parse("2022-12-25");
        System.out.println("Parsed Date: " + parsedDate);

        // 4. Getting Date Components
        System.out.println("Year: " + today.getYear());
        System.out.println("Month: " + today.getMonth());             // OCTOBER (enum)
        System.out.println("Month value: " + today.getMonthValue()); // 10
        System.out.println("Day of Month: " + today.getDayOfMonth());
        System.out.println("Day of Week: " + today.getDayOfWeek());   // THURSDAY (enum)
        System.out.println("Day of Year: " + today.getDayOfYear());
        System.out.println("Is Leap Year? " + today.isLeapYear());

        // 5. Modifying Dates (returns new instances because LocalDate is immutable)
        LocalDate tomorrow = today.plusDays(1);
        System.out.println("Tomorrow: " + tomorrow);

        LocalDate lastMonth = today.minusMonths(1);
        System.out.println("Last Month: " + lastMonth);

        LocalDate nextYearSameDay = today.plusYears(1);
        System.out.println("Next Year Same Day: " + nextYearSameDay);

        // Setting a specific field
        LocalDate firstDayOfNextMonth = today.plusMonths(1).withDayOfMonth(1);
        System.out.println("First day of next month: " + firstDayOfNextMonth);

        // 6. Comparison
        LocalDate christmas2023 = LocalDate.of(2023, 12, 25);
        System.out.println("Is today before Christmas 2023? " + today.isBefore(christmas2023));
        System.out.println("Is today after Christmas 2023? " + today.isAfter(christmas2023));
        System.out.println("Is today equal to 2023-10-26? " + today.isEqual(LocalDate.of(2023, 10, 26)));
    }
}
```

### 2.2 `LocalTime` - Time Without Date or Timezone

**Purpose:** Represents a time of day without a date or a time-zone.

**Examples:**

```java
import java.time.LocalTime;
import java.time.temporal.ChronoUnit;

public class LocalTimeExample {
    public static void main(String[] args) {
        // 1. Current Time
        LocalTime now = LocalTime.now();
        System.out.println("Current Time: " + now); // e.g., 14:30:45.123456789

        // 2. Specific Time
        LocalTime specificTime = LocalTime.of(10, 30, 45); // Hour, Minute, Second
        LocalTime specificTimeNano = LocalTime.of(10, 30, 45, 500_000_000); // Hour, Minute, Second, Nanosecond
        System.out.println("Specific Time: " + specificTime);
        System.out.println("Specific Time with Nanos: " + specificTimeNano);

        // 3. Parsing a String to LocalTime (ISO 8601 format by default)
        LocalTime parsedTime = LocalTime.parse("23:59:59");
        System.out.println("Parsed Time: " + parsedTime);

        // 4. Getting Time Components
        System.out.println("Hour: " + now.getHour());
        System.out.println("Minute: " + now.getMinute());
        System.out.println("Second: " + now.getSecond());
        System.out.println("Nanosecond: " + now.getNano());

        // 5. Modifying Times (returns new instances)
        LocalTime oneHourLater = now.plusHours(1);
        System.out.println("One Hour Later: " + oneHourLater);

        LocalTime fifteenMinutesAgo = now.minusMinutes(15);
        System.out.println("Fifteen Minutes Ago: " + fifteenMinutesAgo);

        LocalTime truncatedToSeconds = now.truncatedTo(ChronoUnit.SECONDS); // Remove nanos
        System.out.println("Truncated to Seconds: " + truncatedToSeconds);

        // 6. Comparison
        LocalTime morning = LocalTime.of(9, 0);
        LocalTime evening = LocalTime.of(18, 0);
        System.out.println("Is " + morning + " before " + evening + "? " + morning.isBefore(evening));
        System.out.println("Is " + evening + " after " + morning + "? " + evening.isAfter(morning));
    }
}
```

### 2.3 `LocalDateTime` - Date and Time Without Timezone

**Purpose:** Represents a date and time without any timezone information. It's often used when you store date-time information in a database without considering specific timezones.

**Examples:**

```java
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.Month;

public class LocalDateTimeExample {
    public static void main(String[] args) {
        // 1. Current Date and Time
        LocalDateTime now = LocalDateTime.now();
        System.out.println("Current LocalDateTime: " + now); // e.g., 2023-10-26T14:30:45.123

        // 2. Specific Date and Time
        LocalDateTime specificDateTime = LocalDateTime.of(2023, Month.JANUARY, 1, 10, 30, 0);
        System.out.println("Specific LocalDateTime: " + specificDateTime);

        // 3. Combining LocalDate and LocalTime
        LocalDate date = LocalDate.of(2024, 7, 20);
        LocalTime time = LocalTime.of(16, 45);
        LocalDateTime combinedDateTime = LocalDateTime.of(date, time);
        System.out.println("Combined LocalDateTime: " + combinedDateTime);

        // 4. Parsing a String to LocalDateTime (ISO 8601 format by default: YYYY-MM-DDTHH:MM:SS)
        LocalDateTime parsedDateTime = LocalDateTime.parse("2023-05-10T08:00:00");
        System.out.println("Parsed LocalDateTime: " + parsedDateTime);

        // 5. Getting Components (similar to LocalDate and LocalTime)
        System.out.println("Year: " + now.getYear());
        System.out.println("Hour: " + now.getHour());

        // 6. Modifying Date and Time
        LocalDateTime futureDateTime = now.plusDays(7).minusHours(3);
        System.out.println("Future LocalDateTime: " + futureDateTime);

        // 7. Extracting LocalDate or LocalTime
        LocalDate extractedDate = now.toLocalDate();
        LocalTime extractedTime = now.toLocalTime();
        System.out.println("Extracted Date: " + extractedDate);
        System.out.println("Extracted Time: " + extractedTime);

        // 8. Comparison
        LocalDateTime pastDateTime = LocalDateTime.of(2023, 1, 1, 0, 0);
        System.out.println("Is " + now + " before " + pastDateTime + "? " + now.isBefore(pastDateTime));
    }
}
```

### 2.4 `Instant` - A Point in Time (Machine Readable)

**Purpose:** Represents a point in time, independent of any time-zone, in nanoseconds precision since the Unix epoch (January 1, 1970, 00:00:00 GMT). It's primarily for recording event timestamps.

**Examples:**

```java
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;

public class InstantExample {
    public static void main(String[] args) {
        // 1. Current Instant
        Instant now = Instant.now();
        System.out.println("Current Instant: " + now); // e.g., 2023-10-26T12:00:00.123456789Z (Z indicates UTC)

        // 2. Instant from Epoch Milliseconds/Seconds
        Instant fromMillis = Instant.ofEpochMilli(System.currentTimeMillis());
        Instant fromSeconds = Instant.ofEpochSecond(1678886400); // March 15, 2023 00:00:00 GMT
        System.out.println("Instant from Millis: " + fromMillis);
        System.out.println("Instant from Seconds: " + fromSeconds);

        // 3. Converting Instant to Epoch Milliseconds/Seconds
        long epochMillis = now.toEpochMilli();
        long epochSeconds = now.getEpochSecond(); // Truncates nanoseconds
        System.out.println("Epoch Millis: " + epochMillis);
        System.out.println("Epoch Seconds: " + epochSeconds);

        // 4. Adding/Subtracting Time
        Instant oneHourLater = now.plusSeconds(3600);
        System.out.println("Instant one hour later: " + oneHourLater);

        // 5. Converting Instant to LocalDateTime/ZonedDateTime (requires timezone)
        LocalDateTime localDateTimeFromInstant = LocalDateTime.ofInstant(now, ZoneId.systemDefault());
        System.out.println("LocalDateTime from Instant (System Default Zone): " + localDateTimeFromInstant);

        LocalDateTime localDateTimeFromInstantNY = LocalDateTime.ofInstant(now, ZoneId.of("America/New_York"));
        System.out.println("LocalDateTime from Instant (New York Zone): " + localDateTimeFromInstantNY);
    }
}
```

### 2.5 `ZonedDateTime` - Date, Time, and Timezone

**Purpose:** Represents a complete date and time, including the time-zone information. It's the most comprehensive date-time class, crucial for handling daylight saving time (DST) and internationalization.

**Examples:**

```java
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;

public class ZonedDateTimeExample {
    public static void main(String[] args) {
        // 1. Current ZonedDateTime in System Default Timezone
        ZonedDateTime now = ZonedDateTime.now();
        System.out.println("Current ZonedDateTime: " + now); // e.g., 2023-10-26T14:30:45.123-04:00[America/New_York]

        // 2. Specific ZonedDateTime in a specific Timezone
        ZoneId newYorkZone = ZoneId.of("America/New_York");
        ZonedDateTime specificInNY = ZonedDateTime.of(2023, 1, 15, 10, 30, 0, 0, newYorkZone);
        System.out.println("Specific ZonedDateTime in NY: " + specificInNY);

        // From LocalDateTime and ZoneId
        LocalDateTime localDateTime = LocalDateTime.of(2023, 10, 27, 9, 0);
        ZonedDateTime zdtFromLocal = ZonedDateTime.of(localDateTime, ZoneId.of("Europe/London"));
        System.out.println("ZonedDateTime from LocalDateTime + ZoneId: " + zdtFromLocal);

        // 3. Changing Timezone (while keeping the same *moment* in time)
        ZonedDateTime newYorkNow = ZonedDateTime.now(ZoneId.of("America/New_York"));
        ZonedDateTime londonNow = newYorkNow.withZoneSameInstant(ZoneId.of("Europe/London"));
        System.out.println("New York Now: " + newYorkNow);
        System.out.println("Same moment in London: " + londonNow);

        // 4. Changing Timezone (while keeping the same *local* date-time)
        // This is tricky and can lead to different instants, especially during DST changes.
        ZonedDateTime fixedLocalInLondon = newYorkNow.withZoneSameLocal(ZoneId.of("Europe/London"));
        System.out.println("Same local time in London: " + fixedLocalInLondon);
        System.out.println("(Notice the instant/offset difference compared to 'Same moment in London')");


        // 5. Handling Daylight Saving Time (DST)
        // Consider a date when DST changes (e.g., Nov 5, 2023, 2 AM in America/New_York, clock falls back)
        ZoneId newYork = ZoneId.of("America/New_York");
        // An invalid time during DST transition (clock skips forward)
        try {
            ZonedDateTime skippedTime = ZonedDateTime.of(2023, 3, 12, 2, 30, 0, 0, newYork);
            System.out.println("Skipped time (should adjust): " + skippedTime); // Will adjust to 3:30 AM
        } catch (java.time.DateTimeException e) {
            System.out.println("Error for skipped time: " + e.getMessage()); // Or will adjust
        }

        // An ambiguous time during DST transition (clock falls back, 1 AM occurs twice)
        try {
            ZonedDateTime ambiguousTime = ZonedDateTime.of(2023, 11, 5, 1, 30, 0, 0, newYork);
            System.out.println("Ambiguous time (default to first occurrence): " + ambiguousTime);
            // You can control resolution for ambiguous times:
            // .resolveLocal(ResolverStyle.STRICT) // Throws exception for ambiguous/skipped
            // .resolveLocal(ResolverStyle.LENIENT) // Always resolve to valid (may be different instant)
            // .resolveLocal(ResolverStyle.SMART) // Default, tries to do the right thing
        } catch (java.time.DateTimeException e) {
            System.out.println("Error for ambiguous time: " + e.getMessage());
        }

        // 6. Converting to Instant
        System.out.println("Instant from ZonedDateTime: " + now.toInstant());
    }
}
```

### 2.6 `Duration` - Time-based Amount

**Purpose:** Represents a quantity of time in terms of seconds and nanoseconds. Useful for measuring time between two `Instant` or `LocalTime` objects.

**Examples:**

```java
import java.time.Duration;
import java.time.Instant;
import java.time.LocalTime;

public class DurationExample {
    public static void main(String[] args) throws InterruptedException {
        // 1. Creating Durations
        Duration threeHours = Duration.ofHours(3);
        Duration fifteenMinutes = Duration.ofMinutes(15);
        Duration tenSeconds = Duration.ofSeconds(10);
        Duration fiftyMillis = Duration.ofMillis(50);

        System.out.println("Three Hours: " + threeHours);
        System.out.println("Fifteen Minutes: " + fifteenMinutes);

        // 2. Calculating Duration between two points in time
        LocalTime start = LocalTime.of(9, 0);
        LocalTime end = LocalTime.of(12, 30);
        Duration timeElapsed = Duration.between(start, end);
        System.out.println("Time elapsed between " + start + " and " + end + ": " + timeElapsed);

        Instant startInstant = Instant.now();
        Thread.sleep(2500); // Simulate some work
        Instant endInstant = Instant.now();
        Duration workDuration = Duration.between(startInstant, endInstant);
        System.out.println("Work duration: " + workDuration.toMillis() + " ms");

        // 3. Accessing components
        System.out.println("Total seconds in timeElapsed: " + timeElapsed.getSeconds());
        System.out.println("Total minutes in timeElapsed: " + timeElapsed.toMinutes());
        System.out.println("Total hours in timeElapsed: " + timeElapsed.toHours());

        // 4. Adding/Subtracting Durations
        Duration combinedDuration = threeHours.plus(fifteenMinutes);
        System.out.println("Combined Duration: " + combinedDuration);

        Duration remainingDuration = combinedDuration.minus(Duration.ofHours(1));
        System.out.println("Remaining Duration: " + remainingDuration);
    }
}
```

### 2.7 `Period` - Date-based Amount

**Purpose:** Represents a quantity of time in terms of years, months, and days. Useful for measuring periods between two `LocalDate` objects.

**Examples:**

```java
import java.time.LocalDate;
import java.time.Period;

public class PeriodExample {
    public static void main(String[] args) {
        // 1. Creating Periods
        Period fiveYears = Period.ofYears(5);
        Period twoMonths = Period.ofMonths(2);
        Period tenDays = Period.ofDays(10);
        Period mixedPeriod = Period.of(1, 6, 15); // 1 year, 6 months, 15 days

        System.out.println("Five Years: " + fiveYears);
        System.out.println("Mixed Period: " + mixedPeriod);

        // 2. Calculating Period between two dates
        LocalDate startDate = LocalDate.of(2023, 1, 15);
        LocalDate endDate = LocalDate.of(2025, 5, 20);
        Period periodBetween = Period.between(startDate, endDate);
        System.out.println("Period between " + startDate + " and " + endDate + ": " + periodBetween);

        System.out.println("Years: " + periodBetween.getYears());
        System.out.println("Months: " + periodBetween.getMonths());
        System.out.println("Days: " + periodBetween.getDays());

        // 3. Adding/Subtracting Periods to/from dates
        LocalDate today = LocalDate.now();
        LocalDate futureDate = today.plus(mixedPeriod);
        System.out.println("Today: " + today);
        System.out.println("Today plus mixed period: " + futureDate);

        // 4. Normalizing a Period (e.g., converting 18 months to 1 year and 6 months)
        Period periodToNormalize = Period.ofMonths(18);
        System.out.println("Period to Normalize: " + periodToNormalize);
        System.out.println("Normalized: " + periodToNormalize.normalized()); // P1Y6M
    }
}
```

### 2.8 `DateTimeFormatter` - Formatting and Parsing

**Purpose:** Thread-safe class for formatting `java.time` objects into strings and parsing strings back into `java.time` objects. It replaces `SimpleDateFormat` and is the recommended way to handle date-time string conversions.

**Examples:**

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
        LocalDateTime now = LocalDateTime.now();
        ZonedDateTime zdtNow = ZonedDateTime.now();
        LocalDate today = LocalDate.now();

        // 1. Using predefined formatters
        String isoDate = today.format(DateTimeFormatter.ISO_LOCAL_DATE);
        System.out.println("ISO Local Date: " + isoDate); // 2023-10-26

        String isoDateTime = now.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
        System.out.println("ISO Local DateTime: " + isoDateTime); // 2023-10-26T14:30:45.123

        String isoZoned = zdtNow.format(DateTimeFormatter.ISO_ZONED_DATE_TIME);
        System.out.println("ISO Zoned DateTime: " + isoZoned); // 2023-10-26T14:30:45.123-04:00[America/New_York]

        // 2. Using pattern strings (similar to SimpleDateFormat, but thread-safe)
        DateTimeFormatter customFormatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss");
        String formattedCustom = now.format(customFormatter);
        System.out.println("Custom formatted: " + formattedCustom); // 26/10/2023 14:30:45

        DateTimeFormatter dateOnlyFormatter = DateTimeFormatter.ofPattern("EEEE, MMMM dd, yyyy");
        String formattedDateOnly = today.format(dateOnlyFormatter);
        System.out.println("Date only formatted: " + formattedDateOnly); // Thursday, October 26, 2023

        // 3. Using localized styles
        String localizedDate = today.format(DateTimeFormatter.ofLocalizedDate(FormatStyle.FULL));
        System.out.println("Localized Date (FULL): " + localizedDate); // Thursday, October 26, 2023

        String localizedDateTime = now.format(DateTimeFormatter.ofLocalizedDateTime(FormatStyle.MEDIUM));
        System.out.println("Localized DateTime (MEDIUM): " + localizedDateTime); // Oct 26, 2023, 2:30:45 PM

        // Localized for a different locale
        DateTimeFormatter frLocaleFormatter = DateTimeFormatter
                                                .ofLocalizedDateTime(FormatStyle.MEDIUM)
                                                .withLocale(Locale.FRENCH);
        String frenchDateTime = now.format(frLocaleFormatter);
        System.out.println("French DateTime (MEDIUM): " + frenchDateTime); // 26 oct. 2023 14:30:45

        // 4. Parsing Strings
        String dateString = "15-08-2024 10:00:00";
        DateTimeFormatter parser = DateTimeFormatter.ofPattern("dd-MM-yyyy HH:mm:ss");
        LocalDateTime parsedDateTime = LocalDateTime.parse(dateString, parser);
        System.out.println("Parsed LocalDateTime: " + parsedDateTime);

        String timeString = "07:30 PM";
        DateTimeFormatter timeParser = DateTimeFormatter.ofPattern("hh:mm a");
        LocalTime parsedTime = LocalTime.parse(timeString, timeParser);
        System.out.println("Parsed LocalTime: " + parsedTime);
    }
}
```

### 2.9 `TemporalAdjusters` - Complex Date Adjustments

**Purpose:** A utility class that provides a rich set of predefined `TemporalAdjuster` implementations. These are useful for calculating "the next working day", "the last day of the month", "the first day of the year", etc.

**Examples:**

```java
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.temporal.TemporalAdjusters;

public class TemporalAdjustersExample {
    public static void main(String[] args) {
        LocalDate today = LocalDate.of(2023, 10, 26); // Thursday

        // 1. Last day of the month
        LocalDate lastDayOfMonth = today.with(TemporalAdjusters.lastDayOfMonth());
        System.out.println("Last day of " + today.getMonth() + ": " + lastDayOfMonth);

        // 2. First day of the next month
        LocalDate firstDayOfNextMonth = today.with(TemporalAdjusters.firstDayOfNextMonth());
        System.out.println("First day of next month: " + firstDayOfNextMonth);

        // 3. Next Monday
        LocalDate nextMonday = today.with(TemporalAdjusters.next(DayOfWeek.MONDAY));
        System.out.println("Next Monday from " + today + ": " + nextMonday);

        // 4. Previous Sunday
        LocalDate previousSunday = today.with(TemporalAdjusters.previous(DayOfWeek.SUNDAY));
        System.out.println("Previous Sunday from " + today + ": " + previousSunday);

        // 5. First working day of the month (Monday-Friday)
        LocalDate firstWorkingDay = LocalDate.of(2023, 11, 1) // November 1, 2023 is a Wednesday
                                    .with(TemporalAdjusters.firstInMonth(DayOfWeek.MONDAY));
        System.out.println("First Monday of November 2023: " + firstWorkingDay);

        // 6. Custom Adjuster (e.g., next pay day - 15th or last day of month)
        LocalDate myNextPayDay = today.with(temporal -> {
            LocalDate date = (LocalDate) temporal;
            if (date.getDayOfMonth() < 15) {
                return date.withDayOfMonth(15);
            } else {
                return date.with(TemporalAdjusters.lastDayOfMonth());
            }
        });
        System.out.println("Next pay day from " + today + ": " + myNextPayDay);
    }
}
```

---

## 3. Converting Between Legacy and Modern APIs

Sometimes, you need to convert between the old `java.util.Date`/`Calendar` classes and the new `java.time` classes, especially when integrating with older codebases or libraries.

*   `java.util.Date` <-> `java.time.Instant`
*   `java.util.Calendar` <-> `java.time.ZonedDateTime`

**Examples:**

```java
import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Calendar;
import java.util.Date;

public class ConversionExample {
    public static void main(String[] args) {
        // --- Legacy to Modern ---

        // 1. Date to Instant
        Date oldDate = new Date(); // Current date/time
        Instant instantFromDate = oldDate.toInstant();
        System.out.println("Old Date: " + oldDate);
        System.out.println("Instant from Date: " + instantFromDate);

        // 2. Date to LocalDateTime (requires a ZoneId)
        // LocalDateTime does not have timezone info, so you need to specify one
        LocalDateTime localDateTimeFromDate = oldDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDateTime();
        System.out.println("LocalDateTime from Date: " + localDateTimeFromDate);

        // 3. Date to ZonedDateTime
        ZonedDateTime zonedDateTimeFromDate = oldDate.toInstant().atZone(ZoneId.systemDefault());
        System.out.println("ZonedDateTime from Date: " + zonedDateTimeFromDate);

        // 4. Calendar to ZonedDateTime
        Calendar oldCalendar = Calendar.getInstance(); // Current date/time
        ZonedDateTime zonedDateTimeFromCalendar = oldCalendar.toInstant().atZone(ZoneId.systemDefault());
        System.out.println("Old Calendar: " + oldCalendar.getTime());
        System.out.println("ZonedDateTime from Calendar: " + zonedDateTimeFromCalendar);

        // --- Modern to Legacy ---

        // 1. Instant to Date
        Instant modernInstant = Instant.now();
        Date dateFromInstant = Date.from(modernInstant);
        System.out.println("Modern Instant: " + modernInstant);
        System.out.println("Date from Instant: " + dateFromInstant);

        // 2. LocalDateTime to Date (requires a ZoneId to convert to Instant first)
        LocalDateTime modernLocalDateTime = LocalDateTime.now();
        Date dateFromLocalDateTime = Date.from(modernLocalDateTime.atZone(ZoneId.systemDefault()).toInstant());
        System.out.println("Modern LocalDateTime: " + modernLocalDateTime);
        System.out.println("Date from LocalDateTime: " + dateFromLocalDateTime);

        // 3. ZonedDateTime to Date
        ZonedDateTime modernZonedDateTime = ZonedDateTime.now(ZoneId.of("Europe/London"));
        Date dateFromZonedDateTime = Date.from(modernZonedDateTime.toInstant());
        System.out.println("Modern ZonedDateTime: " + modernZonedDateTime);
        System.out.println("Date from ZonedDateTime: " + dateFromZonedDateTime);

        // 4. ZonedDateTime to Calendar
        Calendar calendarFromZonedDateTime = Calendar.getInstance();
        calendarFromZonedDateTime.setTime(Date.from(modernZonedDateTime.toInstant()));
        System.out.println("Calendar from ZonedDateTime: " + calendarFromZonedDateTime.getTime());

        // 5. LocalDate to Date (not direct, needs to be combined with a time and zone)
        LocalDate modernLocalDate = LocalDate.now();
        Date dateFromLocalDate = Date.from(modernLocalDate.atStartOfDay(ZoneId.systemDefault()).toInstant());
        System.out.println("Modern LocalDate: " + modernLocalDate);
        System.out.println("Date from LocalDate (start of day): " + dateFromLocalDate);
    }
}
```

---

## Conclusion

For any new development in Java, it is **highly recommended** to use the **Modern Date/Time API (`java.time` package)** introduced in Java 8. It solves the long-standing problems of the legacy API by providing a clear, immutable, thread-safe, and comprehensive set of classes for handling all date and time requirements. Only use the legacy API when you absolutely must interact with older code or libraries that have not yet been migrated.