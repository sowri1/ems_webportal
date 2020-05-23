CREATE OR REPLACE PROCEDURE add_user_usage_time(eml VARCHAR, dt DATE, st_tm TIME, wk_tm INT, md INT)
LANGUAGE  plpgsql
AS $$
	BEGIN
 		INSERT INTO emp_usage(email, _date, start_time , work_time, mode) VALUES (eml, dt, st_tm, wk_tm, md);
	END
$$