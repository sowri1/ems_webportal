CREATE or REPLACE FUNCTION get_emp_details(emp_email VARCHAR)
RETURNS TABLE (emp_name VARCHAR, org_name VARCHAR, emp_role INT, org_id INT)
AS $$
	BEGIN
		RETURN QUERY SELECT
			user_details.name as emp_name, organisation.name as org_name, org_employees.type as emp_role, organisation.id as org_id FROM user_details INNER JOIN org_employees on user_details.email = emp_email and org_employees.employee_email = user_details.email  INNER JOIN organisation on organisation.id = org_employees.org_id;
	END; 
$$
LANGUAGE plpgsql;