-- Inserta con nuevos usernames únicos
INSERT INTO users (email, username, first_name, last_name, hashed_password, is_active, role)
VALUES
('alice2@example.com', 'alice2', 'Alice', 'Smith', 'hashed_pwd_1', 1, 'admin'),
('bob2@example.com', 'bob2', 'Bob', 'Johnson', 'hashed_pwd_2', 1, 'user'),
('carol2@example.com', 'carol2', 'Carol', 'Williams', 'hashed_pwd_3', 0, 'user'),
('david2@example.com', 'david2', 'David', 'Brown', 'hashed_pwd_4', 1, 'moderator'),
('eve2@example.com', 'eve2', 'Eve', 'Davis', 'hashed_pwd_5', 1, 'user');


INSERT INTO todos (title, description, priority, complete, owner_id)
VALUES
('Buy groceries', 'Milk, eggs, bread, and coffee', 2, 0, 1),
('Finish report', 'Complete the quarterly financial report', 3, 0, 2),
('Workout', 'Go to the gym for 1 hour', 1, 1, 2),
('Book flight tickets', 'Flight to New York for conference', 2, 0, 3),
('Pay bills', 'Electricity and Internet', 1, 1, 1),
('Call mom', 'Check in with mom this weekend', 1, 0, 4),
('Read book', 'Read 50 pages of a new novel', 2, 0, 5),
('Clean room', 'Organize desk and vacuum floor', 1, 1, 4),
('Update resume', 'Add recent work experience', 3, 0, 5),
('Plan trip', 'Plan a trip to the mountains', 2, 0, 3);
