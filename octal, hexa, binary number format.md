
# Understanding Number Formats in Java: Binary, Octal, and Hexadecimal

In computer science, numbers are not always represented in the familiar base-10 (decimal) system. Binary (base 2), Octal (base 8), and Hexadecimal (base 16) are crucial for various low-level operations, memory representation, and data encoding.

Java provides built-in support for representing these number literals directly in your code and for converting between these formats and their decimal equivalents.

## Key Concepts

1.  **Literal Representation**: How you write the number directly in your Java source code.
2.  **Internal Representation**: All numbers (integers, longs, etc.) are *always* stored internally in binary format within the computer's memory. The base-specific prefixes (`0b`, `0o`, `0x`, or just `0`) only tell the Java compiler how to interpret the literal value you've written, not how it's stored.
3.  **Conversion**: Methods provided by `Integer`, `Long`, etc., to parse strings of different bases into integer types and to format integer types into string representations of different bases.

---

## 1. Binary Numbers (Base 2)

Binary numbers use only two digits: `0` and `1`. They are the fundamental language of computers.

### Literal Representation in Java

To represent a binary literal in Java, prefix the number with `0b` or `0B`.

```java
int binaryNumber = 0b1011; // This is equivalent to decimal 11
// (1 * 2^3) + (0 * 2^2) + (1 * 2^1) + (1 * 2^0) = 8 + 0 + 2 + 1 = 11
```

### Conversion Methods

*   **From Decimal `int` to Binary `String`**: `Integer.toBinaryString(int i)`
*   **From Binary `String` to Decimal `int`**: `Integer.parseInt(String s, int radix)` with `radix = 2`

### Example: Binary Numbers

```java
// BinaryExample.java
public class BinaryExample {
    public static void main(String[] args) {
        System.out.println("--- Binary Number Examples ---");

        // 1. Binary Literal Representation
        int binaryLiteral = 0b101101; // Equivalent to decimal 45
        System.out.println("\n1. Binary Literal:");
        System.out.println("  Literal (0b101101) in decimal: " + binaryLiteral); // Output: 45

        // 2. Converting Decimal to Binary String
        int decimalValue = 75;
        String binaryString = Integer.toBinaryString(decimalValue);
        System.out.println("\n2. Decimal to Binary String:");
        System.out.println("  Decimal " + decimalValue + " in binary: " + binaryString); // Output: 1001011

        // 3. Converting Binary String to Decimal Integer
        String binaryInput = "11010"; // This is decimal 26
        try {
            int parsedDecimal = Integer.parseInt(binaryInput, 2);
            System.out.println("\n3. Binary String to Decimal Integer:");
            System.out.println("  Binary string \"" + binaryInput + "\" parsed to decimal: " + parsedDecimal); // Output: 26
        } catch (NumberFormatException e) {
            System.out.println("  Error parsing binary string: " + e.getMessage());
        }

        // 4. Using Long for larger numbers
        long longBinaryLiteral = 0b10000000000000000000000000000000L; // 2^31
        System.out.println("\n4. Long Binary Literal:");
        System.out.println("  Long binary literal (0b1...) in decimal: " + longBinaryLiteral);

        // 5. Invalid Binary String
        String invalidBinary = "101201";
        try {
            Integer.parseInt(invalidBinary, 2);
        } catch (NumberFormatException e) {
            System.out.println("\n5. Invalid Binary String (Expected Error):");
            System.out.println("  Error parsing \"" + invalidBinary + "\": " + e.getMessage()); // Contains non-binary digit '2'
        }
    }
}
```

#### Input (Implicit from code):

```java
// No direct user input for this example. Values are hardcoded.
```

#### Output:

```plaintext
--- Binary Number Examples ---

1. Binary Literal:
  Literal (0b101101) in decimal: 45

2. Decimal to Binary String:
  Decimal 75 in binary: 1001011

3. Binary String to Decimal Integer:
  Binary string "11010" parsed to decimal: 26

4. Long Binary Literal:
  Long binary literal (0b1...) in decimal: 2147483648

5. Invalid Binary String (Expected Error):
  Error parsing "101201": For input string: "101201"
```

---

## 2. Octal Numbers (Base 8)

Octal numbers use digits from `0` to `7`. They were more common in early computing and are sometimes still used for file permissions (e.g., in Unix/Linux systems).

