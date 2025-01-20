
# **Encrypted JSON Database**

The motivation behind creating this project was our need for a local database for a desktop application while ensuring its security—even from regular users—to prevent data breaches. I decided to share this tool with anyone looking to establish a secure, JSON-based database. It's a simple, lightweight, and encrypted system that's easy to implement in Python. This library offers a straightforward way to securely store and manage structured data, with full support for CRUD operations.

---

## **Features**
- **Encrypted Storage**: Uses AES encryption (via `cryptography` library) to protect your data.
- **Table Management**: Define tables with schemas to ensure data consistency.
- **CRUD Operations**: Supports Create, Read, Update, and Delete operations.
- **Custom Encryption Key Management**: You can provide your own encryption key or let the system generate one.
- **Cross-Platform**: Works seamlessly on macOS, Windows, and Linux.

---

## **Installation**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/json-database.git
   cd json-database
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.x installed, then install the required library:
   ```bash
   pip install cryptography
   ```

3. **Generate an Encryption Key**:
   Run the following command to generate a key and save it to a file:
   ```python
   from cryptography.fernet import Fernet
   key = Fernet.generate_key()
   with open("encryption_key.key", "wb") as key_file:
       key_file.write(key)
   ```

---

## **Usage**

### **1. Import and Initialize**
```python
from db import EncryptedDatabase

# Load the encryption key from a file
with open("encryption_key.key", "rb") as key_file:
    encryption_key = key_file.read()

# Create a database instance
db = EncryptedDatabase(encryption_key=encryption_key)
```

---

### **2. Define a Table**
Create a table with a specified schema:
```python
db.define_table("users", ["id", "name", "email"])
```

---

### **3. Insert Data**
Insert rows into the defined table:
```python
db.insert("users", {"id": 1, "name": "Alice", "email": "alice@example.com"})
db.insert("users", {"id": 2, "name": "Bob", "email": "bob@example.com"})
```

---

### **4. Read Data**
Retrieve all rows or filter data:
```python
# Fetch all rows
print(db.read("users"))

# Filter rows
print(db.read("users", filters={"name": "Alice"}))
```

---

### **5. Update Data**
Update specific rows matching the filter criteria:
```python
db.update("users", filters={"id": 1}, updates={"email": "alice_new@example.com"})
```

---

### **6. Delete Data**
Delete rows based on a filter:
```python
db.delete("users", filters={"id": 2})
```

---

### **7. Manage Database Schema**
- **List Tables**:
   ```python
   print(db.list_tables())
   ```
- **Get Table Schema**:
   ```python
   print(db.get_table_schema("users"))
   ```
- **Get Database Metadata**:
   ```python
   print(db.get_database_info())
   ```

---

## **Security Notes**
1. **Encryption Key**:
   - The encryption key is essential for accessing the database. Store it securely (e.g., in a secure secrets manager or environment variable).
   - Losing the key will result in irreversible data loss, as the database cannot be decrypted.

2. **Database File**:
   - The database file (`db.json`) is encrypted and secure even if accessed by unauthorized users.
   - Use proper file permissions to prevent tampering.

---

## **File Structure**
The project structure:
```
json-database/
├── db.py                # Core implementation
├── README.md            # Documentation
├── encryption_key.key   # Encryption key (keep secure)
├── db.json              # Encrypted database file (auto-generated)
├── .gitignore           # Files to ignore in version control
```

---

## **Advanced Tips**

### **1. Use Environment Variables**
Store the encryption key in an environment variable for better security:
```bash
export DB_ENCRYPTION_KEY=$(cat encryption_key.key)
```
Load it in Python:
```python
import os
encryption_key = os.getenv("DB_ENCRYPTION_KEY").encode()
db = EncryptedDatabase(encryption_key=encryption_key)
```

---

### **2. Key Rotation**
To rotate the encryption key:
1. Decrypt the database with the old key.
2. Re-encrypt it with the new key:
   ```python
   new_key = Fernet.generate_key()
   db = EncryptedDatabase(encryption_key=old_key)
   data = db.read_all()  # Hypothetical method to read all unencrypted data
   db = EncryptedDatabase(encryption_key=new_key)
   db.rewrite_all(data)  # Hypothetical method to re-encrypt data with a new key
   ```

---

## **License**
This project is licensed under the MIT License.
