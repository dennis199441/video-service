create table process_types (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(250) NOT NULL,
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW(),
    PRIMARY KEY(id)
);

create table process(
	id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    type_id INT NOT NULL,
    filename VARCHAR(250) NOT NULL,
    hashed_name TEXT NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW(),
    PRIMARY KEY(id),
    FOREIGN KEY(type_id) REFERENCES process_types(id) ON DELETE CASCADE
);

CREATE INDEX idx_process_1 ON process(user_id);