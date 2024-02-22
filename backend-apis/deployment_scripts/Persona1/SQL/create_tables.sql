-- Copyright 2024 Google LLC
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--     http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.

CREATE TABLE products (
	id INT NOT NULL,
	title VARCHAR(300),
	description VARCHAR(2000),
	image VARCHAR(300),
	features VARCHAR(1000),
	categories VARCHAR(1000),
	price DECIMAL(6,2) NOT NULL,
	quantity INT,
	owner VARCHAR(100),
	featured BIT(1),
	PRIMARY KEY(id)
);
