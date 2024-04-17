import crypt

# Open the password file in read-only mode
with open('/etc/shadow', 'r') as f:
    # Create a dictionary to store username-password pairs
    user_passwords = {}

    # Iterate through each line in the file
    for line in f:
        # Split the line into fields
        fields = line.strip().split(':')

        # Extract the username and hashed password
        username = fields[0]
        hashed_password = fields[1]

        # Decrypt the hashed password using crypt.crypt()
        decrypted_password = crypt.crypt("password", hashed_password)

        # Store the username and decrypted password in the dictionary
        user_passwords[username] = decrypted_password

# Display the username-password pairs
for username, decrypted_password in user_passwords.items():
    print(f"Username: {username}, Password: {decrypted_password}")
