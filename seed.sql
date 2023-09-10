INSERT INTO roles (id, description) VALUES(1, 'admin');
INSERT INTO roles (id, description) VALUES(2, 'user');

INSERT INTO claims (id, description, active) VALUES(1, 'profile', true);
INSERT INTO claims (id, description, active) VALUES(2, 'investiments', true);
INSERT INTO claims (id, description, active) VALUES(3, 'transactions', true);
INSERT INTO claims (id, description, active) VALUES(4, 'extrato', true);

INSERT INTO users (id, "name", email, "password", role_id, updated_at, created_at) VALUES(1, 'victor', 'stuntaro@protonmail.com', 'b4cfad9682ee033ceb45daf2d7b20db9fce2abef331cfe38d7f86aff5794c5a952072d74787209f739592e2008eb8529575336f43d9a7db1a130ee6a9a919531', 1, NULL, '2022-02-25 15:22:20.757');
INSERT INTO users (id, "name", email, "password", role_id, updated_at, created_at) VALUES(2, 'victor', 'nutaro@protonmail.com', '2856ee1bfef51ca14242829d786dca3983436e715abb0a094f517f6dc391e336435d4329e43f0ca7315f5eae9ca2dca3ce80d6424957d5d9458c74bd15b432b6', 1, NULL, '2022-02-25 15:22:20.757');
INSERT INTO users (id, "name", email, "password", role_id, updated_at, created_at) VALUES(3, 'victor', 'cabal@protonmail.com', '736bc0c5ac9b8b83c33c726849300155c11c20ae49512b3a3071506d37acf2151728e763f3259b99a8546941f1fcbeef12f058cdbef4ee17ba22681eaf6ffc77', 1, NULL, '2022-02-25 15:22:20.757');
INSERT INTO users (id, "name", email, "password", role_id, updated_at, created_at) VALUES(4, 'victor', 'nix@protonmail.com', '61bb26da1e6055756348f4b770dbd4d5e857086d079b8352bf1b4139c71c2df5c692893748fc515dea874c15902104ed189e0e5edb108ed7823aa92b4b817906', 2, NULL, '2022-02-25 15:22:20.757');
INSERT INTO users (id, "name", email, "password", role_id, updated_at, created_at) VALUES(5, 'victor', 'blats@protonmail.com', 'ea4a71e59cd00b380e00fd2b8e76cb786600955d259b08df54c43c501c91d38e2b6c69823f2ecb38de098017ee2e91ea240bd764db5e3d65206d0bd0bfc32162', 2, NULL, '2022-02-25 15:22:20.757');

INSERT INTO user_claims (user_id, claim_id) VALUES(1, 1);
INSERT INTO user_claims (user_id, claim_id) VALUES(1, 2);
INSERT INTO user_claims (user_id, claim_id) VALUES(1, 3);
INSERT INTO user_claims (user_id, claim_id) VALUES(1, 4);
INSERT INTO user_claims (user_id, claim_id) VALUES(2, 1);
INSERT INTO user_claims (user_id, claim_id) VALUES(2, 4);
INSERT INTO user_claims (user_id, claim_id) VALUES(3, 1);
INSERT INTO user_claims (user_id, claim_id) VALUES(3, 3);
INSERT INTO user_claims (user_id, claim_id) VALUES(4, 1);
INSERT INTO user_claims (user_id, claim_id) VALUES(4, 4);
