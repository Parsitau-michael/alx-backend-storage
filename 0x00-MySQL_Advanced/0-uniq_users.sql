-- The script below creates a table users with the following attributes:
--	id, integer, never null, auto increment and primary key
--	email, string (255 characters), never null and unique
--	name, string (255 characters)
-- Ps; The script handles cases where the table already exists
CREATE TABLE IF NOT EXISTS users(
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255)
);
