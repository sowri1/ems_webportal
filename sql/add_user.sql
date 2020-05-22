CREATE OR REPLACE FUNCTION add_user(orgId INT, eml VARCHAR, pass VARCHAR, role INT) 
RETURNS INTEGER 
LANGUAGE plpgsql
AS $$
	DECLARE org_id INTEGER;
	DECLARE is_admin BOOLEAN;
	BEGIN
		IF (SELECT 1 FROM users WHERE email = eml) THEN
			RETURN 0;
		ELSE
 			INSERT INTO users (email, password) VALUES(eml, MD5(MD5(MD5(pass))));
 			INSERT INTO org_employees(org_id, employee_email, type) VALUES(orgId, eml, role);
			RETURN 1;
		END IF;
	END;
$$;