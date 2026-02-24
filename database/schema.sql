-- College Library Database Schema
-- MySQL Database

CREATE DATABASE IF NOT EXISTS college_library;
USE college_library;

-- Books Table
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    publisher VARCHAR(100),
    publication_year INT,
    category VARCHAR(50),
    total_copies INT DEFAULT 1,
    available_copies INT DEFAULT 1,
    location VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_isbn (isbn),
    INDEX idx_title (title),
    INDEX idx_author (author),
    INDEX idx_category (category)
);

-- Members Table
CREATE TABLE IF NOT EXISTS members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    membership_type VARCHAR(20) DEFAULT 'standard',
    join_date DATE NOT NULL,
    expiry_date DATE,
    status VARCHAR(20) DEFAULT 'active',
    max_books_allowed INT DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_member_id (member_id),
    INDEX idx_email (email),
    INDEX idx_status (status)
);

-- Transactions Table (Borrow/Return records)
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id VARCHAR(30) UNIQUE NOT NULL,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    fine_amount FLOAT DEFAULT 0.0,
    fine_paid BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'active',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,

    INDEX idx_transaction_id (transaction_id),
    INDEX idx_book_id (book_id),
    INDEX idx_member_id (member_id),
    INDEX idx_status (status),
    INDEX idx_borrow_date (borrow_date)
);

-- Fines Table
CREATE TABLE IF NOT EXISTS fines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL,
    member_id INT NOT NULL,
    amount FLOAT NOT NULL,
    reason VARCHAR(100),
    status VARCHAR(20) DEFAULT 'unpaid',
    paid_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,

    INDEX idx_member_id (member_id),
    INDEX idx_status (status)
);

-- Insert Sample Data
INSERT INTO books (isbn, title, author, publisher, publication_year, category, total_copies, available_copies, location) VALUES
('978-0-13-468599-1', 'Introduction to Algorithms', 'Thomas H. Cormen', 'MIT Press', 2009, 'Computer Science', 5, 5, 'A-101'),
('978-0-07-352332-2', 'Data Structures and Algorithms', 'Michael T. Goodrich', 'McGraw-Hill', 2014, 'Computer Science', 3, 3, 'A-102'),
('978-0-201-63361-0', 'Design Patterns', 'Erich Gamma', 'Addison-Wesley', 1994, 'Computer Science', 4, 4, 'A-103'),
('978-0-13-110362-7', 'The C Programming Language', 'Brian W. Kernighan', 'Prentice Hall', 1988, 'Computer Science', 2, 2, 'A-104'),
('978-0-06-112008-4', 'To Kill a Mockingbird', 'Harper Lee', 'J.B. Lippincott', 1960, 'Fiction', 3, 3, 'B-101'),
('978-0-7432-7356-5', 'The Great Gatsby', 'F. Scott Fitzgerald', 'Scribner', 1925, 'Fiction', 2, 2, 'B-102'),
('978-0-452-28423-4', '1984', 'George Orwell', 'Secker & Warburg', 1949, 'Fiction', 4, 4, 'B-103'),
('978-0-316-76948-0', 'The Catcher in the Rye', 'J.D. Salinger', 'Little, Brown', 1951, 'Fiction', 2, 2, 'B-104');

INSERT INTO members (member_id, first_name, last_name, email, phone, address, membership_type, join_date, expiry_date, status, max_books_allowed) VALUES
('LIB00001', 'John', 'Doe', 'john.doe@email.com', '555-0101', '123 Main St', 'premium', '2024-01-15', '2025-01-15', 'active', 5),
('LIB00002', 'Jane', 'Smith', 'jane.smith@email.com', '555-0102', '456 Oak Ave', 'standard', '2024-02-01', '2025-02-01', 'active', 3),
('LIB00003', 'Mike', 'Johnson', 'mike.johnson@email.com', '555-0103', '789 Pine Rd', 'standard', '2024-02-15', '2025-02-15', 'active', 3);