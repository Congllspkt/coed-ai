This document provides a detailed explanation of Java access modifiers: `private`, `public`, `protected`, and `default` (package-private), along with illustrative examples.

---

# Java Access Modifiers

In Java, access modifiers are keywords that set the accessibility (or visibility) of classes, constructors, methods, and data members (fields). They are a crucial part of **encapsulation**, allowing you to control which parts of your code can access other parts.

There are four types of access modifiers in Java:

1.  `private`
2.  `default` (no keyword, also known as package-private)
3.  `protected`
4.  `public`

---

## Summary Table

| Modifier   | Scope                                                              | Description                                                                 | Applicable To                                |
| :--------- | :----------------------------------------------------------------- | :-------------------------------------------------------------------------- | :------------------------------------------- |
| `private`  | Within the **same class** only.                                    | Most restrictive. Members are only accessible from inside the class.        | Fields, Methods, Constructors, Inner Classes |
| `default`  | Within the **same package** only.                                  | No keyword. Members are accessible only within their own package.           | Classes, Fields, Methods, Constructors       |
| `protected`| Within the **same package** OR by **subclasses** (even in different packages). | Provides inheritance-based access.                                          | Fields, Methods, Constructors, Inner Classes |
| `public`   | From **anywhere**.                                                 | Least restrictive. Members are accessible from all classes, all packages.   | Classes, Fields, Methods, Constructors       |

---

## 1. `private`

*   **Definition**: The `private` access modifier is the most restrictive. When a member (field, method, or constructor) is declared `private`, it is only accessible from within the class in which it is declared.
*   **Scope**: Only within the same class.
*   **Usage**: Primarily used for implementing strong encapsulation. Private members represent the internal implementation details of a class that should not be exposed directly to the outside world. Often used with "getters" and "setters" (public methods) to control access to private fields.
*   **Applicability**: Fields, methods, constructors, inner classes. **Cannot be applied to top-level classes**.

### Example: `private`

```java
// File: com/example/model/BankAccount.java
package com.example.model;

public class BankAccount {
    private String accountNumber; // private field
    private double balance;       // private field

    public BankAccount(String accountNumber, double initialBalance) {
        this.accountNumber = accountNumber;
        this.balance = initialBalance;
    }

    // Public method to deposit money (safe way to modify private balance)
    public void deposit(double amount) {
        if (amount > 0) {
            this.balance += amount;
            System.out.println("Deposited: $" + amount + ". New balance: $" + this.balance);
        } else {
            System.out.println("Deposit amount must be positive.");
        }
    }

    // Public method to withdraw money (safe way to modify private balance)
    public void withdraw(double amount) {
        if (amount > 0 && this.balance >= amount) {
            this.balance -= amount;
            System.out.println("Withdrew: $" + amount + ". New balance: $" + this.balance);
        } else {
            System.out.println("Insufficient funds or invalid withdrawal amount.");
        }
    }

    // Public getter method to read private balance
    public double getBalance() {
        return this.balance;
    }

    // A private helper method, only usable within BankAccount
    private void logTransaction(String type, double amount) {
        System.out.println("Transaction logged: " + type + " of $" + amount + " on account " + accountNumber);
    }
}
```

```java
// File: com/example/app/BankApp.java
package com.example.app;

import com.example.model.BankAccount;

public class BankApp {
    public static void main(String[] args) {
        BankAccount myAccount = new BankAccount("123456789", 1000.00);

        // Accessing public methods is allowed
        myAccount.deposit(200.00);
        myAccount.withdraw(150.00);
        System.out.println("Current balance: $" + myAccount.getBalance());

        // --- The following lines would cause a compile-time error ---
        // myAccount.balance = 5000.00; // Error: balance has private access in BankAccount
        // myAccount.accountNumber = "987654321"; // Error: accountNumber has private access in BankAccount
        // myAccount.logTransaction("Info", 0); // Error: logTransaction has private access in BankAccount
    }
}
```

---

## 2. `default` (Package-Private)

