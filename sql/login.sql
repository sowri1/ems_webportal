CREATE OR REPLACE FUNCTION login_user(eml VARCHAR, pwd VARCHAR)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
	BEGIN
		IF (SELECT 1 FROM users WHERE email = eml and password = MD5(MD5(MD5(pwd)))) THEN
			RETURN 1;
		ELSE
			RETURN 0;
		END IF;
	END;
$$;