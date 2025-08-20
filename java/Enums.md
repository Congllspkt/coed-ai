Enums, short for "enumerations," in Java are a special kind of class that represents a fixed set of named constants. They were introduced in Java 5 to address limitations of using simple `int` or `String` constants for representing a collection of related values.

## What are Enums?

At their core, enums are a more powerful, type-safe, and readable way to define a collection of constants. Instead of:

```java
public static final int MONDAY = 1;
public static final int TUESDAY = 2;
// ...and so on
```

You can declare an enum:

```java
public enum Day {
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
}
```

### Key Characteristics:

1.  **Type Safety:** Enums prevent you from assigning an invalid value. If a method expects a `Day` enum, you can only pass one of the defined `Day` constants, not an arbitrary integer or string.
2.  **Readability:** Using `Day.MONDAY` is far more descriptive than just `1`.
3.  **Built-in Methods:** All enums implicitly extend `java.lang.Enum` and inherit useful methods like `name()` (returns the constant's name as a string), `ordinal()` (returns the constant's position in the enum declaration, starting from 0), `valueOf()` (converts a string name to an enum constant), and `values()` (returns an array of all enum constants).
4.  **Can Have Fields, Constructors, and Methods:** Enums can be as complex as regular classes, allowing you to associate data and behavior with each constant.
5.  **Implicitly `final` and `static`:** Enum constants are implicitly `public static final`. The enum type itself is also implicitly `final`, meaning it cannot be extended.
6.  **Singleton Nature:** Each enum constant is a singleton; there's only one instance of `Day.MONDAY` throughout your application.

---

## 1. Basic Enum Example

This demonstrates the fundamental declaration and usage, including the built-in methods.

**`Day.java`**
```java
public enum Day {
    MONDAY, 
    TUESDAY, 
    WEDNESDAY, 
    THURSDAY, 
    FRIDAY, 
    SATURDAY, 
    SUNDAY
}
```

**`BasicEnumDemo.java`**
```java
public class BasicEnumDemo {
    public static void main(String[] args) {
        // Accessing enum constants
        Day today = Day.WEDNESDAY;
        Day weekendDay = Day.SATURDAY;

        System.out.println("--- Basic Enum Access ---");
        System.out.println("Today is: " + today); // Calls toString() which returns name()

        // Using built-in methods
        System.out.println("Name of today: " + today.name());
        System.out.println("Ordinal of today (position): " + today.ordinal());

        // Comparing enums
        if (today == Day.WEDNESDAY) {
            System.out.println("Indeed, it's Wednesday!");
        }

        // Iterating through all enum constants
        System.out.println("\n--- All Days of the Week ---");
        for (Day day : Day.values()) {
            System.out.println(day.name() + " (Ordinal: " + day.ordinal() + ")");
        }

        // Converting String to Enum (case-sensitive)
        System.out.println("\n--- Converting String to Enum ---");
        try {
            Day parsedDay = Day.valueOf("FRIDAY");
            System.out.println("Parsed Day from String 'FRIDAY': " + parsedDay);
            
            // This will throw IllegalArgumentException
            // Day invalidDay = Day.valueOf("Funday"); 
        } catch (IllegalArgumentException e) {
            System.err.println("Error: Could not find enum constant for 'Funday'. " + e.getMessage());
        }
    }
}
```

**Input:**
```
(Run `BasicEnumDemo.java`)
```

**Output:**
```
--- Basic Enum Access ---
Today is: WEDNESDAY
Name of today: WEDNESDAY
Ordinal of today (position): 2
Indeed, it's Wednesday!

--- All Days of the Week ---
MONDAY (Ordinal: 0)
TUESDAY (Ordinal: 1)
WEDNESDAY (Ordinal: 2)
THURSDAY (Ordinal: 3)
FRIDAY (Ordinal: 4)
SATURDAY (Ordinal: 5)
SUNDAY (Ordinal: 6)

--- Converting String to Enum ---
Parsed Day from String 'FRIDAY': FRIDAY
Error: Could not find enum constant for 'Funday'. No enum constant Day.Funday
```

---

## 2. Enums with Fields, Constructors, and Methods

This is where enums become truly powerful, allowing each constant to have its own specific data and behavior.