*   **Definition**: When no access modifier is specified for a class, field, method, or constructor, it is considered to have `default` or **package-private** access.
*   **Scope**: Accessible only within the same package. It means classes in the same package can access these members, but classes in other packages cannot.
*   **Usage**: Useful for components that are internal to a package and should not be exposed outside of it. It promotes modularity within a larger system.
*   **Applicability**: Classes, fields, methods, constructors.

### Example: `default`

**Package: `com.example.util`**

```java
// File: com/example/util/InternalLogger.java
package com.example.util;

// This class has default access, meaning it's only accessible within com.example.util
class InternalLogger { 
    // This method has default access
    void logMessage(String message) { 
        System.out.println("INTERNAL LOG: " + message);
    }

    // This field has default access
    String defaultLogTag = "DefaultTag"; 
}
```

```java
// File: com/example/util/ServiceHelper.java
package com.example.util;

public class ServiceHelper {
    public void performServiceOperation() {
        InternalLogger logger = new InternalLogger(); // Accessible: InternalLogger is in the same package
        logger.logMessage("Performing service operation..."); // Accessible: logMessage is in the same package
        System.out.println("Using log tag: " + logger.defaultLogTag); // Accessible: defaultLogTag is in the same package
    }
}
```

**Package: `com.example.app`**

```java
// File: com/example/app/MainApp.java
package com.example.app;

// import com.example.util.InternalLogger; // ERROR: InternalLogger is not public in com.example.util; cannot be accessed from outside package
import com.example.util.ServiceHelper;

public class MainApp {
    public static void main(String[] args) {
        ServiceHelper helper = new ServiceHelper(); // Accessible: ServiceHelper is public
        helper.performServiceOperation(); // Accessible: performServiceOperation is public

        // --- The following lines would cause compile-time errors ---
        // InternalLogger logger = new InternalLogger(); // Error: InternalLogger has default access in com.example.util
                                                      // You cannot even import it if it's not public.

        // If you somehow instantiated it (e.g., via reflection, but that bypasses checks):
        // logger.logMessage("This won't work!"); // Error: logMessage has default access in InternalLogger
    }
}
```

---

## 3. `protected`

*   **Definition**: The `protected` access modifier allows members to be accessed within the same package and also by subclasses in *any* package.
*   **Scope**:
    1.  Within the same package (like `default`).
    2.  By subclasses, even if the subclass is in a different package.
*   **Usage**: Primarily used for inheritance. It enables base classes to provide functionality that can be used or extended by their derived classes, while still limiting access to non-related classes outside the package.
*   **Applicability**: Fields, methods, constructors, inner classes. **Cannot be applied to top-level classes**.

### Example: `protected`

**Package: `com.example.vehicles`**

```java
// File: com/example/vehicles/Vehicle.java
package com.example.vehicles;

public class Vehicle {
    protected String brand; // Protected field
    protected int year;     // Protected field

    public Vehicle(String brand, int year) {
        this.brand = brand;
        this.year = year;
    }

    protected void startEngine() { // Protected method
        System.out.println(brand + " engine started. (Year: " + year + ")");
    }

    // A public method that might use protected members internally
    public void displayInfo() {
        System.out.println("Vehicle: " + brand + ", Year: " + year);
    }
}
```

**Package: `com.example.vehicles` (Same package)**

```java
// File: com/example/vehicles/Car.java
package com.example.vehicles;

// Car is in the same package as Vehicle
public class Car extends Vehicle {
    public Car(String brand, int year) {
        super(brand, year);
    }

    public void drive() {
        startEngine(); // Accessible: protected method is accessible within the same package
        System.out.println(brand + " is driving. (Year: " + year + ")"); // Accessible: protected fields are accessible within the same package
    }
}
```

**Package: `com.example.app` (Different package)**

