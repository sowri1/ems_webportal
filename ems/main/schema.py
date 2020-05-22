import graphene
import psycopg2
from collections import namedtuple
import secrets

conn = psycopg2.connect("host=localhost dbname=test user=sowri password=6461")
cur = conn.cursor()

class user_details(graphene.ObjectType):
	emp_name = graphene.String()
	org_name = graphene.String()
	emp_role = graphene.Int()
	org_id = graphene.Int()

class org_employees(graphene.ObjectType):
	name = graphene.String()
	email = graphene.String()

def get_db_rows(sql, cols = None):
	cur.execute(sql)
	if cols is None:
		columns = [col[0] for col in cur.description]
	else:
		columns = cols
	RowType = namedtuple('Row', columns)
	data = [
		RowType(*row)
		for row in cur.fetchall() ]
	return data

def ret_data(data, cols = None):
	RowType = namedtuple('Row', cols)
	print(data)
	ret_dat = [
		RowType(dt)
		for dt in data ]
	print(ret_dat)
	return ret_dat

class result(graphene.ObjectType):
    result = graphene.ID()

class add_org_admin(graphene.Mutation):
	class Arguments:
		org_name = graphene.String()
		admin_email = graphene.String()
		admin_pass = graphene.String()

	sess_token = graphene.String()
	email = graphene.String()

	def mutate(self, args, org_name, admin_email, admin_pass):
		print("hello")
		print(org_name, admin_email, admin_pass)
		token = secrets.token_urlsafe(64)
		# cur.execute("SELECT store_org_admin('{}', '{}', '{}');".format(org_name, admin_email, admin_pass))
		# conn.commit()
		# out = cur.fetchone()
		out = (1,)
		print(out)
		if int(out[0]) == 1:
			# cur.execute("CALL add_token('{}', '{}');".format(admin_email, token))
			return add_org_admin(sess_token = token, email = admin_email)
		else:
			return add_org_admin(sess_token = 0, email = admin_email)
	

class add_user_details(graphene.Mutation):
	class Arguments:
		name = graphene.String()
		gender = graphene.Boolean()
		email = graphene.String()
		d_o_b = graphene.String()
		phone_no = graphene.ID()

	result = graphene.Int()

	def mutate(self, args, name, gender, email, d_o_b, phone_no):
		cur.execute("CALL store_user_details('{}', '{}', '{}', '{}', {});".format(email, name, gender, d_o_b, phone_no))
		# conn.commit()
		return add_user_details(result = 1)

class add_user(graphene.Mutation):
	class Arguments:
		org_id = graphene.Int()
		email = graphene.String()
		password = graphene.String() 
		role = graphene.Int()

	result = graphene.Int()

	def mutate(self, args, org_id, email, password, role):
		cur.execute("SELECT add_user({}, '{}', '{}', {});".format(org_id, email, password, role))
		conn.commit()
		res = cur.fetchone()[0]
		print(res)
		# conn.commit()
		return add_user_details(result = 1)
		

class Query(graphene.ObjectType):
	class Meta:
		type_name = 'Query'

	test = graphene.List(result, param = graphene.Int())
	validate_user_login = graphene.List(result, email = graphene.String(), token = graphene.String())
	user_login = graphene.List(result, email = graphene.String(), password = graphene.String())
	emp_details = graphene.List(user_details, email = graphene.String())
	org_emp = graphene.List(org_employees, org_id = graphene.Int())

	def resolve_test(self, args, param=None):
		print("Working")
		print(param)
		out = namedtuple('result', result)
		res = (out(1),)
		return [(1)]
	
	def resolve_validate_user_login(self, args, email, token):
		sql = "SELECT validate_login('{}', '{}');".format(email, token)
		return get_db_rows(sql, cols = ['result'])

	def resolve_user_login(self, args, email, password):
		sql = "SELECT login_user('{}', '{}');".format(email, password)
		print(email, password)
		cur.execute(sql)
		is_success = cur.fetchone()[0]
		print(is_success)
		if int(is_success) == 1:
			token = secrets.token_urlsafe(64)
			cur.execute("CALL add_token('{}', '{}');".format(email, token))
			conn.commit()
			return ret_data([email, token], cols = ['result'])
		else:
			return ret_data([0], cols = ['result'])

	def resolve_emp_details(self, args, email):
		print("coming")
		sql = "SELECT * FROM get_emp_details('{}');".format(email)
		return get_db_rows(sql)

	def resolve_org_emp(self, args, org_id):
		sql = "SELECT * FROM get_org_employee({});".format(org_id)
		return get_db_rows(sql)
		

class Mutation(graphene.ObjectType):
	addOrgAdmin = add_org_admin.Field()
	addUserDetails = add_user_details.Field()
	addUser = add_user.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)