### Literal Representation in Java

To represent an octal literal in Java, prefix the number with a single `0` (zero).

```java
int octalNumber = 017; // This is equivalent to decimal 15
// (1 * 8^1) + (7 * 8^0) = 8 + 7 = 15
```

**Important Note**: A leading `0` always signifies an octal literal in Java for integer types. Be careful not to accidentally add a leading `0` to a decimal number if you intend it to be interpreted as decimal, as it will be treated as octal.

### Conversion Methods

*   **From Decimal `int` to Octal `String`**: `Integer.toOctalString(int i)`
*   **From Octal `String` to Decimal `int`**: `Integer.parseInt(String s, int radix)` with `radix = 8`

### Example: Octal Numbers

```java
// OctalExample.java
public class OctalExample {
    public static void main(String[] args) {
        System.out.println("--- Octal Number Examples ---");

        // 1. Octal Literal Representation
        int octalLiteral = 037; // Equivalent to decimal 31
        System.out.println("\n1. Octal Literal:");
        System.out.println("  Literal (037) in decimal: " + octalLiteral); // Output: 31

        // 2. Common Pitfall: Leading zero
        int decimalIntended = 010; // This is NOT decimal 10, it's octal 10 (decimal 8)
        System.out.println("  Common Pitfall: 010 interpreted as octal: " + decimalIntended); // Output: 8

        // 3. Converting Decimal to Octal String
        int decimalValue = 64;
        String octalString = Integer.toOctalString(decimalValue);
        System.out.println("\n3. Decimal to Octal String:");
        System.out.println("  Decimal " + decimalValue + " in octal: " + octalString); // Output: 100

        // 4. Converting Octal String to Decimal Integer
        String octalInput = "71"; // This is decimal 57
        try {
            int parsedDecimal = Integer.parseInt(octalInput, 8);
            System.out.println("\n4. Octal String to Decimal Integer:");
            System.out.println("  Octal string \"" + octalInput + "\" parsed to decimal: " + parsedDecimal); // Output: 57
        } catch (NumberFormatException e) {
            System.out.println("  Error parsing octal string: " + e.getMessage());
        }

        // 5. Invalid Octal String
        String invalidOctal = "187"; // Contains digit '8' which is invalid for octal
        try {
            Integer.parseInt(invalidOctal, 8);
        } catch (NumberFormatException e) {
            System.out.println("\n5. Invalid Octal String (Expected Error):");
            System.out.println("  Error parsing \"" + invalidOctal + "\": " + e.getMessage());
        }
    }
}
```

#### Input (Implicit from code):

```java
// No direct user input for this example. Values are hardcoded.
```

#### Output:

```plaintext
--- Octal Number Examples ---

1. Octal Literal:
  Literal (037) in decimal: 31
  Common Pitfall: 010 interpreted as octal: 8

3. Decimal to Octal String:
  Decimal 64 in octal: 100

4. Octal String to Decimal Integer:
  Octal string "71" parsed to decimal: 57

5. Invalid Octal String (Expected Error):
  Error parsing "187": For input string: "187"
```

---

## 3. Hexadecimal Numbers (Base 16)

Hexadecimal numbers use digits `0-9` and letters `A-F` (or `a-f`) to represent values from `0` to `15`. Each hexadecimal digit corresponds to exactly four binary digits (a nibble), making it a compact and human-readable way to represent binary data. It's widely used in web colors (e.g., `#FF0000`), memory addresses, MAC addresses, and UUIDs.

### Literal Representation in Java

To represent a hexadecimal literal in Java, prefix the number with `0x` or `0X`.

```java
int hexNumber = 0xFF; // This is equivalent to decimal 255
// (15 * 16^1) + (15 * 16^0) = 240 + 15 = 255
```

### Conversion Methods

*   **From Decimal `int` to Hexadecimal `String`**: `Integer.toHexString(int i)`
*   **From Hexadecimal `String` to Decimal `int`**: `Integer.parseInt(String s, int radix)` with `radix = 16`

### Example: Hexadecimal Numbers