**`TrafficLight.java`**
```java
public enum TrafficLight {
    RED(30, "Stop! No turning on red."),
    YELLOW(5, "Prepare to stop."),
    GREEN(45, "Go, proceed with caution.");

    private final int durationInSeconds;
    private final String message;

    // Constructor for enum constants
    // Enum constructors are implicitly private or package-private.
    // They cannot be public or protected.
    TrafficLight(int durationInSeconds, String message) {
        this.durationInSeconds = durationInSeconds;
        this.message = message;
    }

    // Public getter methods
    public int getDurationInSeconds() {
        return durationInSeconds;
    }

    public String getMessage() {
        return message;
    }

    // A custom method for enum behavior
    public void displayStatus() {
        System.out.println("Traffic Light: " + this.name());
        System.out.println("  Duration: " + durationInSeconds + " seconds");
        System.out.println("  Message: " + message);
    }
}
```

**`EnumWithFieldsDemo.java`**
```java
public class EnumWithFieldsDemo {
    public static void main(String[] args) {
        System.out.println("--- Traffic Light States ---");

        TrafficLight currentLight = TrafficLight.RED;
        currentLight.displayStatus();
        System.out.println("Will change in " + currentLight.getDurationInSeconds() + " seconds.\n");

        TrafficLight nextLight = TrafficLight.YELLOW;
        nextLight.displayStatus();
        System.out.println("Will change in " + nextLight.getDurationInSeconds() + " seconds.\n");

        // Iterate through all traffic light states
        System.out.println("--- All Traffic Light States ---");
        for (TrafficLight light : TrafficLight.values()) {
            System.out.println("State: " + light.name() + 
                               ", Duration: " + light.getDurationInSeconds() + "s" +
                               ", Message: '" + light.getMessage() + "'");
        }
    }
}
```

**Input:**
```
(Run `EnumWithFieldsDemo.java`)
```

**Output:**
```
--- Traffic Light States ---
Traffic Light: RED
  Duration: 30 seconds
  Message: Stop! No turning on red.
Will change in 30 seconds.

Traffic Light: YELLOW
  Duration: 5 seconds
  Message: Prepare to stop.
Will change in 5 seconds.

--- All Traffic Light States ---
State: RED, Duration: 30s, Message: 'Stop! No turning on red.'
State: YELLOW, Duration: 5s, Message: 'Prepare to stop.'
State: GREEN, Duration: 45s, Message: 'Go, proceed with caution.'
```

### Enum with Constant-Specific Method Implementations (Polymorphism)

Enums can also have abstract methods that each constant implements differently, providing a powerful way to implement the Strategy pattern.

**`Operation.java`**
```java
public enum Operation {
    ADD {
        @Override
        public double apply(double x, double y) {
            return x + y;
        }
    },
    SUBTRACT {
        @Override
        public double apply(double x, double y) {
            return x - y;
        }
    },
    MULTIPLY {
        @Override
        public double apply(double x, double y) {
            return x * y;
        }
    },
    DIVIDE {
        @Override
        public double apply(double x, double y) {
            if (y == 0) {
                throw new IllegalArgumentException("Cannot divide by zero.");
            }
            return x / y;
        }
    };

    // This is an abstract method that each enum constant must implement.
    public abstract double apply(double x, double y);
}
```

**`EnumPolymorphismDemo.java`**
```java
public class EnumPolymorphismDemo {
    public static void main(String[] args) {
        double num1 = 10.0;
        double num2 = 5.0;

        System.out.println("--- Performing Operations ---");

        // Use the apply method specific to each enum constant
        System.out.println(num1 + " + " + num2 + " = " + Operation.ADD.apply(num1, num2));
        System.out.println(num1 + " - " + num2 + " = " + Operation.SUBTRACT.apply(num1, num2));
        System.out.println(num1 + " * " + num2 + " = " + Operation.MULTIPLY.apply(num1, num2));
        System.out.println(num1 + " / " + num2 + " = " + Operation.DIVIDE.apply(num1, num2));

        // Attempt division by zero
        try {
            Operation.DIVIDE.apply(num1, 0.0);
        } catch (IllegalArgumentException e) {
            System.out.println("\nError during division: " + e.getMessage());
        }
    }
}
```

**Input:**
```
(Run `EnumPolymorphismDemo.java`)
```

**Output:**
```
--- Performing Operations ---
10.0 + 5.0 = 15.0
10.0 - 5.0 = 5.0
10.0 * 5.0 = 50.0
10.0 / 5.0 = 2.0

Error during division: Cannot divide by zero.
```

---

## 3. Enums in `switch` Statements

Enums are perfectly suited for use in `switch` statements, providing clear and concise control flow.

