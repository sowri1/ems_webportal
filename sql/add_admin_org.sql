CREATE OR REPLACE FUNCTION store_org_admin(org_name VARCHAR, admin_email VARCHAR, admin_pass VARCHAR) 
RETURNS INTEGER 
LANGUAGE plpgsql
AS $$
	DECLARE org_id INTEGER;
	DECLARE is_admin BOOLEAN;
	BEGIN
		IF (SELECT 1 FROM users WHERE email = admin_email) THEN
			RETURN 0;
		ELSE
			INSERT INTO users (email, password) VALUES(admin_email, MD5(MD5(MD5(admin_pass))));
			INSERT INTO organisation(name, admin) VALUES(org_name, admin_email) RETURNING id INTO org_id;
			INSERT INTO org_employees(org_id, employee_email, type) VALUES(org_id, admin_email, 1);
			RETURN 1;
		END IF;
	END;
$$;