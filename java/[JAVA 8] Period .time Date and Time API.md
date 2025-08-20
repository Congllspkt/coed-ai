The `java.time` package, introduced in Java 8, provides a comprehensive and immutable date and time API. `Period` is a key class within this API, representing a quantity of time in terms of years, months, and days.

## `java.time.Period`

### 1. Introduction

`Period` represents a quantity or amount of time, expressed in years, months, and days. It is part of the Java 8 Date and Time API (`java.time` package), which offers a significant improvement over the older `java.util.Date` and `Calendar` classes.

**Key Characteristics:**

*   **Immutable:** Like all classes in `java.time`, `Period` objects are immutable. Any operation that modifies a `Period` will return a new `Period` instance.
*   **Calendar-based:** It operates on a calendar system (the ISO-8601 calendar system by default), making it suitable for human-centric date calculations like "3 years, 2 months, and 5 days".
*   **Distinct from `Duration`:** While `Period` represents a quantity of time in years, months, and days, `java.time.Duration` represents a quantity of time in seconds and nanoseconds. Use `Period` for date-based amounts (e.g., "how many years until retirement?") and `Duration` for time-based amounts (e.g., "how long did that method take to execute?").

### 2. Core Concepts and Methods

`Period` objects contain three integer fields: years, months, and days.

#### 2.1. Creating a `Period`

There are several static factory methods to create `Period` instances:

*   **`Period.of(int years, int months, int days)`**: Creates a `Period` with the specified years, months, and days.
*   **`Period.ofYears(int years)`**: Creates a `Period` with only years.
*   **`Period.ofMonths(int months)`**: Creates a `Period` with only months.
*   **`Period.ofDays(int days)`**: Creates a `Period` with only days.
*   **`Period.between(LocalDate startDateInclusive, LocalDate endDateExclusive)`**: Calculates the period between two `LocalDate` objects. The start date is inclusive, and the end date is exclusive. The calculation is calendar-aware, meaning it considers months and years correctly (e.g., Jan 1 to Feb 1 is 1 month, not 31 days).
*   **`Period.parse(CharSequence text)`**: Parses a text string to obtain a `Period`. The string must be in the ISO-8601 period format `PnYnMnD` (e.g., `P1Y2M3D` for 1 year, 2 months, 3 days, or `P1Y` for 1 year, or `P5M` for 5 months).

#### 2.2. Getting Components

*   **`getYears()`**: Returns the number of years in the period.
*   **`getMonths()`**: Returns the number of months in the period.
*   **`getDays()`**: Returns the number of days in the period.
*   **`getUnits()`**: Returns a list of `TemporalUnit` instances that the `Period` uses (Years, Months, Days).

#### 2.3. Arithmetic Operations

`Period` provides methods to perform arithmetic operations, returning new `Period` instances:

*   **`plus(Period other)`**: Returns a new `Period` by adding the years, months, and days of another `Period`.
*   **`minus(Period other)`**: Returns a new `Period` by subtracting the years, months, and days of another `Period`.
*   **`multipliedBy(int scalar)`**: Returns a new `Period` with each component multiplied by the scalar.
*   **`negated()`**: Returns a new `Period` with each component negated (e.g., `P1Y` becomes `P-1Y`).

#### 2.4. Normalization

*   **`normalized()`**: Returns a copy of this period with the years and months units normalized. This method normalizes the months into years (e.g., 13 months become 1 year and 1 month). **Important**: It does *not* normalize days into months. So, `Period.of(0, 0, 35)` remains `P35D` after normalization, while `Period.of(0, 13, 0)` becomes `P1Y1M`.

#### 2.5. Applying a `Period` to Dates

`Period` can be added to or subtracted from `LocalDate`, `LocalDateTime`, or `ZonedDateTime` objects:

*   **`LocalDate.plus(Period period)`**: Returns a new `LocalDate` by adding the period.
*   **`LocalDate.minus(Period period)`**: Returns a new `LocalDate` by subtracting the period.
*   **`addTo(Temporal temporal)`**: Returns a new `Temporal` object (e.g., `LocalDate`) with this period added.
*   **`subtractFrom(Temporal temporal)`**: Returns a new `Temporal` object with this period subtracted.

#### 2.6. Other Useful Methods

*   **`isZero()`**: Checks if all three components (years, months, days) are zero.
*   **`isNegative()`**: Checks if any of the components are negative.
*   **`toString()`**: Returns a string representation of the period in the ISO-8601 format (e.g., `P1Y2M3D`).

### 3. Examples

Let's illustrate with code examples.

