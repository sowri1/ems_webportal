CREATE OR REPLACE FUNCTION validate_login(eml VARCHAR, tkn VARCHAR)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
	BEGIN
		IF (SELECT 1 FROM user_login_sessions WHERE email = eml and token = tkn) THEN
			RETURN 1;
		ELSE
			RETURN 0;
		END IF;
	END;
$$;