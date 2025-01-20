import os
import json
from cryptography.fernet import Fernet

class EncryptedDatabase:
    def __init__(self, db_file=None, encryption_key=None):
        # Set default path to Desktop/db.json
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        self.db_file = db_file or os.path.join(desktop_path, "db.json")
        
        # Use provided encryption key or retrieve from environment
        self.encryption_key = encryption_key or os.getenv("DB_ENCRYPTION_KEY") or Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        
        # Load or initialize the database
        self.database = self._load_or_initialize_db()

    def _load_or_initialize_db(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, 'rb') as file:
                encrypted_data = file.read()
                decrypted_data = self.cipher.decrypt(encrypted_data)
                return json.loads(decrypted_data)
        
        # Initialize database with a metadata section
        return {"_meta": {"tables": {}}}

    def _save_db(self):
        encrypted_data = self.cipher.encrypt(json.dumps(self.database).encode())
        with open(self.db_file, 'wb') as file:
            file.write(encrypted_data)

    def define_table(self, table_name, columns):
        if table_name in self.database["_meta"]["tables"]:
            raise ValueError(f"Table '{table_name}' already exists.")
        if not isinstance(columns, list) or not all(isinstance(col, str) for col in columns):
            raise ValueError("Columns must be a list of strings.")
        
        # Add table metadata
        self.database["_meta"]["tables"][table_name] = {"columns": columns}
        self.database[table_name] = []  # Initialize table data
        self._save_db()

    def insert(self, table_name, row):
        if table_name not in self.database["_meta"]["tables"]:
            raise ValueError(f"Table '{table_name}' does not exist.")
        columns = self.database["_meta"]["tables"][table_name]["columns"]
        if set(row.keys()) != set(columns):
            raise ValueError("Row does not match table columns.")
        self.database[table_name].append(row)
        self._save_db()

    def read(self, table_name, filters=None):
        if table_name not in self.database["_meta"]["tables"]:
            raise ValueError(f"Table '{table_name}' does not exist.")
        rows = self.database[table_name]
        if filters:
            rows = [row for row in rows if all(row[k] == v for k, v in filters.items())]
        return rows

    def update(self, table_name, filters, updates):
        if table_name not in self.database["_meta"]["tables"]:
            raise ValueError(f"Table '{table_name}' does not exist.")
        columns = self.database["_meta"]["tables"][table_name]["columns"]
        for key in updates.keys():
            if key not in columns:
                raise ValueError(f"Column '{key}' does not exist in table '{table_name}'.")
        updated_rows = 0
        for row in self.database[table_name]:
            if all(row.get(k) == v for k, v in filters.items()):
                for k, v in updates.items():
                    row[k] = v
                updated_rows += 1
        self._save_db()
        return updated_rows

    def delete(self, table_name, filters):
        if table_name not in self.database["_meta"]["tables"]:
            raise ValueError(f"Table '{table_name}' does not exist.")
        original_count = len(self.database[table_name])
        self.database[table_name] = [
            row for row in self.database[table_name]
            if not all(row.get(k) == v for k, v in filters.items())
        ]
        deleted_count = original_count - len(self.database[table_name])
        self._save_db()
        return deleted_count

    def list_tables(self):
        return list(self.database["_meta"]["tables"].keys())

    def get_table_schema(self, table_name):
        if table_name not in self.database["_meta"]["tables"]:
            raise ValueError(f"Table '{table_name}' does not exist.")
        return self.database["_meta"]["tables"][table_name]["columns"]

    def get_database_info(self):
        """
        Returns metadata about the database, including all table names and their columns.
        """
        return self.database["_meta"]["tables"]

    def get_encryption_key(self):
        """
        Returns the current encryption key being used by the database.
        """
        return self.encryption_key


if __name__ == "__main__":
    # Load the encryption key from a file
    with open("encryption_key.key", "rb") as key_file:
        custom_key = key_file.read()

    # Make json db instance
    db = EncryptedDatabase(encryption_key=custom_key.encode())

    # Insert rows
    db.insert("users", {"id": 1, "name": "Alice", "email": "alice@example.com"})
    db.insert("users", {"id": 2, "name": "Bob", "email": "bob@example.com"})
    
    # Read rows
    print("All users:", db.read("users"))
    print("Filtered users:", db.read("users", filters={"name": "Alice"}))

    # Update rows
    db.update("users", filters={"id": 1}, updates={"email": "alice_new@example.com"})
    print("After update:", db.read("users"))

    # Delete rows
    db.delete("users", filters={"id": 2})
    print("After delete:", db.read("users"))
    
    # List tables and their schemas
    print("List of tables:", db.list_tables())
    print("Schema for 'users':", db.get_table_schema("users"))

    # Get full database info
    print("Database metadata:", db.get_database_info())

    # Print or save the encryption key
    print("Encryption Key:", db.get_encryption_key())
