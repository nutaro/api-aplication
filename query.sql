select users.name, users.email, roles.description, claims.description from users 
	left join roles on users.role_id = roles.id
	left join user_claims on users.id = user_claims.user_id
	left join claims on user_claims.claim_id = claims.id;