**`Day.java` (from Basic Example)**
```java
public enum Day {
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
}
```

**`EnumSwitchDemo.java`**
```java
public class EnumSwitchDemo {

    public static void describeDay(Day day) {
        System.out.print("Today (" + day.name() + ") is a ");
        switch (day) {
            case MONDAY:
                System.out.println("fresh start to the week.");
                break;
            case TUESDAY:
            case WEDNESDAY:
            case THURSDAY:
                System.out.println("mid-week grind.");
                break;
            case FRIDAY:
                System.out.println("great day for winding down.");
                break;
            case SATURDAY:
            case SUNDAY:
                System.out.println("relaxing weekend day!");
                break;
            // No need for 'default' if all enum constants are covered,
            // but can be useful for future-proofing or error handling.
        }
    }

    public static void main(String[] args) {
        System.out.println("--- Describing Days ---");
        describeDay(Day.MONDAY);
        describeDay(Day.WEDNESDAY);
        describeDay(Day.FRIDAY);
        describeDay(Day.SUNDAY);
    }
}
```

**Input:**
```
(Run `EnumSwitchDemo.java`)
```

**Output:**
```
--- Describing Days ---
Today (MONDAY) is a fresh start to the week.
Today (WEDNESDAY) is a mid-week grind.
Today (FRIDAY) is a great day for winding down.
Today (SUNDAY) is a relaxing weekend day!
```

---

## 4. Enums Implementing Interfaces

Enums can implement interfaces, allowing them to participate in polymorphism with other classes or enums that implement the same interface.

**`Loggable.java`**
```java
public interface Loggable {
    String getLogMessage(String event);
    int getSeverityLevel();
}
```

**`LogSeverity.java`**
```java
public enum LogSeverity implements Loggable {
    INFO(1, "Informational message"),
    WARNING(2, "Potential issue detected"),
    ERROR(3, "Critical error occurred"),
    DEBUG(0, "Debugging information");

    private final int level;
    private final String description;

    LogSeverity(int level, String description) {
        this.level = level;
        this.description = description;
    }

    @Override
    public String getLogMessage(String event) {
        return "[" + this.name() + " - Level " + level + "] " + description + ": " + event;
    }

    @Override
    public int getSeverityLevel() {
        return level;
    }
}
```

**`EnumInterfaceDemo.java`**
```java
public class EnumInterfaceDemo {
    public static void processLoggable(Loggable loggable, String event) {
        System.out.println(loggable.getLogMessage(event));
        System.out.println("  (Severity Level: " + loggable.getSeverityLevel() + ")");
    }

    public static void main(String[] args) {
        System.out.println("--- Logging Events ---");

        processLoggable(LogSeverity.INFO, "User 'JohnDoe' logged in.");
        processLoggable(LogSeverity.WARNING, "Disk space running low on server 'web-01'.");
        processLoggable(LogSeverity.ERROR, "Database connection failed.");
        processLoggable(LogSeverity.DEBUG, "Variable 'x' value is: 42.");
    }
}
```

**Input:**
```
(Run `EnumInterfaceDemo.java`)
```

**Output:**
```
--- Logging Events ---
[INFO - Level 1] Informational message: User 'JohnDoe' logged in.
  (Severity Level: 1)
[WARNING - Level 2] Potential issue detected: Disk space running low on server 'web-01'.
  (Severity Level: 2)
[ERROR - Level 3] Critical error occurred: Database connection failed.
  (Severity Level: 3)
[DEBUG - Level 0] Debugging information: Variable 'x' value is: 42.
```

---

## When to Use Enums

*   **Fixed set of constants:** When you have a collection of items that will not change (e.g., days of the week, months, directions, cardinal points, genders, error codes, HTTP status codes).
*   **Type Safety:** To ensure that only valid, predefined values are used, preventing runtime errors caused by typos or incorrect integer/string values.
*   **Associating Data/Behavior:** When each constant needs to carry specific data (like a duration for a traffic light) or perform a specific action (like different arithmetic operations).
*   **Replacing `int` or `String` constants:** Enums provide a much more robust, readable, and maintainable alternative.
*   **Strategy Pattern:** Enums with constant-specific method implementations are an elegant way to implement variations of an algorithm.

## Conclusion

Enums in Java are a powerful and versatile feature that goes far beyond simple integer constants. By providing type safety, readability, and the ability to encapsulate data and behavior, they significantly improve the design, maintainability, and robustness of Java applications, especially when dealing with fixed sets of related values.