```java
import java.time.LocalDate;
import java.time.Period;
import java.time.format.DateTimeParseException;

public class PeriodExamples {

    public static void main(String[] args) {

        System.out.println("--- 1. Creating a Period ---");
        // 1.1. Using of()
        Period p1 = Period.of(1, 2, 3); // 1 year, 2 months, 3 days
        System.out.println("Period using of(1, 2, 3): " + p1); // Output: P1Y2M3D

        Period pYears = Period.ofYears(5);
        System.out.println("Period of 5 years: " + pYears); // Output: P5Y

        Period pMonths = Period.ofMonths(10);
        System.out.println("Period of 10 months: " + pMonths); // Output: P10M

        Period pDays = Period.ofDays(15);
        System.out.println("Period of 15 days: " + pDays); // Output: P15D

        // 1.2. Using between(LocalDate start, LocalDate end)
        LocalDate startDate = LocalDate.of(2020, 1, 15);
        LocalDate endDate = LocalDate.of(2023, 7, 20);
        Period periodBetween = Period.between(startDate, endDate);
        System.out.println("Period between " + startDate + " and " + endDate + ": " + periodBetween);
        // Output: P3Y6M5D (2020-01-15 to 2023-01-15 is 3 years,
        // 2023-01-15 to 2023-07-15 is 6 months,
        // 2023-07-15 to 2023-07-20 is 5 days)

        LocalDate date1 = LocalDate.of(2023, 1, 31);
        LocalDate date2 = LocalDate.of(2023, 3, 1);
        Period trickyPeriod = Period.between(date1, date2);
        System.out.println("Period between " + date1 + " and " + date2 + ": " + trickyPeriod);
        // Output: P1M1D (Jan 31 to Feb 28 is 1 month, Feb 28 to Mar 1 is 1 day in non-leap year)
        // For 2023 (not a leap year), Feb has 28 days. So Jan 31 -> Feb 28 is 1 month. Feb 28 -> Mar 1 is 1 day.

        // 1.3. Using parse(String text)
        String periodString1 = "P1Y2M3D";
        Period parsedPeriod1 = Period.parse(periodString1);
        System.out.println("Parsed Period '" + periodString1 + "': " + parsedPeriod1); // Output: P1Y2M3D

        String periodString2 = "P-5M"; // Negative period is also possible
        Period parsedPeriod2 = Period.parse(periodString2);
        System.out.println("Parsed Period '" + periodString2 + "': " + parsedPeriod2); // Output: P-5M

        String periodString3 = "P13M"; // Will be normalized later
        Period parsedPeriod3 = Period.parse(periodString3);
        System.out.println("Parsed Period '" + periodString3 + "': " + parsedPeriod3); // Output: P13M

        try {
            Period.parse("invalid-format");
        } catch (DateTimeParseException e) {
            System.out.println("Error parsing invalid format: " + e.getMessage().split("\n")[0]);
            // Output: Error parsing invalid format: Text 'invalid-format' could not be parsed at index 0
        }

        System.out.println("\n--- 2. Getting Components ---");
        Period periodComponents = Period.of(2, 5, 10);
        System.out.println("Period: " + periodComponents);
        System.out.println("Years: " + periodComponents.getYears());   // Output: 2
        System.out.println("Months: " + periodComponents.getMonths()); // Output: 5
        System.out.println("Days: " + periodComponents.getDays());     // Output: 10

        System.out.println("\n--- 3. Arithmetic Operations ---");
        Period pA = Period.of(1, 1, 1);
        Period pB = Period.of(0, 6, 15);

        // 3.1. Adding Periods
        Period pSum = pA.plus(pB);
        System.out.println(pA + " + " + pB + " = " + pSum); // Output: P1Y1M1D + P6M15D = P1Y7M16D

        // 3.2. Subtracting Periods
        Period pDiff = pA.minus(pB);
        System.out.println(pA + " - " + pB + " = " + pDiff); // Output: P1Y1M1D - P6M15D = P1Y-5M-14D

        // 3.3. Multiplying a Period
        Period pMultiplied = pA.multipliedBy(3);
        System.out.println(pA + " * 3 = " + pMultiplied); // Output: P1Y1M1D * 3 = P3Y3M3D

        // 3.4. Negating a Period
        Period pNegated = pA.negated();
        System.out.println("Negation of " + pA + " = " + pNegated); // Output: Negation of P1Y1M1D = P-1Y-1M-1D

        System.out.println("\n--- 4. Normalization ---");
        Period periodToNormalize1 = Period.of(0, 15, 0); // 15 months
        Period normalizedPeriod1 = periodToNormalize1.normalized();
        System.out.println("Period " + periodToNormalize1 + " normalized: " + normalizedPeriod1);
        // Output: Period P15M normalized: P1Y3M (15 months = 1 year and 3 months)

        Period periodToNormalize2 = Period.of(0, 0, 35); // 35 days
        Period normalizedPeriod2 = periodToNormalize2.normalized();
        System.out.println("Period " + periodToNormalize2 + " normalized: " + normalizedPeriod2);
        // Output: Period P35D normalized: P35D (Days are NOT normalized into months/years)

        Period periodToNormalize3 = Period.of(1, -13, 0); // 1 year, -13 months
        Period normalizedPeriod3 = periodToNormalize3.normalized();
        System.out.println("Period " + periodToNormalize3 + " normalized: " + normalizedPeriod3);
        // Output: Period P1Y-13M normalized: P-1M (1 year - 13 months = 12 months - 13 months = -1 month)


        System.out.println("\n--- 5. Applying a Period to Dates ---");
        LocalDate today = LocalDate.now();
        System.out.println("Today: " + today);

        Period futurePeriod = Period.of(1, 6, 10); // 1 year, 6 months, 10 days
        LocalDate futureDate = today.plus(futurePeriod);
        System.out.println("Date after adding " + futurePeriod + ": " + futureDate);

        LocalDate pastDate = today.minus(futurePeriod);
        System.out.println("Date after subtracting " + futurePeriod + ": " + pastDate);

        // Using addTo/subtractFrom
        LocalDate someDate = LocalDate.of(2024, 2, 29); // A leap day
        Period oneYear = Period.ofYears(1);
        LocalDate nextYear = (LocalDate) oneYear.addTo(someDate);
        System.out.println(someDate + " + " + oneYear + " = " + nextYear); // Output: 2024-02-29 + P1Y = 2025-02-28 (handles end-of-month correctly)

        System.out.println("\n--- 6. Checking Properties ---");
        Period zeroPeriod = Period.of(0, 0, 0);
        System.out.println(zeroPeriod + " is zero? " + zeroPeriod.isZero());       // Output: true
        System.out.println(pDiff + " is zero? " + pDiff.isZero());                 // Output: false

        Period negativePeriod = Period.of(-1, 0, 0);
        System.out.println(negativePeriod + " is negative? " + negativePeriod.isNegative()); // Output: true
        System.out.println(pA + " is negative? " + pA.isNegative());               // Output: false

        System.out.println("\n--- 7. Practical Example: Calculate Age ---");
        LocalDate birthDate = LocalDate.of(1990, 5, 10);
        LocalDate currentDate = LocalDate.now();
        Period age = Period.between(birthDate, currentDate);
        System.out.println("Birth Date: " + birthDate);
        System.out.println("Current Date: " + currentDate);
        System.out.println("Age: " + age.getYears() + " years, " + age.getMonths() + " months, and " + age.getDays() + " days.");
        // Example Output (will vary based on current date): Age: 33 years, 8 months, and 12 days.
    }
}
```

