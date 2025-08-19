
A **class** in Java is the fundamental building block of Object-Oriented Programming (OOP). It serves as a **blueprint** or a **template** for creating objects.

Think of it like this: If you want to build many houses, you first need a blueprint. This blueprint specifies how many rooms, what kind of roof, where the windows go, etc. You don't live *in* the blueprint; you build actual houses *from* the blueprint.

In Java:
*   The **class** is the blueprint (`House.java`).
*   An **object** is an actual house built from that blueprint. You can create many houses (objects) from the same blueprint (class).

## What is a Java Class? - Detailed Explanation

A class encapsulates (bundles together) **data** (fields) and the **methods** (functions) that operate on that data. This concept is known as **encapsulation**, one of the core principles of OOP.

### Core Components of a Class:

1.  **Fields (or Instance Variables):**
    *   These are variables defined within a class but outside any method.
    *   They represent the **state** or **attributes** of an object created from that class.
    *   Example: For a `Car` class, fields might be `color`, `make`, `model`, `speed`.

2.  **Methods:**
    *   These are functions defined within a class.
    *   They represent the **behavior** or **actions** that objects of the class can perform.
    *   Example: For a `Car` class, methods might be `startEngine()`, `accelerate()`, `brake()`, `displayInfo()`.

3.  **Constructors:**
    *   Special methods used to **initialize** new objects of a class.
    *   They have the **same name as the class** and no return type (not even `void`).
    *   Called automatically when an object is created using the `new` keyword.
    *   You can have multiple constructors (constructor overloading) with different parameters.

