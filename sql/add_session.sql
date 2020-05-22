CREATE or REPLACE PROCEDURE add_token(eml VARCHAR, tkn TEXT)
LANGUAGE plpgsql
AS $$
	BEGIN
		INSERT INTO user_login_sessions(email, token) VALUES(eml, tkn) ON CONFLICT ON CONSTRAINT email_pk DO UPDATE SET token = tkn;		
	END;
$$;