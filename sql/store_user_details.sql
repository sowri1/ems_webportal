CREATE OR REPLACE PROCEDURE store_user_details (eml VARCHAR, nm VARCHAR, gdr BOOLEAN, dob DATE, p_no BIGINT)
LANGUAGE plpgsql
AS $$
	BEGIN
		INSERT INTO user_details (email, name, gender, d_o_b, phone_no) VALUES(eml, nm, gdr, dob, p_no) ON CONFLICT ON CONSTRAINT user_details_pkey DO UPDATE set name = nm, d_o_b = dob, phone_no = p_no;
	END;
$$;