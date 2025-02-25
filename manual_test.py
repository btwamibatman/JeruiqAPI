import bcrypt

password = "passAAALLL3"

# Generate hash
hashed_password = "$2b$12$n8iGv7/7W8jR4dQP3n4.TOUrc2ek6vIAVV6TbVkzQiTe.P8yGajeW"

# Print for debugging
print(f"Generated Hash: {hashed_password}")

# Verify immediately
if bcrypt.checkpw(password.encode(), hashed_password.encode()):
    print("✅ Password is correct!")
else:
    print("❌ Incorrect password!")