```java
// File: com/example/app/Truck.java
package com.example.app;

import com.example.vehicles.Vehicle;

// Truck is a subclass of Vehicle but in a different package
public class Truck extends Vehicle {
    private double payloadCapacity;

    public Truck(String brand, int year, double payloadCapacity) {
        super(brand, year);
        this.payloadCapacity = payloadCapacity;
    }

    public void haul() {
        startEngine(); // Accessible: protected method is accessible by a subclass (even in different package)
        System.out.println(brand + " is hauling with a capacity of " + payloadCapacity + " tons. (Year: " + year + ")"); // Accessible: protected fields are accessible by a subclass
    }
}
```

```java
// File: com/example/app/MainApplication.java
package com.example.app;

import com.example.vehicles.Vehicle;
import com.example.vehicles.Car;

public class MainApplication {
    public static void main(String[] args) {
        Car myCar = new Car("Honda", 2020);
        myCar.drive(); // Calls public method, which uses protected internally
        myCar.displayInfo(); // Calls public method

        Truck myTruck = new Truck("Ford", 2018, 5.0);
        myTruck.haul(); // Calls public method, which uses protected internally
        myTruck.displayInfo(); // Calls public method

        Vehicle genericVehicle = new Vehicle("Motorcycle", 2022);
        // genericVehicle.startEngine(); // Error: startEngine() has protected access in Vehicle
                                      // Not accessible here because MainApplication is NOT a subclass of Vehicle
                                      // and is in a different package from Vehicle.

        // System.out.println(genericVehicle.brand); // Error: brand has protected access in Vehicle
                                                // Same reason as above.
    }
}
```

---

## 4. `public`

*   **Definition**: The `public` access modifier is the least restrictive. When a class, field, method, or constructor is declared `public`, it is accessible from anywhere.
*   **Scope**: Accessible from any class, in any package.
*   **Usage**: Used for components that are part of the public API of your library or application. These are the elements that other classes or applications are expected to interact with.
*   **Applicability**: Classes, fields, methods, constructors.

### Example: `public`

```java
// File: com/example/math/Calculator.java
package com.example.math;

public class Calculator { // Public class: accessible from anywhere

    public static final double PI = 3.14159; // Public field: accessible from anywhere

    public Calculator() { // Public constructor: can be instantiated from anywhere
        System.out.println("Calculator instance created.");
    }

    public int add(int a, int b) { // Public method: callable from anywhere
        return a + b;
    }

    public int subtract(int a, int b) { // Public method: callable from anywhere
        return a - b;
    }
}
```

```java
// File: com/example/main/Application.java
package com.example.main;

import com.example.math.Calculator; // Import public class

public class Application {
    public static void main(String[] args) {
        Calculator myCalc = new Calculator(); // Accessible: public constructor

        int sum = myCalc.add(10, 5); // Accessible: public method
        System.out.println("10 + 5 = " + sum);

        int difference = myCalc.subtract(10, 5); // Accessible: public method
        System.out.println("10 - 5 = " + difference);

        System.out.println("Value of PI: " + Calculator.PI); // Accessible: public static final field
    }
}
```

---

## Best Practices and Considerations

*   **Encapsulation (Information Hiding)**: Aim to make your fields `private` and provide `public` getter/setter methods to control how they are accessed and modified. This protects the internal state of your objects.
*   **Least Privilege**: Always choose the most restrictive access modifier that still allows your code to function. Start with `private`, then consider `default`, then `protected`, and only use `public` if absolutely necessary for the API.
*   **API Design**: `public` members define the public contract of your classes and libraries. Change `public` members carefully, as they can break code that uses your library. `private` and `default` members are internal implementation details that can be changed more freely.
*   **Inheritance vs. Composition**: `protected` is closely tied to inheritance. Consider if inheritance is truly the best approach, or if composition (`has-a` relationship) might be better, which often avoids the need for `protected` members.
*   **Top-Level Classes**: Only `public` and `default` modifiers are applicable to top-level classes. Inner classes can use `private`, `protected`, `public`, or `default`.

By understanding and correctly applying access modifiers, you can build more robust, maintainable, and secure Java applications.