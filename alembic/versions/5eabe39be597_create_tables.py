"""create tables

Revision ID: 5eabe39be597
Revises: 
Create Date: 2021-12-25 02:07:37.870336

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "5eabe39be597"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TYPE EmployeeStatus AS ENUM ('works', 'blacklist', 'fired');
        CREATE TYPE TaskPriority AS ENUM ('minor', 'normal', 'major', 'hot');
        CREATE TYPE TaskStatus AS ENUM ('done', 'in_progress', 'selected_for_development');
        CREATE TYPE LeaveType AS ENUM ('vacation', 'sick_leave');
        CREATE TYPE PhoneStatus AS ENUM ('active', 'deprecated');
        CREATE TYPE LeaveStatus AS ENUM ('confirmed', 'rejected', 'pending');
        
        CREATE TABLE IF NOT EXISTS employees(
            id serial PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            middle_name VARCHAR(255),
            last_name VARCHAR(255) NOT NULL,
            info TEXT,
            date_of_birth DATE,
            hired_on DATE NOT NULL,
            fired_on DATE,
            status EmployeeStatus NOT NULL DEFAULT 'works'
        );
        
        CREATE TABLE IF NOT EXISTS tasks(
            id serial PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            priority TaskPriority NOT NULL DEFAULT 'normal',
            status TaskStatus NOT NULL DEFAULT 'selected_for_development',
            assignee_id INT,
            FOREIGN KEY (assignee_id) REFERENCES employees(id),
            reporter_id INT,
            FOREIGN KEY (reporter_id) REFERENCES employees(id),
            created_at timestamp,
            employee_id INT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        );
        
        CREATE TABLE IF NOT EXISTS links(
            id serial PRIMARY KEY,
            name VARCHAR(255),
            link VARCHAR(511),
            employee_id INT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        );
        
        CREATE TABLE IF NOT EXISTS leaves(
            id serial PRIMARY KEY,
            leave_type LeaveType NOT NULL DEFAULT 'vacation',
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            status LeaveStatus NOT NULL DEFAULT 'pending',
            approved_by INT,
            FOREIGN KEY (approved_by) REFERENCES employees(id),
            requested_at TIMESTAMP NOT NULL,
            approved_at TIMESTAMP,
            employee_id INT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        );
        
        CREATE TABLE IF NOT EXISTS phone_numbers(
            id serial PRIMARY KEY,
            phone VARCHAR(255) ,
            status PhoneStatus NOT NULL DEFAULT 'active',
            employee_id INT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        );
        """
    )


def downgrade():
    pass
