CREATE or REPLACE FUNCTION get_org_employee(orgId INT)
RETURNS TABLE (name VARCHAR, email VARCHAR) 
AS $$ 
BEGIN
	RETURN QUERY SELECT
		user_details.name, user_details.email
		FROM org_employees INNER JOIN user_details on org_employees.org_id = orgId and org_employees.employee_email = user_details.email;
END;
$$
LANGUAGE plpgsql;