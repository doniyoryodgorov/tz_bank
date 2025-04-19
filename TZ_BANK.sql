create database TZ_BANK

USE TZ_BANK
GO

CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    phone_number NVARCHAR(15) UNIQUE NOT NULL,
    email NVARCHAR(100) UNIQUE,
    created_at DATETIME DEFAULT GETDATE(),
    last_active_at DATETIME,
    status NVARCHAR(20) DEFAULT 'active', -- active, blocked, vip
    is_vip BIT DEFAULT 0,
    total_balance BIGINT DEFAULT 0
);

CREATE TABLE cards (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE,
    card_number NVARCHAR(16) UNIQUE NOT NULL,
    balance BIGINT DEFAULT 0,
    is_blocked BIT DEFAULT 0,
    created_at DATETIME DEFAULT GETDATE(),
    card_type NVARCHAR(20) CHECK (card_type IN ('debit', 'credit', 'savings')),
    limit_amount BIGINT DEFAULT 150000000
);

CREATE TABLE transactions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    from_card_id INT,
    to_card_id INT,
    amount BIGINT NOT NULL,
    status NVARCHAR(20) CHECK (status IN ('pending', 'success', 'failed')) DEFAULT 'pending',
    created_at DATETIME DEFAULT GETDATE(),
    transaction_type NVARCHAR(20) CHECK (transaction_type IN ('transfer', 'withdrawal', 'deposit')),
    is_flagged BIT DEFAULT 0,

    -- Tashqi kalitlar
    CONSTRAINT FK_Transactions_FromCard FOREIGN KEY (from_card_id) 
        REFERENCES cards(id) ON DELETE NO ACTION,

    CONSTRAINT FK_Transactions_ToCard FOREIGN KEY (to_card_id) 
        REFERENCES cards(id) ON DELETE NO ACTION
);


CREATE TABLE logs (
    id INT IDENTITY(1,1) PRIMARY KEY,
    transaction_id INT FOREIGN KEY REFERENCES transactions(id) ON DELETE CASCADE,
    message NVARCHAR(MAX) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE reports (
    id INT IDENTITY(1,1) PRIMARY KEY,
    report_type NVARCHAR(50), -- daily, weekly, monthly
    created_at DATETIME DEFAULT GETDATE(),
    total_transactions BIGINT DEFAULT 0,
    flagged_transactions BIGINT DEFAULT 0,
    total_amount BIGINT DEFAULT 0
);

CREATE TABLE fraud_detection (
    id INT IDENTITY(1,1) PRIMARY KEY,
    transaction_id INT FOREIGN KEY REFERENCES transactions(id) ON DELETE CASCADE,
    user_id INT FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE,
    reason NVARCHAR(MAX) NOT NULL,
    status NVARCHAR(20) CHECK (status IN ('pending', 'reviewed', 'blocked')) DEFAULT 'pending',
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE scheduled_payments (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    card_id INT,
    amount BIGINT NOT NULL,
    payment_date DATETIME NOT NULL,
    status NVARCHAR(20) CHECK (status IN ('pending', 'completed', 'failed')) DEFAULT 'pending',
    created_at DATETIME DEFAULT GETDATE(),

    CONSTRAINT FK_ScheduledPayments_User FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE NO ACTION,

    CONSTRAINT FK_ScheduledPayments_Card FOREIGN KEY (card_id) 
        REFERENCES cards(id) ON DELETE NO ACTION
);


CREATE TABLE vip_users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE,
    assigned_at DATETIME DEFAULT GETDATE(),
    reason NVARCHAR(MAX) NOT NULL
);

CREATE TABLE blocked_users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE,
    blocked_at DATETIME DEFAULT GETDATE(),
    reason NVARCHAR(MAX) NOT NULL
);