4.  **`main` Method (Special Case):**
    *   A class can (but doesn't have to) contain a `main` method: `public static void main(String[] args)`.
    *   This is the **entry point** for any Java application. When you run a Java program, the Java Virtual Machine (JVM) looks for and executes the `main` method of the specified class.
    *   It's where you typically create objects of other classes and invoke their methods.

### Key Concepts Related to Classes:

*   **Objects (Instantiation):** An object is an instance of a class. You create an object using the `new` keyword followed by the class's constructor.
    ```java
    ClassName objectName = new ClassName();
    ```
*   **Encapsulation:** Achieved by making the fields `private` (not directly accessible from outside the class) and providing `public` methods (getters and setters) to access and modify them. This protects the internal state of the object.
*   **Access Modifiers:** Keywords that control the visibility of classes, fields, methods, and constructors.
    *   `public`: Accessible from anywhere.
    *   `private`: Accessible only within the class itself.
    *   `protected`: Accessible within the class, by subclasses, and from classes in the same package.
    *   (default/package-private): Accessible only within the same package.
*   **`this` Keyword:** Refers to the current object. It's often used inside a class to distinguish between instance variables and parameters with the same name, or to call other constructors of the same class.

## Example: `Book` Class

Let's create a `Book` class to demonstrate these concepts.

### 1. Define the `Book` Class (`Book.java`)

```java
// Book.java
public class Book {
    // 1. Fields (Instance Variables) - represent the state of a Book object
    private String title;
    private String author;
    private String isbn;
    private boolean isAvailable; // To track if the book is currently available for borrowing

    // 2. Constructor - used to initialize a new Book object
    // This is a parameterized constructor
    public Book(String title, String author, String isbn) {
        // 'this' keyword refers to the current object's instance variables
        this.title = title;
        this.author = author;
        this.isbn = isbn;
        this.isAvailable = true; // A new book is typically available by default
        System.out.println("Book '" + title + "' by " + author + " created.");
    }

    // 3. Methods - represent the behavior of a Book object

    // Getter methods to access private fields (Encapsulation)
    public String getTitle() {
        return title;
    }

    public String getAuthor() {
        return author;
    }

    public String getIsbn() {
        return isbn;
    }

    public boolean isAvailable() { // Standard naming convention for boolean getters
        return isAvailable;
    }

    // Setter method to modify a private field (Encapsulation)
    public void setAvailable(boolean available) {
        this.isAvailable = available;
    }

    // Custom method to display book information
    public void displayBookInfo() {
        System.out.println("--- Book Details ---");
        System.out.println("Title: " + title);
        System.out.println("Author: " + author);
        System.out.println("ISBN: " + isbn);
        System.out.println("Availability: " + (isAvailable ? "Available" : "Borrowed"));
        System.out.println("--------------------");
    }

    // Custom method for borrowing a book
    public void borrowBook() {
        if (isAvailable) {
            this.isAvailable = false;
            System.out.println("'" + title + "' has been successfully borrowed.");
        } else {
            System.out.println("Sorry, '" + title + "' is currently not available.");
        }
    }

    // Custom method for returning a book
    public void returnBook() {
        if (!isAvailable) {
            this.isAvailable = true;
            System.out.println("'" + title + "' has been successfully returned.");
        } else {
            System.out.println("'" + title + "' was already available.");
        }
    }
}
```

### 2. Create a `LibraryApp` Class (`LibraryApp.java`) with `main` Method

This class will contain the `main` method, which is the entry point for our program. We will create `Book` objects here and interact with them.

```java
// LibraryApp.java
public class LibraryApp {
    // The main method - entry point of the application
    public static void main(String[] args) {
        System.out.println("--- Welcome to the Library App ---");

        // 1. Creating objects (instantiating the Book class)
        // Uses the constructor defined in the Book class
        Book book1 = new Book("The Lord of the Rings", "J.R.R. Tolkien", "978-0618053267");
        Book book2 = new Book("Pride and Prejudice", "Jane Austen", "978-0141439518");
        Book book3 = new Book("1984", "George Orwell", "978-0451524935");

        System.out.println("\n--- Displaying Initial Book Info ---");
        book1.displayBookInfo();
        book2.displayBookInfo();
        book3.displayBookInfo();

        System.out.println("\n--- Simulating Book Operations ---");

        // 2. Interacting with objects (calling methods)
        book1.borrowBook(); // Book1 is borrowed
        book2.borrowBook(); // Book2 is borrowed
        book2.borrowBook(); // Try to borrow again (should fail)

        System.out.println("\n--- Displaying Book Info After Borrowing ---");
        book1.displayBookInfo();
        book2.displayBookInfo();
        book3.displayBookInfo(); // Book3 should still be available

        book1.returnBook(); // Book1 is returned
        book3.returnBook(); // Try to return a book that wasn't borrowed (should indicate it was available)

        System.out.println("\n--- Displaying Book Info After Returning ---");
        book1.displayBookInfo();
        book2.displayBookInfo();
        book3.displayBookInfo();

        // Using getters to check status directly
        System.out.println("\n--- Checking specific book status ---");
        System.out.println("Is '" + book2.getTitle() + "' available? " + book2.isAvailable());

        System.out.println("\n--- Library App Ended ---");
    }
}
```

### How to Compile and Run:

1.  **Save:** Save the first file as `Book.java` and the second as `LibraryApp.java` in the same directory.
2.  **Open Terminal/Command Prompt:** Navigate to the directory where you saved the files.
3.  **Compile:** Use the Java compiler (`javac`) to compile both `.java` files into `.class` files (bytecode).
    ```bash
    javac Book.java LibraryApp.java
    ```
    This will create `Book.class` and `LibraryApp.class` in the same directory.
4.  **Run:** Execute the `LibraryApp` class, as it contains the `main` method.
    ```bash
    java LibraryApp
    ```

### Expected Input and Output:

**Input:**
The "input" in this context is the Java source code itself (`Book.java` and `LibraryApp.java`). The `LibraryApp` class defines the sequence of operations (creating books, borrowing, returning, displaying).

**Output:**
```
--- Welcome to the Library App ---
Book 'The Lord of the Rings' by J.R.R. Tolkien created.
Book 'Pride and Prejudice' by Jane Austen created.
Book '1984' by George Orwell created.

--- Displaying Initial Book Info ---
--- Book Details ---
Title: The Lord of the Rings
Author: J.R.R. Tolkien
ISBN: 978-0618053267
Availability: Available
--------------------
--- Book Details ---
Title: Pride and Prejudice
Author: Jane Austen
ISBN: 978-0141439518
Availability: Available
--------------------
--- Book Details ---
Title: 1984
Author: George Orwell
ISBN: 978-0451524935
Availability: Available
--------------------

--- Simulating Book Operations ---
'The Lord of the Rings' has been successfully borrowed.
'Pride and Prejudice' has been successfully borrowed.
Sorry, 'Pride and Prejudice' is currently not available.

--- Displaying Book Info After Borrowing ---
--- Book Details ---
Title: The Lord of the Rings
Author: J.R.R. Tolkien
ISBN: 978-0618053267
Availability: Borrowed
--------------------
--- Book Details ---
Title: Pride and Prejudice
Author: Jane Austen
ISBN: 978-0141439518
Availability: Borrowed
--------------------
--- Book Details ---
Title: 1984
Author: George Orwell
ISBN: 978-0451524935
Availability: Available
--------------------

--- Returning Books ---
'The Lord of the Rings' has been successfully returned.
'1984' was already available.

--- Displaying Book Info After Returning ---
--- Book Details ---
Title: The Lord of the Rings
Author: J.R.R. Tolkien
ISBN: 978-0618053267
Availability: Available
--------------------
--- Book Details ---
Title: Pride and Prejudice
Author: Jane Austen
ISBN: 978-0141439518
Availability: Borrowed
--------------------
--- Book Details ---
Title: 1984
Author: George Orwell
ISBN: 978-0451524935
Availability: Available
--------------------

--- Checking specific book status ---
Is 'Pride and Prejudice' available? false

--- Library App Ended ---
```

This example clearly shows how a `Book` class acts as a blueprint, how objects (`book1`, `book2`, `book3`) are created from it, and how their state (fields) and behavior (methods) are managed.