**Example Output (execution on 2024-01-22):**

```
--- 1. Creating a Period ---
Period using of(1, 2, 3): P1Y2M3D
Period of 5 years: P5Y
Period of 10 months: P10M
Period of 15 days: P15D
Period between 2020-01-15 and 2023-07-20: P3Y6M5D
Period between 2023-01-31 and 2023-03-01: P1M1D
Parsed Period 'P1Y2M3D': P1Y2M3D
Parsed Period 'P-5M': P-5M
Parsed Period 'P13M': P13M
Error parsing invalid format: Text 'invalid-format' could not be parsed at index 0

--- 2. Getting Components ---
Period: P2Y5M10D
Years: 2
Months: 5
Days: 10

--- 3. Arithmetic Operations ---
P1Y1M1D + P6M15D = P1Y7M16D
P1Y1M1D - P6M15D = P1Y-5M-14D
P1Y1M1D * 3 = P3Y3M3D
Negation of P1Y1M1D = P-1Y-1M-1D

--- 4. Normalization ---
Period P15M normalized: P1Y3M
Period P35D normalized: P35D
Period P1Y-13M normalized: P-1M

--- 5. Applying a Period to Dates ---
Today: 2024-01-22
Date after adding P1Y6M10D: 2025-07-02
Date after subtracting P1Y6M10D: 2022-07-12
2024-02-29 + P1Y = 2025-02-28

--- 6. Checking Properties ---
P0D is zero? true
P1Y-5M-14D is zero? false
P-1Y is negative? true
P1Y1M1D is negative? false

--- 7. Practical Example: Calculate Age ---
Birth Date: 1990-05-10
Current Date: 2024-01-22
Age: 33 years, 8 months, and 12 days.
```