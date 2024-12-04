drop database if exists todo_list;

create database todo_list;

use  todo_list;
CREATE TABLE todo_items (
    task_num INT AUTO_INCREMENT PRIMARY KEY,
    task_text VARCHAR(255),
    countdown VARCHAR(10),
    importance INTEGER(10),
    due_date DATETIME
);