```java
// HexExample.java
public class HexExample {
    public static void main(String[] args) {
        System.out.println("--- Hexadecimal Number Examples ---");

        // 1. Hexadecimal Literal Representation
        int hexLiteral = 0xA2F; // Equivalent to decimal 2607
        System.out.println("\n1. Hexadecimal Literal:");
        System.out.println("  Literal (0xA2F) in decimal: " + hexLiteral); // Output: 2607

        // Hex literals are case-insensitive
        int hexLiteralUppercase = 0XFF;
        int hexLiteralLowercase = 0xff;
        System.out.println("  0XFF: " + hexLiteralUppercase + ", 0xff: " + hexLiteralLowercase); // Output: 255, 255

        // 2. Converting Decimal to Hexadecimal String
        int decimalValue = 4095; // FFF in hex
        String hexString = Integer.toHexString(decimalValue);
        System.out.println("\n2. Decimal to Hexadecimal String:");
        System.out.println("  Decimal " + decimalValue + " in hex: " + hexString); // Output: fff

        int anotherDecimal = 10;
        System.out.println("  Decimal " + anotherDecimal + " in hex: " + Integer.toHexString(anotherDecimal)); // Output: a

        // 3. Converting Hexadecimal String to Decimal Integer
        String hexInput = "1C"; // This is decimal 28
        try {
            int parsedDecimal = Integer.parseInt(hexInput, 16);
            System.out.println("\n3. Hexadecimal String to Decimal Integer:");
            System.out.println("  Hex string \"" + hexInput + "\" parsed to decimal: " + parsedDecimal); // Output: 28
        } catch (NumberFormatException e) {
            System.out.println("  Error parsing hex string: " + e.getMessage());
        }

        // Case-insensitivity for parsing
        String hexInputUppercase = "ABC"; // Decimal 2748
        String hexInputLowercase = "abc"; // Decimal 2748
        System.out.println("  Hex string \"" + hexInputUppercase + "\" parsed to decimal: " + Integer.parseInt(hexInputUppercase, 16));
        System.out.println("  Hex string \"" + hexInputLowercase + "\" parsed to decimal: " + Integer.parseInt(hexInputLowercase, 16));

        // 4. Invalid Hexadecimal String
        String invalidHex = "1G2"; // Contains digit 'G' which is invalid for hex
        try {
            Integer.parseInt(invalidHex, 16);
        } catch (NumberFormatException e) {
            System.out.println("\n4. Invalid Hexadecimal String (Expected Error):");
            System.out.println("  Error parsing \"" + invalidHex + "\": " + e.getMessage());
        }
    }
}
```

#### Input (Implicit from code):

```java
// No direct user input for this example. Values are hardcoded.
```

#### Output:

```plaintext
--- Hexadecimal Number Examples ---

1. Hexadecimal Literal:
  Literal (0xA2F) in decimal: 2607
  0XFF: 255, 0xff: 255

2. Decimal to Hexadecimal String:
  Decimal 4095 in hex: fff
  Decimal 10 in hex: a

3. Hexadecimal String to Decimal Integer:
  Hex string "1C" parsed to decimal: 28
  Hex string "ABC" parsed to decimal: 2748
  Hex string "abc" parsed to decimal: 2748

4. Invalid Hexadecimal String (Expected Error):
  Error parsing "1G2": For input string: "1G2"
```

---

## Important Considerations

*   **Underscores in Numeric Literals (Java 7+)**: For readability, you can place underscores between digits in numeric literals (binary, octal, decimal, hexadecimal). The underscores are ignored by the compiler.
    ```java
    int million = 1_000_000;
    int binaryValue = 0b1011_0100_1101_0001;
    int hexValue = 0xAB_CD_EF;
    ```
*   **`Long` vs. `Integer`**: Similar `to...String()` and `parse...()` methods exist for the `Long` class (`Long.toBinaryString()`, `Long.parseLong()`, etc.) to handle larger numbers.
*   **`valueOf` Method**: `Integer.valueOf(String s, int radix)` and `Long.valueOf(String s, int radix)` also parse strings to their respective `Wrapper` objects.
*   **Error Handling**: Always use `try-catch` blocks when parsing strings that might not conform to the expected number format, as `Integer.parseInt()` and `Long.parseLong()` will throw a `NumberFormatException` for invalid input.

---

This comprehensive guide should give you a solid understanding of how to work with binary, octal, and hexadecimal number formats in Java, both as literals in your code and through conversions with strings.